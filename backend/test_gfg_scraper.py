"""Test GeeksforGeeks scraper with new URL"""
import requests
from bs4 import BeautifulSoup
import json

username = "sreenilay"
url = f"https://www.geeksforgeeks.org/profile/{username}/?tab=activity"

print(f"Testing URL: {url}\n")

try:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers, timeout=10)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Save HTML for inspection
        with open('gfg_page.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print("✓ HTML saved to gfg_page.html")
        
        # Try to find data in script tags (often contains JSON data)
        scripts = soup.find_all('script')
        print(f"\n✓ Found {len(scripts)} script tags")
        
        # Look for specific data patterns
        print("\n=== Looking for data patterns ===")
        
        # Check for coding score
        if 'Coding Score' in response.text:
            print("✓ Found 'Coding Score' text")
        
        if 'Problems Solved' in response.text:
            print("✓ Found 'Problems Solved' text")
            
        if 'Institute Rank' in response.text:
            print("✓ Found 'Institute Rank' text")
            
        if 'Articles Published' in response.text:
            print("✓ Found 'Articles Published' text")
            
        if 'Longest Streak' in response.text:
            print("✓ Found 'Longest Streak' text")
            
        if 'POTDs Solved' in response.text:
            print("✓ Found 'POTDs Solved' text")
        
        # Look for JSON data in scripts
        print("\n=== Checking for JSON data ===")
        for i, script in enumerate(scripts):
            script_text = script.string
            if script_text and ('codingScore' in script_text or 'problemsSolved' in script_text):
                print(f"✓ Found potential data in script tag {i}")
                # Print first 500 chars
                print(script_text[:500])
                break
        
        # Check for data attributes
        print("\n=== Checking for data attributes ===")
        elements_with_data = soup.find_all(attrs={'data-score': True})
        if elements_with_data:
            print(f"✓ Found {len(elements_with_data)} elements with data-score")
            
    else:
        print(f"✗ Failed to fetch page: {response.status_code}")
        
except Exception as e:
    print(f"✗ Error: {e}")
