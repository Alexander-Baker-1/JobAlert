import sqlite3
from datetime import datetime
from job import Job

class JobDatabase:
    def __init__(self, db_path="jobs.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create the jobs table with status tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT NOT NULL,
                salary TEXT,
                url TEXT,
                keyword TEXT,
                search_location TEXT,
                scraped_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'new',
                status_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                UNIQUE(title, company, location)
            )
        ''')
        
        # Add status column to existing tables if it doesn't exist
        try:
            cursor.execute('ALTER TABLE jobs ADD COLUMN status TEXT DEFAULT "new"')
        except sqlite3.OperationalError:
            pass  # Column already exists
            
        try:
            cursor.execute('ALTER TABLE jobs ADD COLUMN status_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
        except sqlite3.OperationalError:
            pass
            
        try:
            cursor.execute('ALTER TABLE jobs ADD COLUMN notes TEXT')
        except sqlite3.OperationalError:
            pass
        
        conn.commit()
        conn.close()
    
    def save_jobs(self, jobs):
        """Save a list of Job objects to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        saved_count = 0
        for job in jobs:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO jobs 
                    (title, company, location, salary, url, keyword, search_location, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'new')
                ''', (job.title, job.company, job.location, job.salary, 
                      job.url, job.keyword, job.search_location))
                
                if cursor.rowcount > 0:
                    saved_count += 1
                    
            except sqlite3.Error as e:
                print(f"Error saving job: {e}")
        
        conn.commit()
        conn.close()
        
        print(f"Saved {saved_count} new jobs to database")
        return saved_count
    
    def get_jobs_by_status(self, status):
        """Get jobs filtered by status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, company, location, salary, url, keyword, 
                   search_location, scraped_date, status, notes 
            FROM jobs 
            WHERE status = ? 
            ORDER BY scraped_date DESC
        ''', (status,))
        
        rows = cursor.fetchall()
        conn.close()
        
        jobs = []
        for row in rows:
            job_data = {
                'id': row[0],
                'title': row[1],
                'company': row[2],
                'location': row[3],
                'salary': row[4],
                'url': row[5],
                'keyword': row[6],
                'search_location': row[7],
                'scraped_date': row[8],
                'status': row[9],
                'notes': row[10]
            }
            jobs.append(job_data)
        
        return jobs
    
    def update_job_status(self, job_id, new_status, notes=None):
        """Update a job's status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if notes is not None:
            cursor.execute('''
                UPDATE jobs 
                SET status = ?, status_updated = ?, notes = ?
                WHERE id = ?
            ''', (new_status, datetime.now(), notes, job_id))
        else:
            cursor.execute('''
                UPDATE jobs 
                SET status = ?, status_updated = ?
                WHERE id = ?
            ''', (new_status, datetime.now(), job_id))
        
        conn.commit()
        conn.close()
        
        return cursor.rowcount > 0
    
    def get_all_jobs(self):
        """Get all jobs (for backward compatibility)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM jobs ORDER BY scraped_date DESC')
        rows = cursor.fetchall()
        
        jobs = []
        for row in rows:
            job = Job(
                title=row[1],
                company=row[2],
                location=row[3],
                salary=row[4],
                url=row[5],
                keyword=row[6],
                search_location=row[7]
            )
            jobs.append(job)
        
        conn.close()
        return jobs
    
    def get_status_counts(self):
        """Get count of jobs by status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT status, COUNT(*) 
            FROM jobs 
            GROUP BY status
        ''')
        
        status_counts = dict(cursor.fetchall())
        conn.close()
        
        # Ensure all statuses are present
        all_statuses = ['new', 'in_progress', 'applied', 'not_interested']
        for status in all_statuses:
            if status not in status_counts:
                status_counts[status] = 0
                
        return status_counts
    
    def get_stats(self):
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM jobs')
        total_jobs = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT company) FROM jobs')
        unique_companies = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT location) FROM jobs')
        unique_locations = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_jobs': total_jobs,
            'unique_companies': unique_companies,
            'unique_locations': unique_locations
        }