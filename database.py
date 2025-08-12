import sqlite3
from datetime import datetime
from job import Job

class JobDatabase:
    def __init__(self, db_path="jobs.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create the jobs table if it doesn't exist."""
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
                UNIQUE(title, company, location)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_jobs(self, jobs):
        """Save a list of Job objects to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        saved_count = 0
        for job in jobs:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO jobs 
                    (title, company, location, salary, url, keyword, search_location)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
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
    
    def get_all_jobs(self):
        """Get all jobs from the database."""
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
    
    def get_jobs_by_keyword(self, keyword):
        """Get jobs filtered by keyword."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM jobs WHERE keyword = ? ORDER BY scraped_date DESC', (keyword,))
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
    
    def get_stats(self):
        """Get database statistics."""
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
    
    def clear_database(self):
        """Clear all jobs from database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM jobs')
        conn.commit()
        conn.close()
        print("Database cleared")