from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from urllib.parse import urlparse, parse_qs
from database import JobDatabase

class JobWebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        
        if path == '/' or path == '/index.html':
            self.serve_html()
        elif path == '/api/jobs':
            self.serve_jobs_api()
        elif path == '/api/stats':
            self.serve_stats_api()
        elif path == '/api/status-counts':
            self.serve_status_counts_api()
        else:
            self.send_error(404)
    
    def do_POST(self):
        path = urlparse(self.path).path
        
        if path == '/api/update-status':
            self.update_job_status()
        else:
            self.send_error(404)
    
    def serve_html(self):
        """Serve the main HTML page with job tracking"""
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Application Tracker</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
            color: white;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .tabs {
            display: flex;
            justify-content: center;
            margin-bottom: 30px;
            gap: 10px;
            flex-wrap: wrap;
        }

        .tab {
            background: rgba(255,255,255,0.2);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
            position: relative;
        }

        .tab:hover {
            background: rgba(255,255,255,0.3);
        }

        .tab.active {
            background: white;
            color: #667eea;
        }

        .tab-count {
            background: rgba(255,255,255,0.3);
            border-radius: 12px;
            padding: 2px 8px;
            margin-left: 8px;
            font-size: 0.8rem;
        }

        .tab.active .tab-count {
            background: #667eea;
            color: white;
        }

        .stats {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }

        .stat-card {
            background: rgba(255,255,255,0.1);
            -webkit-backdrop-filter: blur(10px);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            color: white;
            min-width: 120px;
        }

        .stat-number {
            font-size: 1.8rem;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .jobs-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 20px;
        }

        .job-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            border-left: 4px solid #667eea;
        }

        .job-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }

        .job-title {
            font-size: 1.3rem;
            font-weight: bold;
            color: #2d3748;
            margin-bottom: 10px;
            line-height: 1.3;
        }

        .job-company {
            font-size: 1.1rem;
            color: #667eea;
            font-weight: 600;
            margin-bottom: 8px;
        }

        .job-location {
            color: #718096;
            font-size: 0.95rem;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .job-location::before {
            content: "📍";
        }

        .job-salary {
            background: #f7fafc;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 0.9rem;
            color: #2d3748;
            margin-bottom: 15px;
            border: 1px solid #e2e8f0;
        }

        .job-actions {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .btn {
            padding: 8px 16px;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            display: inline-block;
            text-align: center;
            font-size: 0.85rem;
        }

        .btn-primary {
            background: #667eea;
            color: white;
        }

        .btn-success {
            background: #48bb78;
            color: white;
        }

        .btn-warning {
            background: #ed8936;
            color: white;
        }

        .btn-danger {
            background: #f56565;
            color: white;
        }

        .btn-secondary {
            background: #a0aec0;
            color: white;
        }

        .btn:hover {
            transform: translateY(-1px);
            opacity: 0.9;
        }

        .notes-section {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #e2e8f0;
        }

        .notes-textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #e2e8f0;
            border-radius: 5px;
            resize: vertical;
            min-height: 60px;
            font-size: 0.9rem;
        }

        .loading {
            text-align: center;
            color: white;
            font-size: 1.2rem;
            margin: 50px 0;
        }

        .last-updated {
            text-align: center;
            color: rgba(255,255,255,0.8);
            margin-bottom: 20px;
            font-size: 0.9rem;
        }

        @media (max-width: 768px) {
            .jobs-grid {
                grid-template-columns: 1fr;
            }
            
            .stats {
                flex-direction: column;
                align-items: center;
            }
            
            .tabs {
                flex-direction: column;
                align-items: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Job Application Tracker</h1>
            <p>Organize and track your job applications</p>
        </div>

        <div class="last-updated">
            Last updated: <span id="lastUpdated">Loading...</span>
        </div>

        <div class="tabs">
            <button class="tab active" data-status="new">
                New Jobs <span class="tab-count" id="newCount">0</span>
            </button>
            <button class="tab" data-status="in_progress">
                In Progress <span class="tab-count" id="inProgressCount">0</span>
            </button>
            <button class="tab" data-status="applied">
                Applied <span class="tab-count" id="appliedCount">0</span>
            </button>
            <button class="tab" data-status="not_interested">
                Not Interested <span class="tab-count" id="notInterestedCount">0</span>
            </button>
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-number" id="totalJobs">0</div>
                <div>Total Jobs</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="uniqueCompanies">0</div>
                <div>Companies</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="uniqueLocations">0</div>
                <div>Locations</div>
            </div>
        </div>

        <div class="jobs-grid" id="jobsContainer">
            <div class="loading">Loading jobs...</div>
        </div>
    </div>

    <script>
        let currentStatus = 'new';
        
        async function loadJobs(status = 'new') {
            try {
                const response = await fetch(`/api/jobs?status=${status}`);
                const jobs = await response.json();
                
                renderJobs(jobs, status);
                updateLastUpdated();
            } catch (error) {
                console.error('Error loading jobs:', error);
                document.getElementById('jobsContainer').innerHTML = 
                    '<div class="loading">Error loading jobs.</div>';
            }
        }

        async function loadStats() {
            try {
                const response = await fetch('/api/stats');
                const stats = await response.json();
                
                document.getElementById('totalJobs').textContent = stats.total_jobs;
                document.getElementById('uniqueCompanies').textContent = stats.unique_companies;
                document.getElementById('uniqueLocations').textContent = stats.unique_locations;
            } catch (error) {
                console.error('Error loading stats:', error);
            }
        }

        async function loadStatusCounts() {
            try {
                const response = await fetch('/api/status-counts');
                const counts = await response.json();
                
                document.getElementById('newCount').textContent = counts.new || 0;
                document.getElementById('inProgressCount').textContent = counts.in_progress || 0;
                document.getElementById('appliedCount').textContent = counts.applied || 0;
                document.getElementById('notInterestedCount').textContent = counts.not_interested || 0;
            } catch (error) {
                console.error('Error loading status counts:', error);
            }
        }

        function renderJobs(jobs, status) {
            const container = document.getElementById('jobsContainer');
            
            if (jobs.length === 0) {
                container.innerHTML = `<div class="loading">No ${status.replace('_', ' ')} jobs found.</div>`;
                return;
            }
            
            container.innerHTML = jobs.map(job => `
                <div class="job-card">
                    <div class="job-title">${job.title}</div>
                    <div class="job-company">${job.company}</div>
                    <div class="job-location">${job.location}</div>
                    <div class="job-salary">${job.salary || 'No salary listed'}</div>
                    
                    <div class="job-actions">
                        <a href="${job.url || '#'}" class="btn btn-primary" target="_blank">View Job</a>
                        ${getStatusButtons(job.id, job.status)}
                    </div>
                    
                    <div class="notes-section">
                        <textarea class="notes-textarea" placeholder="Add notes..." 
                                  onchange="updateNotes(${job.id}, this.value)">${job.notes || ''}</textarea>
                    </div>
                </div>
            `).join('');
        }

        function getStatusButtons(jobId, currentStatus) {
            const buttons = [];
            
            if (currentStatus !== 'in_progress') {
                buttons.push(`<button class="btn btn-warning" onclick="updateJobStatus(${jobId}, 'in_progress')">Mark In Progress</button>`);
            }
            
            if (currentStatus !== 'applied') {
                buttons.push(`<button class="btn btn-success" onclick="updateJobStatus(${jobId}, 'applied')">Mark Applied</button>`);
            }
            
            if (currentStatus !== 'not_interested') {
                buttons.push(`<button class="btn btn-danger" onclick="updateJobStatus(${jobId}, 'not_interested')">Not Interested</button>`);
            }
            
            if (currentStatus !== 'new') {
                buttons.push(`<button class="btn btn-secondary" onclick="updateJobStatus(${jobId}, 'new')">Mark as New</button>`);
            }
            
            return buttons.join('');
        }

        async function updateJobStatus(jobId, newStatus) {
            try {
                const response = await fetch('/api/update-status', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        job_id: jobId,
                        status: newStatus
                    })
                });
                
                if (response.ok) {
                    // Reload current view and update counts
                    loadJobs(currentStatus);
                    loadStatusCounts();
                } else {
                    alert('Failed to update job status');
                }
            } catch (error) {
                console.error('Error updating status:', error);
                alert('Error updating job status');
            }
        }

        async function updateNotes(jobId, notes) {
            try {
                await fetch('/api/update-status', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        job_id: jobId,
                        notes: notes
                    })
                });
            } catch (error) {
                console.error('Error updating notes:', error);
            }
        }

        function updateLastUpdated() {
            const now = new Date();
            document.getElementById('lastUpdated').textContent = now.toLocaleString();
        }

        // Tab switching
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => {
                // Update active tab
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                
                // Load jobs for selected status
                currentStatus = tab.dataset.status;
                loadJobs(currentStatus);
            });
        });

        // Auto-refresh every 60 seconds
        setInterval(() => {
            loadJobs(currentStatus);
            loadStatusCounts();
        }, 60000);

        // Load initial data
        loadJobs('new');
        loadStats();
        loadStatusCounts();
    </script>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def serve_jobs_api(self):
        """Serve jobs data as JSON API with status filtering"""
        try:
            query_params = parse_qs(urlparse(self.path).query)
            status = query_params.get('status', ['new'])[0]
            
            db = JobDatabase("data/jobs.db")
            jobs = db.get_jobs_by_status(status)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(jobs).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def serve_stats_api(self):
        """Serve stats data as JSON API"""
        try:
            db = JobDatabase("data/jobs.db")
            stats = db.get_stats()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(stats).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def serve_status_counts_api(self):
        """Serve status counts as JSON API"""
        try:
            db = JobDatabase("data/jobs.db")
            counts = db.get_status_counts()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(counts).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def update_job_status(self):
        """Update job status via POST request"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            job_id = data.get('job_id')
            new_status = data.get('status')
            notes = data.get('notes')
            
            db = JobDatabase("data/jobs.db")
            
            if new_status:
                success = db.update_job_status(job_id, new_status, notes)
            else:
                # Update notes
                success = db.update_job_status(job_id, None, notes)
            
            if success:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True}).encode())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Job not found'}).encode())
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

def start_server(port=8000):
    """Start the web server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, JobWebHandler)
    
    print(f"Job tracker server starting on http://localhost:{port}")
    print(f"View your jobs at: http://localhost:{port}")
    print(f"Track application progress with multiple status pages")
    print(f"Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\nServer stopped")
        httpd.server_close()

if __name__ == "__main__":
    start_server()