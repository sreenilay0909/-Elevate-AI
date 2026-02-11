"""Test CodeChef and DevPost scrapers"""
import subprocess
import json
import tempfile
import os

def test_codechef(username):
    print(f"\n{'='*60}")
    print(f"Testing CodeChef for: {username}")
    print('='*60)
    
    script = f"""
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
        page.goto(url, wait_until='networkidle', timeout=30000)
        page.wait_for_timeout(3000)
        content = page.content()
        
        # Save HTML for inspection
        with open('codechef_page.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Try multiple patterns for rating
        rating = 0
        rating_patterns = [
            r'rating["\']?\\s*:\\s*(\\d+)',
            r'rating-number[^>]*>(\\d+)',
            r'<div[^>]*rating[^>]*>(\\d+)',
        ]
        for pattern in rating_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                rating = int(match.group(1))
                break
        
        # Calculate stars
        if rating >= 2500: stars = 7
        elif rating >= 2200: stars = 6
        elif rating >= 1800: stars = 5
        elif rating >= 1600: stars = 4
        elif rating >= 1400: stars = 3
        elif rating >= 1200: stars = 2
        else: stars = 1 if rating > 0 else 0
        
        # Extract other stats
        problems_match = re.search(r'(\\d+)\\s*problems?\\s*solved', content, re.IGNORECASE)
        problems_solved = int(problems_match.group(1)) if problems_match else 0
        
        data = {{
            'current_rating': rating,
            'stars': stars,
            'problems_solved': problems_solved,
            'contests_participated': 0,
            'global_rank': 0,
            'country_rank': 0,
        }}
        
        browser.close()
        print(json.dumps(data))
except Exception as e:
    print(json.dumps({{"error": str(e)}}), file=sys.stderr)
    sys.exit(1)
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(script)
        script_path = f.name
    
    try:
        result = subprocess.run(['python', script_path], capture_output=True, text=True, timeout=40)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            print(f"✓ SUCCESS!")
            print(f"Rating: {data['current_rating']}")
            print(f"Stars: {data['stars']}")
            print(f"Problems Solved: {data['problems_solved']}")
        else:
            print(f"✗ FAILED: {result.stderr}")
    finally:
        try:
            os.unlink(script_path)
        except:
            pass

def test_devpost(username):
    print(f"\n{'='*60}")
    print(f"Testing DevPost for: {username}")
    print('='*60)
    
    script = f"""
import sys
import json
from playwright.sync_api import sync_playwright
import re

username = "{username}"
url = f"https://devpost.com/{{username}}"

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until='networkidle', timeout=30000)
        page.wait_for_timeout(3000)
        content = page.content()
        
        # Save HTML for inspection
        with open('devpost_page.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Extract stats
        projects_match = re.search(r'(\\d+)\\s*projects?', content, re.IGNORECASE)
        projects = int(projects_match.group(1)) if projects_match else 0
        
        hackathons_match = re.search(r'(\\d+)\\s*hackathons?', content, re.IGNORECASE)
        hackathons = int(hackathons_match.group(1)) if hackathons_match else 0
        
        prizes_match = re.search(r'(\\d+)\\s*prizes?', content, re.IGNORECASE)
        prizes = int(prizes_match.group(1)) if prizes_match else 0
        
        followers_match = re.search(r'(\\d+)\\s*followers?', content, re.IGNORECASE)
        followers = int(followers_match.group(1)) if followers_match else 0
        
        data = {{
            'projects_submitted': projects,
            'hackathons_participated': hackathons,
            'prizes_won': prizes,
            'followers': followers,
            'likes_received': 0,
        }}
        
        browser.close()
        print(json.dumps(data))
except Exception as e:
    print(json.dumps({{"error": str(e)}}), file=sys.stderr)
    sys.exit(1)
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(script)
        script_path = f.name
    
    try:
        result = subprocess.run(['python', script_path], capture_output=True, text=True, timeout=40)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            print(f"✓ SUCCESS!")
            print(f"Projects: {data['projects_submitted']}")
            print(f"Hackathons: {data['hackathons_participated']}")
            print(f"Prizes: {data['prizes_won']}")
            print(f"Followers: {data['followers']}")
        else:
            print(f"✗ FAILED: {result.stderr}")
    finally:
        try:
            os.unlink(script_path)
        except:
            pass

# Test with your usernames
test_codechef("sreenilay")
test_devpost("sreenilay")

print("\n" + "="*60)
print("Check codechef_page.html and devpost_page.html for HTML structure")
print("="*60)
