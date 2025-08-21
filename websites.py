import requests
import time
import random
from bs4 import BeautifulSoup
from job import Job

class Website:
    def __init__(self):
        self.base_url = ""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Charset': 'utf-8',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def search(self, keyword, location):
        raise NotImplementedError("Subclass must implement search method")
    
    def parse_job(self, job_element):
        raise NotImplementedError("Subclass must implement parse_job method")
    
    def make_request(self, url, params=None, custom_headers=None):
        if custom_headers:
            # Create a new session with updated headers
            temp_session = requests.Session()
            temp_session.headers.update(custom_headers)
            return temp_session.get(url, params=params)
        return self.session.get(url, params=params)

class LinkedIn(Website):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.linkedin.com/jobs/search"
    
    def search(self, keyword, location):
        params = {
            'keywords': keyword,
            'location': location,
            'f_TPR': 'r86400'  # Only jobs posted in last 24 hours
        }
        response = self.make_request(self.base_url, params=params)
        print(response.status_code)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        jobs = soup.find_all('div', class_='base-card')
        
        job_listings = []
        for job in jobs:
            job_data = self.parse_job(job, keyword, location)
            job_listings.append(job_data)
        
        return job_listings
    
    def parse_job(self, job_element, keyword, location):
        # Extract job title
        title_a = job_element.find('a', class_='base-card__full-link')
        title = title_a.get_text(strip=True) if title_a else 'No title'
        
        # Extract company
        company_a = job_element.find('a', {'data-tracking-control-name': 'public_jobs_jserp-result_job-search-card-subtitle'})
        company = company_a.get_text(strip=True) if company_a else 'No company'
        
        # Extract location
        location_span = job_element.find('span', class_='job-search-card__location')
        location_text = location_span.get_text(strip=True) if location_span else 'No location'
        
        # Extract salary
        salary = self._get_salary(job_element)

        # Extract job URL
        job_url = self._get_job_url(job_element)
        
        return Job(
            title=title,
            company=company,
            location=location_text,
            salary=salary,
            url=job_url,
            keyword=keyword,
            search_location=location
        )
    
    def _get_salary(self, job_element):
        # Try common LinkedIn salary selectors
        salary_span = job_element.find('span', class_='job-search-card__salary-info')
        if salary_span:
            return salary_span.get_text(strip=True)
        
        # Alternative LinkedIn selector
        salary_div = job_element.find('div', class_='result-benefits__text')
        if salary_div:
            return salary_div.get_text(strip=True)
        
        # Search for salary keywords in any text
        for element in job_element.find_all(text=True):
            text = element.strip().lower()
            if any(keyword in text for keyword in ['$', '/hr', '/year', 'salary', 'k-', 'k ']):
                parent_text = element.parent.get_text(strip=True) if element.parent else element
                if len(parent_text) < 50:  # Keep it short
                    return parent_text
        
        return 'No salary listed'
    
    def _get_job_url(self, job_element):
        link_a = job_element.find('a', class_='base-card__full-link')
        if link_a and link_a.get('href'):
            href = link_a.get('href')
            return href
        return 'No URL'