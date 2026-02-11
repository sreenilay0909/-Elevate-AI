"""Test Playwright scrapers"""
import sys
sys.path.insert(0, '.')

from app.services.playwright_scrapers import PlaywrightGFGScraper, PlaywrightCodeChefScraper

print("="*60)
print("Testing GeeksforGeeks with Playwright")
print("="*60)

try:
    data = PlaywrightGFGScraper.fetch_user_data("sreenilay")
    print("✓ SUCCESS!")
    print(f"Data: {data}")
    print(f"\nCoding Score: {data['coding_score']}")
    print(f"Problems Solved: {data['problems_solved']}")
    print(f"Institute Rank: {data['institute_rank']}")
    print(f"Articles Published: {data['articles_published']}")
    print(f"Longest Streak: {data['longest_streak']}")
    print(f"POTDs Solved: {data['potds_solved']}")
except Exception as e:
    print(f"✗ FAILED: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("Testing CodeChef with Playwright")
print("="*60)

try:
    data = PlaywrightCodeChefScraper.fetch_user_data("sreenilay")
    print("✓ SUCCESS!")
    print(f"Data: {data}")
    print(f"\nRating: {data['current_rating']}")
    print(f"Stars: {data['stars']}")
    print(f"Problems Solved: {data['problems_solved']}")
    print(f"Contests: {data['contests_participated']}")
    print(f"Global Rank: {data['global_rank']}")
    print(f"Country Rank: {data['country_rank']}")
except Exception as e:
    print(f"✗ FAILED: {e}")
    import traceback
    traceback.print_exc()
