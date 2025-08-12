from websites import Indeed, LinkedIn
from database import JobDatabase
import time

# Configuration data
keywords = [
    "software engineering intern summer 2026",
    "software developer intern summer 2026", 
    "computer science intern summer 2026",
    "backend developer intern summer 2026",
    "frontend developer intern summer 2026",
    "full stack developer intern summer 2026",
    "machine learning intern summer 2026",
    "AI intern summer 2026",
    "artificial intelligence intern summer 2026",
    "data science intern summer 2026",
    "cybersecurity intern summer 2026",
    "cyber security intern summer 2026",
    "information security intern summer 2026",
    "tech intern summer 2026",
    "programming intern summer 2026",
    "web developer intern summer 2026",
    "Bay Area intern summer 2026",
    "Silicon Valley intern summer 2026"
]

locations = [
    # Bay Area (within 50 miles)
    "Alameda, CA", "Belmont, CA", "Berkeley, CA", "Burlingame, CA",
    "Campbell, CA", "Cupertino, CA", "Daly City, CA", "Foster City, CA",
    "Fremont, CA", "Hayward, CA", "Los Gatos, CA", "Menlo Park, CA",
    "Millbrae, CA", "Milpitas, CA", "Mountain View, CA", "Oakland, CA",
    "Palo Alto, CA", "Redwood City, CA", "San Bruno, CA", "San Carlos, CA",
    "San Francisco, CA", "San Jose, CA", "San Mateo, CA", "Santa Clara, CA",
    "Saratoga, CA", "South San Francisco, CA", "Sunnyvale, CA", "Union City, CA",
    
    # Denver area (within 50 miles)
    "Arvada, CO", "Boulder, CO", "Broomfield, CO", "Denver, CO",
    "Golden, CO", "Lafayette, CO", "Lakewood, CO", "Longmont, CO",
    "Louisville, CO", "Thornton, CO", "Westminster, CO",
    
    # Broader searches
    "Denver Metro Area, CO", "San Francisco Bay Area, CA",
]

def main():
    # Initialize database
    db = JobDatabase("data/jobs.db")
    
    # Initialize scrapers
    indeed = Indeed()
    linkedin = LinkedIn()

    print("Starting job scraping...")
    print(f"Database location: data/jobs.db")
    print(f"Live webapp available at: http://localhost:8000")
    print(f"Start the server with: python run_server.py")
    
    # Ask user if they want to run full scrape
    print(f"\n Full scrape would run {len(keywords)} keywords × {len(locations)} locations = {len(keywords) * len(locations)} searches")
    
    run_full = input("Run full scrape? (y/N): ").lower().strip()
    
    if run_full == 'y' or run_full == 'yes':
        print(" Starting full scrape...")
        
        total_searches = len(keywords) * len(locations)
        current_search = 0
        
        for keyword in keywords:
            for location in locations:
                current_search += 1
                print(f"[{current_search}/{total_searches}] Searching: '{keyword}' in '{location}'")
                
                try:
                    jobs = linkedin.search(keyword, location)
                    if jobs:
                        saved_count = db.save_jobs(jobs)
                        print(f"Found {len(jobs)} jobs, saved {saved_count} new ones")
                    else:
                        print(f"No jobs found")
                except Exception as e:
                    print(f"Error: {e}")
                
                time.sleep(2)  # Wait 2 seconds between searches
    else:
        print("⏭Skipping full scrape")

    # Show final stats
    stats = db.get_stats()
    print(f"\n Final Database Stats:")
    print(f"Total jobs: {stats['total_jobs']}")
    print(f"Unique companies: {stats['unique_companies']}")
    print(f"Unique locations: {stats['unique_locations']}")
    
    print(f"\n Jobs saved to database!")
    print(f"View them live at: http://localhost:8000")
    print(f"Data updates automatically when you run this script again")

if __name__ == "__main__":
    main()