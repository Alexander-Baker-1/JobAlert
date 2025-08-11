import requests
import time
from bs4 import BeautifulSoup
from job import Job

class Website:
    def __init__(self):
        self.base_url = ""
        self.headers = {}
    
    def search(self, keyword, location):
        # Base method that all sites must implement
        raise NotImplementedError("Subclass must implement search method")
    
    def parse_job(self, job_element):
        # Base parsing method
        raise NotImplementedError("Subclass must implement parse_job method")
    
    def make_request(self, url):
        # Common request logic all sites can use
        import requests
        return requests.get(url, headers=self.headers)

class Indeed(Website):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.indeed.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Charset': 'utf-8',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def search(self, keyword, location):
        time.sleep(2)
        params = {'q': keyword, 'l': location}
        response = requests.get(self.base_url, params=params, headers=self.headers)
        print(response.status_code)
        soup = BeautifulSoup(response.content, 'html.parser')
        jobs = soup.find_all('div', class_='job_seen_beacon')
        
        job_listings = []
        for job in jobs:
            job_data = self.parse_job(job, keyword, location)
            job_listings.append(job_data)
        
        return job_listings
    
    def parse_job(self, job_element, keyword, location):
        # Initialize defaults
        title = 'No title'
        company = 'No company'
        location_text = 'No location'
        salary = 'No salary listed'
        job_url = 'No URL'
        
        # Extract job title
        title_span = job_element.find('span', title=True)
        if title_span:
            title = title_span.get('title')
        
        # Extract company
        company_span = job_element.find('span', {'data-testid': 'company-name'})
        if company_span:
            company = company_span.text.strip()
        
        # Extract location
        location_div = job_element.find('div', {'data-testid': 'text-location'})
        if location_div:
            location_text = location_div.text.strip()
        
        # Extract salary
        salary_h2 = job_element.find('h2', class_='mosaic-provider-jobcards-4n9q2y')
        if salary_h2:
            salary = salary_h2.text.strip()
            salary_span = job_element.find('span', class_='mosaic-provider-jobcards-140tz9m')
            if salary_span:
                salary += ' ' + salary_span.text.strip()
        
        # Extract job URL
        link_a = job_element.find('a', class_='jcs-JobTitle')
        if link_a and link_a.get('href'):
            href = link_a.get('href')
            if href.startswith('/'):
                job_url = "https://www.indeed.com" + href
            else:
                job_url = href
        
        return Job(
            title=title,
            company=company,
            location=location_text,
            salary=salary,
            url=job_url,
            keyword=keyword,
            search_location=location
        )

class LinkedIn(Website):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.linkedin.com/jobs/search"
        # LinkedIn-specific setup
    
    def search(self, keyword, location):
        # LinkedIn implementation
        pass