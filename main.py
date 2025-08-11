from websites import Indeed, LinkedIn
import time

# Configuration data
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
    "Denver Metro Area, CO",
    "San Francisco Bay Area, CA",
]

# Main execution
def main():
    indeed = Indeed()
    
    print(f"Searching for intern in Denver, CO")
    jobs = indeed.search("intern", "Denver, CO")

    # for keyword in keywords:
    #     for location in locations:
    #         print(f"Searching for '{keyword}' in '{location}'")
    #         jobs = indeed.search(keyword, location)
    #         time.sleep(2)  # Wait 2 seconds between searches
    #         # Process the jobs...

if __name__ == "__main__":
    main()