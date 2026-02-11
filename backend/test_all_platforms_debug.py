"""Debug script to test all platform scrapers and see actual HTML"""
import subprocess
import json
import tempfile
import os

def test_gfg(username="sreenilay"):
    """Test GFG scraper and show HTML"""
    print(f"\n{'='*60}")
    print(f"TESTING GEEKSFORGEEKS: {username}")
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
        page.wait_for_timeout(5000)  # Wait longer
        content = page.content()
        browser.close()
        
        # Save HTML for debugging
        with open("gfg_debug.html", "w", encoding="utf-8") as f:
            f.write(content)
        
        # Try multiple extraction patterns
        print("\\n=== SEARCHING FOR STATS ===", file=sys.stderr)
        
        # Coding Score
        patterns = [
            r'Coding Score[^\\d]*(\\d+)',
            r'coding[_\\s-]?score[^\\d]*(\\d+)',
            r'score[^\\d]*(\\d+)',
        ]
        coding_score = 0
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                coding_score = int(match.group(1))
                print(f"Found Coding Score: {{coding_score}} with pattern: {{pattern}}", file=sys.stderr)
                break
        
        # Problems Solved
        patterns = [
            r'Problems Solved[^\\d]*(\\d+)',
            r'problems?[_\\s-]?solved[^\\d]*(\\d+)',
            r'solved[^\\d]*(\\d+)',
        ]
        problems = 0
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                problems = int(match.group(1))
                print(f"Found Problems: {{problems}} with pattern: {{pattern}}", file=sys.stderr)
                break
        
        # Institute Rank
        patterns = [
            r'Institute Rank[^\\d]*(\\d+)',
            r'institute[_\\s-]?rank[^\\d]*(\\d+)',
            r'rank[^\\d]*(\\d+)',
        ]
        rank = 0
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                rank = int(match.group(1))
                print(f"Found Rank: {{rank}} with pattern: {{pattern}}", file=sys.stderr)
                break
        
        data = {{
            'coding_score': coding_score,
            'problems_solved': problems,
            'institute_rank': rank,
            'articles_published': 0,
            'longest_streak': 0,
            'potds_solved': 0,
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
        
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            print(f"\n✅ GFG Data: {json.dumps(data, indent=2)}")
        else:
            print(f"\n❌ GFG Failed: {result.stderr}")
    finally:
        try:
            os.unlink(script_path)
        except:
            pass

def test_codechef(username="sreenilay0909"):
    """Test CodeChef scraper"""
    print(f"\n{'='*60}")
    print(f"TESTING CODECHEF: {username}")
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
        page.wait_for_timeout(5000)
        content = page.content()
        browser.close()
        
        # Save HTML
        with open("codechef_debug.html", "w", encoding="utf-8") as f:
            f.write(content)
        
        print("\\n=== SEARCHING FOR STATS ===", file=sys.stderr)
        
        # Rating
        rating = 0
        rating_patterns = [
            r'rating[^\\d]*(\\d{{3,4}})',
            r'<div[^>]*rating[^>]*>(\\d+)',
            r'rating-number[^>]*>(\\d+)',
        ]
        for pattern in rating_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                rating = int(match.group(1))
                if rating > 100:
                    print(f"Found Rating: {{rating}} with pattern: {{pattern}}", file=sys.stderr)
                    break
        
        # Stars
        stars = 0
        if rating >= 2500: stars = 7
        elif rating >= 2200: stars = 6
        elif rating >= 1800: stars = 5
        elif rating >= 1600: stars = 4
        elif rating >= 1400: stars = 3
        elif rating >= 1200: stars = 2
        else: stars = 1 if rating > 0 else 0
        
        data = {{
            'current_rating': rating,
            'stars': stars,
            'problems_solved': 0,
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
        
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            print(f"\n✅ CodeChef Data: {json.dumps(data, indent=2)}")
        else:
            print(f"\n❌ CodeChef Failed: {result.stderr}")
    finally:
        try:
            os.unlink(script_path)
        except:
            pass

def test_devpost(username="sreenilay0908"):
    """Test DevPost scraper"""
    print(f"\n{'='*60}")
    print(f"TESTING DEVPOST: {username}")
    print(f"{'='*60}")
    
    script = f'''
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
        page.set_viewport_size({{"width": 1920, "height": 1080}})
        page.goto(url, wait_until='networkidle', timeout=30000)
        page.wait_for_timeout(5000)
        content = page.content()
        browser.close()
        
        # Save HTML
        with open("devpost_debug.html", "w", encoding="utf-8") as f:
            f.write(content)
        
        print("\\n=== SEARCHING FOR STATS ===", file=sys.stderr)
        
        # Projects
        projects = 0
        patterns = [
            r'(\\d+)\\s*projects?',
            r'projects[^\\d]*(\\d+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                projects = int(match.group(1))
                print(f"Found Projects: {{projects}} with pattern: {{pattern}}", file=sys.stderr)
                break
        
        data = {{
            'projects_submitted': projects,
            'hackathons_participated': 0,
            'prizes_won': 0,
            'followers': 0,
            'likes_received': 0,
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
        
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            data = json.dumps(json.loads(result.stdout), indent=2)
            print(f"\n✅ DevPost Data: {data}")
        else:
            print(f"\n❌ DevPost Failed: {result.stderr}")
    finally:
        try:
            os.unlink(script_path)
        except:
            pass

if __name__ == "__main__":
    print("\\n" + "="*60)
    print("PLATFORM SCRAPER DEBUG TEST")
    print("="*60)
    
    test_gfg("sreenilay")
    test_codechef("sreenilay0909")
    test_devpost("sreenilay0908")
    
    print("\\n" + "="*60)
    print("CHECK THE HTML FILES:")
    print("- gfg_debug.html")
    print("- codechef_debug.html")
    print("- devpost_debug.html")
    print("="*60)
