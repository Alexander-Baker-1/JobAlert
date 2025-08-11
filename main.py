import requests
from bs4 import BeautifulSoup

url = 'https://www.indeed.com'
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Charset': 'utf-8',
            'Upgrade-Insecure-Requests': '1',
          }

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

params = {
    'q': 'intern',
    'l': 'San Mateo, CA'
}

response = requests.get(url, params=params, headers=headers)

print(response.status_code)

soup = BeautifulSoup(response.content, 'html.parser')

print(soup.prettify())

# print(soup.prettify())

# content_div = soup.find('div', class_='article--viewer_content')
# if content_div:
#     for para in content_div.find_all('p'):
#         print(para.text.strip())
# else:
#     print("No article content found.")