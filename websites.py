import requests
import time
from bs4 import BeautifulSoup

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
        self.base_url = "https://www.indeed.com/jobs"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Charset': 'utf-8',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def search(self, keyword, location):
        # Build URL and make request
        time.sleep(2)
        params = {'q': keyword, 'l': location}
        response = requests.get(self.base_url, params=params, headers=self.headers)
        
        # DEBUG: Check if request worked
        print(response.status_code)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # DEBUG: See the HTML structure
        # print(soup.prettify())
        
        # TODO: Find job elements and return them
        return []
    
    def parse_job(self, job_element):
        # Indeed-specific parsing
        pass

class LinkedIn(Website):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.linkedin.com/jobs/search"
        # LinkedIn-specific setup
    
    def search(self, keyword, location):
        # LinkedIn implementation
        pass

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
    "Alameda, CA",
    "Belmont, CA",
    "Berkeley, CA",
    "Burlingame, CA",
    "Campbell, CA",
    "Cupertino, CA",
    "Daly City, CA",
    "Foster City, CA",
    "Fremont, CA",
    "Hayward, CA",
    "Los Gatos, CA",
    "Menlo Park, CA",
    "Millbrae, CA",
    "Milpitas, CA",
    "Mountain View, CA",
    "Oakland, CA",
    "Palo Alto, CA",
    "Redwood City, CA",
    "San Bruno, CA",
    "San Carlos, CA",
    "San Francisco, CA",
    "San Jose, CA",
    "San Mateo, CA",
    "Santa Clara, CA",
    "Saratoga, CA",
    "South San Francisco, CA",
    "Sunnyvale, CA",
    "Union City, CA",
    
    # Denver area (within 50 miles)
    "Arvada, CO",
    "Boulder, CO",
    "Broomfield, CO",
    "Denver, CO",
    "Golden, CO",
    "Lafayette, CO",
    "Lakewood, CO",
    "Longmont, CO",
    "Louisville, CO",
    "Thornton, CO",
    "Westminster, CO",
    
    # Broader searches
    "Denver Metro Area, CO"
    "San Francisco Bay Area, CA",
]