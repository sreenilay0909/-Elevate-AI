"""Test GeeksforGeeks scraper with Selenium"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

username = "sreenilay"
url = f"https://www.geeksforgeeks.org/profile/{username}/?tab=activity"

print(f"Testing GeeksforGeeks scraper for: {username}\n")

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

try:
    # Create driver with webdriver-manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    print("✓ Chrome driver initialized")
    
    # Load page
    driver.get(url)
    print(f"✓ Loaded URL: {url}")
    
    # Wait for page to load
    time.sleep(5)
    
    # Get page source
    page_source = driver.page_source
    
    print("\n=== Extracting Data ===\n")
    
    # Function to extract number from text
    def extract_number(text):
        if not text:
            return 0
        match = re.search(r'(\d+)', text.replace(',', ''))
        return int(match.group(1)) if match else 0
    
    # Try to find elements by text content
    data = {}
    
    # Method 1: Look for specific text patterns in page source
    patterns = {
        'coding_score': r'Coding Score[^\d]*(\d+)',
        'problems_solved': r'Problems Solved[^\d]*(\d+)',
        'institute_rank': r'Institute Rank[^\d]*(\d+)',
        'articles_published': r'Articles Published[^\d]*(\d+)',
        'longest_streak': r'Longest Streak[^\d]*(\d+)',
        'potds_solved': r'POTDs Solved[^\d]*(\d+)',
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, page_source, re.IGNORECASE)
        if match:
            data[key] = int(match.group(1))
            print(f"✓ {key}: {data[key]}")
        else:
            data[key] = 0
            print(f"✗ {key}: Not found")
    
    # Method 2: Try to find elements by class or ID
    try:
        # Look for score elements
        score_elements = driver.find_elements(By.CLASS_NAME, "score_card_value")
        if score_elements:
            print(f"\n✓ Found {len(score_elements)} score elements")
            for elem in score_elements:
                print(f"  - {elem.text}")
    except Exception as e:
        print(f"✗ Error finding score elements: {e}")
    
    # Save rendered HTML for inspection
    with open('gfg_selenium_rendered.html', 'w', encoding='utf-8') as f:
        f.write(page_source)
    print("\n✓ Rendered HTML saved to gfg_selenium_rendered.html")
    
    # Print summary
    print("\n=== Summary ===")
    print(f"Coding Score: {data.get('coding_score', 0)}")
    print(f"Problems Solved: {data.get('problems_solved', 0)}")
    print(f"Institute Rank: {data.get('institute_rank', 0)}")
    print(f"Articles Published: {data.get('articles_published', 0)}")
    print(f"Longest Streak: {data.get('longest_streak', 0)}")
    print(f"POTDs Solved: {data.get('potds_solved', 0)}")
    
    driver.quit()
    print("\n✓ Test complete!")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
