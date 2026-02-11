"""Test GeeksforGeeks with Selenium to render JavaScript"""
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    import time
    
    username = "sreenilay"
    url = f"https://www.geeksforgeeks.org/profile/{username}/?tab=activity"
    
    print(f"Testing URL with Selenium: {url}\n")
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Create driver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(url)
        print("✓ Page loaded")
        
        # Wait for content to load
        time.sleep(3)
        
        # Get page source after JavaScript execution
        page_source = driver.page_source
        
        # Check for data
        print("\n=== Checking for data ===")
        if 'Coding Score' in page_source:
            print("✓ Found 'Coding Score'")
        if 'Problems Solved' in page_source:
            print("✓ Found 'Problems Solved'")
        if 'Institute Rank' in page_source:
            print("✓ Found 'Institute Rank'")
        if 'Articles Published' in page_source:
            print("✓ Found 'Articles Published'")
        if 'Longest Streak' in page_source:
            print("✓ Found 'Longest Streak'")
        if 'POTDs Solved' in page_source:
            print("✓ Found 'POTDs Solved'")
        
        # Try to find specific elements
        print("\n=== Looking for specific elements ===")
        
        # Save rendered HTML
        with open('gfg_rendered.html', 'w', encoding='utf-8') as f:
            f.write(page_source)
        print("✓ Rendered HTML saved to gfg_rendered.html")
        
    finally:
        driver.quit()
        
except ImportError:
    print("✗ Selenium not installed")
    print("Install with: pip install selenium")
    print("\nAlternative: Let's try to find the API endpoint instead")
except Exception as e:
    print(f"✗ Error: {e}")
