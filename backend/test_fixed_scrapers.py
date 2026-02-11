"""Test the fixed GFG and CodeChef scrapers"""
import subprocess
import json
import tempfile
import os

def test_gfg_fixed(username="sreenilay"):
    """Test fixed GFG scraper"""
    print(f"\n{'='*60}")
    print(f"TESTING FIXED GEEKSFORGEEKS SCRAPER")
    print(f"{'='*60}")
    
    script = f'''
import sys
import json
from playwright.sync_api import sync_playwright
import re

username = "{username}"
url = f"https://www.geeksforgeeks.org/profile/{{username}}/?tab=activity"

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({{"width": 1920, "height": 1080}})
        page.goto(url, wait_until='networkidle', timeout=30000)
        page.wait_for_timeout(3000)
        content = page.content()
        browser.close()
        
        def extract_stat(patterns, default=0):
            if isinstance(patterns, str):
                patterns = [patterns]
            for pattern in patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    value = match.group(1).replace(',', '')
                    try:
                        return int(value)
                    except:
                        pass
            return default
        
        data = {{
            'coding_score': extract_stat([
                r'Coding Score[^\\d]*(\\d+)',
                r'coding[_\\s-]?score[^\\d]*(\\d+)',
            ]),
            'problems_solved': extract_stat([
                r'Problems Solved[^\\d]*(\\d+)',
                r'problems?[_\\s-]?solved[^\\d]*(\\d+)',
            ]),
            'institute_rank': extract_stat([
                r'Institute Rank[^\\d]*(\\d+)',
                r'institute[_\\s-]?rank[^\\d]*(\\d+)',
            ]),
            'articles_published': extract_stat([
                r'Articles Published[^\\d]*(\\d+)',
                r'articles?[_\\s-]?published[^\\d]*(\\d+)',
                r'(\\d+)\\s*articles?',
            ]),
            'longest_streak': extract_stat([
                r'Longest Streak[^\\d]*(\\d+)',
                r'longest[_\\s-]?streak[^\\d]*(\\d+)',
                r'streak[^\\d]*(\\d+)\\s*days?',
            ]),
            'potds_solved': extract_stat([
                r'POTDs Solved[^\\d]*(\\d+)',
                r'potds?[_\\s-]?solved[^\\d]*(\\d+)',
                r'(\\d+)\\s*potds?',
            ]),
        }}
        
        print(json.dumps(data))
except Exception as e:
    print(json.dumps({{"error": str(e)}}), file=sys.stderr)
    sys.exit(1)
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(script)
        script_path = f.name
    
    try:
        result = subprocess.run(
            ['python', script_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            print(f"\n✅ GFG Data:")
            print(f"   Coding Score: {data['coding_score']}")
            print(f"   Problems Solved: {data['problems_solved']}")
            print(f"   Institute Rank: {data['institute_rank']}")
            print(f"   Articles Published: {data['articles_published']} {'✅' if data['articles_published'] > 0 else '❌ (still 0)'}")
            print(f"   Longest Streak: {data['longest_streak']} {'✅' if data['longest_streak'] > 0 else '❌ (still 0)'}")
            print(f"   POTDs Solved: {data['potds_solved']} {'✅' if data['potds_solved'] > 0 else '❌ (still 0)'}")
        else:
            print(f"\n❌ GFG Failed: {result.stderr}")
    finally:
        try:
            os.unlink(script_path)
        except:
            pass

def test_codechef_fixed(username="sreenilay0909"):
    """Test fixed CodeChef scraper"""
    print(f"\n{'='*60}")
    print(f"TESTING FIXED CODECHEF SCRAPER")
    print(f"{'='*60}")
    
    script = f'''
import sys
import json
from playwright.sync_api import sync_playwright
import re

username = "{username}"
url = f"https://www.codechef.com/users/{{username}}"

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({{"width": 1920, "height": 1080}})
        page.goto(url, wait_until='networkidle', timeout=30000)
        page.wait_for_timeout(3000)
        content = page.content()
        browser.close()
        
        # Extract rating
        rating = 0
        rating_patterns = [
            r'rating.*?(\\d{{3,4}})',
            r'<div[^>]*rating[^>]*>(\\d+)',
            r'rating-number[^>]*>(\\d+)',
        ]
        for pattern in rating_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                rating = int(match.group(1))
                if rating > 100:
                    break
        
        # Calculate stars
        if rating >= 2500: stars = 7
        elif rating >= 2200: stars = 6
        elif rating >= 1800: stars = 5
        elif rating >= 1600: stars = 4
        elif rating >= 1400: stars = 3
        elif rating >= 1200: stars = 2
        else: stars = 1 if rating > 0 else 0
        
        # Extract problems solved - NEW PATTERNS
        problems_solved = 0
        problems_patterns = [
            r'Total Problems Solved:\\s*(\\d+)',
            r'(\\d+)\\s*problems?\\s*solved',
            r'problems?\\s*solved[^\\d]*(\\d+)',
        ]
        for pattern in problems_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                problems_solved = int(match.group(1))
                break
        
        data = {{
            'current_rating': rating,
            'stars': stars,
            'problems_solved': problems_solved,
            'contests_participated': 0,
            'global_rank': 0,
            'country_rank': 0,
        }}
        
        print(json.dumps(data))
except Exception as e:
    print(json.dumps({{"error": str(e)}}), file=sys.stderr)
    sys.exit(1)
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(script)
        script_path = f.name
    
    try:
        result = subprocess.run(
            ['python', script_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            print(f"\n✅ CodeChef Data:")
            print(f"   Rating: {data['current_rating']}")
            print(f"   Stars: {data['stars']}★")
            print(f"   Problems Solved: {data['problems_solved']} {'✅ (should be 34)' if data['problems_solved'] > 0 else '❌ (still 0)'}")
            print(f"   Contests: {data['contests_participated']}")
        else:
            print(f"\n❌ CodeChef Failed: {result.stderr}")
    finally:
        try:
            os.unlink(script_path)
        except:
            pass

if __name__ == "__main__":
    print("\n" + "="*60)
    print("TESTING FIXED SCRAPERS")
    print("="*60)
    
    test_gfg_fixed("sreenilay")
    test_codechef_fixed("sreenilay0909")
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("\nIf GFG shows Articles/Streak/POTDs > 0: ✅ Fixed!")
    print("If CodeChef shows Problems Solved = 34: ✅ Fixed!")
    print("\nIf still showing 0s, the data might not be on the page.")
    print("="*60)
