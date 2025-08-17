from websites import LinkedIn
from database import JobDatabase
import time
import schedule
from datetime import datetime

def run_daily_linkedin_scrape():
    """Run LinkedIn scraper for today's new postings only"""
    
    print(f"LinkedIn Daily Scrape - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize
    db = JobDatabase("data/jobs.db")
    linkedin = LinkedIn()
    
    # All search terms
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
    
    # Create all combinations
    searches = []
    for keyword in keywords:
        for location in locations:
            searches.append((keyword, location))
    
    print(f"Running {len(searches)} total searches (all combinations)")
    print(f"{len(keywords)} keywords x {len(locations)} locations")
    
    total_new = 0
    total_found = 0
    
    for i, (keyword, location) in enumerate(searches, 1):
        print(f"[{i}/{len(searches)}] {keyword} in {location}")
        
        try:
            # Only get new jobs
            jobs = linkedin.search(keyword, location)
            
            if jobs:
                saved_count = db.save_jobs(jobs)
                total_new += saved_count
                total_found += len(jobs)
                print(f"  Found {len(jobs)}, saved {saved_count} new")
            else:
                print(f"  No new jobs today")
                
        except Exception as e:
            print(f"  Error: {e}")
        
        time.sleep(3)  # Be nice to LinkedIn
    
    print(f"\nDaily scrape complete!")
    print(f"Found {total_found} jobs posted today")
    print(f"Added {total_new} new jobs to database")

def start_daily_scheduler():
    """Start the daily scheduler"""
    
    # Schedule for 9:00 AM every day
    schedule.every().day.at("09:00").do(run_daily_linkedin_scrape)
    
    print("Daily LinkedIn scraper scheduled for 9:00 AM")
    print("Scheduler running... Press Ctrl+C to stop")
    
    # Run once for testing
    print("Running test scrape now...")
    run_daily_linkedin_scrape()
    
    # Keep scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "now":
        # Run immediately
        run_daily_linkedin_scrape()
    else:
        # Start scheduler
        start_daily_scheduler()