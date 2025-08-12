from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from urllib.parse import urlparse
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
        else:
            self.send_error(404)
    
    def serve_html(self):
        """Serve the main HTML page"""
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Live Job Listings</title>
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
            max-width: 1200px;
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

        .refresh-btn {
            background: rgba(255,255,255,0.2);
            color: white;
            border: 1px solid rgba(255,255,255,0.3);
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            margin: 10px;
            transition: background 0.3s;
        }

        .refresh-btn:hover {
            background: rgba(255,255,255,0.3);
        }

        .stats {
            display: flex;
            justify-content: center;
            gap: 30px;
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
            min-width: 150px;
        }

        .stat-number {
            font-size: 2rem;
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
        }

        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            display: inline-block;
            text-align: center;
        }

        .btn-primary {
            background: #667eea;
            color: white;
        }

        .btn-primary:hover {
            background: #5a6fd8;
            transform: translateY(-1px);
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
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Live Job Listings Dashboard</h1>
            <p>Real-time data from your database</p>
            <button class="refresh-btn" onclick="loadJobs()">🔄 Refresh</button>
        </div>

        <div class="last-updated">
            Last updated: <span id="lastUpdated">Loading...</span>
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-number" id="totalJobs">-</div>
                <div>Total Jobs</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="uniqueCompanies">-</div>
                <div>Companies</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="uniqueLocations">-</div>
                <div>Locations</div>
            </div>
        </div>

        <div class="jobs-grid" id="jobsContainer">
            <div class="loading">Loading jobs...</div>
        </div>
    </div>

    <script>
        async function loadJobs() {
            try {
                const response = await fetch('/api/jobs');
                const jobs = await response.json();
                
                renderJobs(jobs);
                updateLastUpdated();
                loadStats();
            } catch (error) {
                console.error('Error loading jobs:', error);
                document.getElementById('jobsContainer').innerHTML = 
                    '<div class="loading">Error loading jobs. Make sure your scraper has run!</div>';
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

        function renderJobs(jobs) {
            const container = document.getElementById('jobsContainer');
            
            if (jobs.length === 0) {
                container.innerHTML = '<div class="loading">No jobs found. Run your scraper first!</div>';
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
                    </div>
                </div>
            `).join('');
        }

        function updateLastUpdated() {
            const now = new Date();
            document.getElementById('lastUpdated').textContent = now.toLocaleString();
        }

        // Auto-refresh every 30 seconds
        setInterval(loadJobs, 30000);

        // Load initial data
        loadJobs();
    </script>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def serve_jobs_api(self):
        """Serve jobs data as JSON API"""
        try:
            db = JobDatabase("data/jobs.db")
            jobs = db.get_all_jobs()
            
            jobs_data = []
            for job in jobs:
                jobs_data.append({
                    'title': job.title,
                    'company': job.company,
                    'location': job.location,
                    'salary': job.salary,
                    'url': job.url
                })
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(jobs_data).encode())
            
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

def start_server(port=8000):
    """Start the web server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, JobWebHandler)
    
    print(f"Job listings server starting on http://localhost:{port}")
    print(f"View your jobs at: http://localhost:{port}")
    print(f"Data updates automatically from your database")
    print(f"Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\nServer stopped")
        httpd.server_close()

if __name__ == "__main__":
    start_server()