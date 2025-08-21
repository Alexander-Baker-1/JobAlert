from websites import LinkedIn
from database import JobDatabase
import time
import schedule
from datetime import datetime

def run_daily_dual_scrape():
    """Run LinkedIn scrapers for today's new postings"""
    
    print(f"Daily Dual Scrape (LinkedIn) - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
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
    
    print(f"Running {len(searches)} total searches per platform")
    print(f"{len(keywords)} keywords x {len(locations)} locations")
    
    # Track totals for both platforms
    linkedin_total_new = 0
    linkedin_total_found = 0
    
    for i, (keyword, location) in enumerate(searches, 1):
        print(f"\n[{i}/{len(searches)}] {keyword} in {location}")
        
        # LinkedIn scraping
        try:
            print("  LinkedIn:", end=" ")
            linkedin_jobs = linkedin.search(keyword, location)
            
            if linkedin_jobs:
                saved_count = db.save_jobs(linkedin_jobs)
                linkedin_total_new += saved_count
                linkedin_total_found += len(linkedin_jobs)
                print(f"Found {len(linkedin_jobs)}, saved {saved_count} new")
            else:
                print("No jobs found")
                
        except Exception as e:
            print(f"Error - {e}")
        
        # Longer break between search combinations to be respectful
        if i < len(searches):  # Don't wait after the last search
            time.sleep(5)
    
    print(f"\n" + "="*50)
    print(f"DAILY SCRAPE COMPLETE!")
    print(f"="*50)
    print(f"LinkedIn Results:")
    print(f"  Found: {linkedin_total_found} jobs")
    print(f"  Saved: {linkedin_total_new} new jobs")
    print(f"Combined Total:")
    print(f"  Found: {linkedin_total_found} jobs")
    print(f"  Saved: {linkedin_total_new} new jobs")

def run_linkedin_only():
    """Run only LinkedIn scraper"""
    
    print(f"LinkedIn-Only Scrape - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize
    db = JobDatabase("data/jobs.db")
    linkedin = LinkedIn()
    
    # Same keywords and locations as above
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
        "Alameda, CA", "Belmont, CA", "Berkeley, CA", "Burlingame, CA",
        "Campbell, CA", "Cupertino, CA", "Daly City, CA", "Foster City, CA",
        "Fremont, CA", "Hayward, CA", "Los Gatos, CA", "Menlo Park, CA",
        "Millbrae, CA", "Milpitas, CA", "Mountain View, CA", "Oakland, CA",
        "Palo Alto, CA", "Redwood City, CA", "San Bruno, CA", "San Carlos, CA",
        "San Francisco, CA", "San Jose, CA", "San Mateo, CA", "Santa Clara, CA",
        "Saratoga, CA", "South San Francisco, CA", "Sunnyvale, CA", "Union City, CA",
        "Arvada, CO", "Boulder, CO", "Broomfield, CO", "Denver, CO",
        "Golden, CO", "Lafayette, CO", "Lakewood, CO", "Longmont, CO",
        "Louisville, CO", "Thornton, CO", "Westminster, CO",
        "Denver Metro Area, CO", "San Francisco Bay Area, CA",
    ]
    
    searches = []
    for keyword in keywords:
        for location in locations:
            searches.append((keyword, location))
    
    total_new = 0
    total_found = 0
    
    for i, (keyword, location) in enumerate(searches, 1):
        print(f"[{i}/{len(searches)}] {keyword} in {location}")
        
        try:
            jobs = linkedin.search(keyword, location)
            
            if jobs:
                saved_count = db.save_jobs(jobs)
                total_new += saved_count
                total_found += len(jobs)
                print(f"  Found {len(jobs)}, saved {saved_count} new")
            else:
                print(f"  No jobs found")
                
        except Exception as e:
            print(f"  Error: {e}")
        
        time.sleep(3)
    
    print(f"\nLinkedIn-only scrape complete!")
    print(f"Found {total_found} jobs")
    print(f"Added {total_new} new jobs to database")

def start_daily_scheduler():
    """Start the daily scheduler"""
    
    # Schedule for 9:00 AM every day
    schedule.every().day.at("09:00").do(run_daily_dual_scrape)
    
    print("Daily dual scraper scheduled for 9:00 AM")
    print("Scheduler running... Press Ctrl+C to stop")
    
    # Run once for testing
    print("Running test scrape now...")
    run_daily_dual_scrape()
    
    # Keep scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "now":
            # Run dual scraper immediately
            run_daily_dual_scrape()
        elif sys.argv[1] == "linkedin":
            # Run LinkedIn only
            run_linkedin_only()
        elif sys.argv[1] == "test":
            # Quick test with just a few searches
            print("Running quick test...")
            db = JobDatabase("data/jobs.db")
            linkedin = LinkedIn()
            
            test_searches = [
                ("software engineer intern", "San Francisco, CA"),
                ("data science intern", "Denver, CO")
            ]
            
            for keyword, location in test_searches:
                print(f"\nTesting: {keyword} in {location}")
                
                try:
                    linkedin_jobs = linkedin.search(keyword, location)
                    print(f"LinkedIn: {len(linkedin_jobs) if linkedin_jobs else 0} jobs")
                except Exception as e:
                    print(f"LinkedIn error: {e}")
                
                time.sleep(5)
        else:
            print("Usage: python script.py [now|linkedin|test]")
    else:
        # Start scheduler
        start_daily_scheduler()