import requests
import time
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
    
    def search(self, keyword, location):
        raise NotImplementedError("Subclass must implement search method")
    
    def parse_job(self, job_element):
        raise NotImplementedError("Subclass must implement parse_job method")
    
    def make_request(self, url, params=None):
        return requests.get(url, params=params, headers=self.headers)

class Indeed(Website):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.indeed.com/jobs"
    
    def search(self, keyword, location):
        time.sleep(2)
        params = {'q': keyword, 'l': location}
        response = self.make_request(self.base_url, params=params)
        print(response.status_code)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        jobs = soup.find_all('div', class_='job_seen_beacon')
        
        job_listings = []
        for job in jobs:
            job_data = self.parse_job(job, keyword, location)
            job_listings.append(job_data)
        
        return job_listings
    
    def parse_job(self, job_element, keyword, location):
        # Extract job title
        title_span = job_element.find('span', title=True)
        title = title_span.get('title') if title_span else 'No title'
        
        # Extract company
        company_span = job_element.find('span', {'data-testid': 'company-name'})
        company = company_span.text.strip() if company_span else 'No company'
        
        # Extract location
        location_div = job_element.find('div', {'data-testid': 'text-location'})
        location_text = location_div.text.strip() if location_div else 'No location'
        
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
        salary_h2 = job_element.find('h2', class_='mosaic-provider-jobcards-4n9q2y')
        if salary_h2:
            salary = salary_h2.text.strip()
            salary_span = job_element.find('span', class_='mosaic-provider-jobcards-140tz9m')
            if salary_span:
                salary += ' ' + salary_span.text.strip()
            return salary
        return 'No salary listed'
    
    def _get_job_url(self, job_element):
        link_a = job_element.find('a', class_='jcs-JobTitle')
        if link_a and link_a.get('href'):
            href = link_a.get('href')
            if href.startswith('/'):
                return "https://www.indeed.com" + href
            return href
        return 'No URL'

class LinkedIn(Website):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.linkedin.com/jobs/search"
    
    def search(self, keyword, location):
        # LinkedIn implementation
        pass