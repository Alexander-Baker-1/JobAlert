class Job:
    def __init__(self, title, company, location, salary, url, keyword, search_location):
        self.title = title
        self.company = company
        self.location = location
        self.salary = salary
        self.url = url
        self.keyword = keyword
        self.search_location = search_location
    
    def __str__(self):
        return f"{self.title} at {self.company} - {self.location}"
    
    def __repr__(self):
        return f"Job(title='{self.title}', company='{self.company}', location='{self.location}')"
    
    def to_dict(self):
        """Convert to dictionary for easy serialization"""
        return {
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'salary': self.salary,
            'url': self.url,
            'keyword': self.keyword,
            'search_location': self.search_location
        }
    
    def is_relevant(self):
        """Check if job is relevant based on keywords"""
        title_lower = self.title.lower()
        return any(keyword in title_lower for keyword in ['intern', '2026', 'summer'])