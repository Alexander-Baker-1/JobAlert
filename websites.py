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
        self.base_url = "https://www.indeed.com"
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