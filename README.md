# Job Application Tracker

Automated job scraper with application tracking system for software engineering internships.

## Features

- Daily LinkedIn scraping with automated scheduling
- Indeed job scraping
- Live web interface for job management
- Status tracking (New, In Progress, Applied, Not Interested)
- Job notes and salary extraction
- SQLite database with duplicate prevention

## Current Configuration

This project is currently hardcoded for my personal job search preferences:
- Software engineering internship positions
- Summer 2026 timeframe
- Bay Area and Denver locations
- Specific keywords and location combinations

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Start the web server: `python run_server.py`
3. View jobs at: http://localhost:8000
4. Run daily scraper: `python simple_daily_runner.py now`

## File Structure

- `websites.py` - Indeed and LinkedIn scrapers
- `database.py` - SQLite database management
- `webapp_server.py` - Live web interface
- `simple_daily_runner.py` - Automated daily LinkedIn scraping
- `data/jobs.db` - Job database (auto-created)

## Automation

Set up Windows Task Scheduler to run:
- `python run_server.py` at startup (webapp server)
- `python simple_daily_runner.py now` daily at 9 AM (scraper)

## Future Plans

Additional job site integrations planned including Glassdoor, AngelList, and company career pages.

## Note

This is a personal project with hardcoded search parameters. Customize keywords and locations in the respective Python files for different job searches.