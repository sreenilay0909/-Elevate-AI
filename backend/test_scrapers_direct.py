"""Test scrapers directly"""
import sys
sys.path.insert(0, '.')

from app.services.platform_service_updated import GeeksforGeeksService, CodeChefService

print("="*60)
print("Testing GeeksforGeeks Scraper")
print("="*60)

gfg = GeeksforGeeksService()
try:
    data = gfg.fetch_user_data("sreenilay")
    print("✓ SUCCESS!")
    print(f"Data: {data}")
except Exception as e:
    print(f"✗ FAILED: {e}")

print("\n" + "="*60)
print("Testing CodeChef Scraper")
print("="*60)

# Try with a known CodeChef username
codechef = CodeChefService()
try:
    # First try with your username if you have one
    data = codechef.fetch_user_data("sreenilay")
    print("✓ SUCCESS!")
    print(f"Data: {data}")
except Exception as e:
    print(f"✗ FAILED: {e}")
    print("\nTrying with a known public username...")
    try:
        data = codechef.fetch_user_data("gennady.korotkevich")
        print("✓ SUCCESS with test user!")
        print(f"Data: {data}")
    except Exception as e2:
        print(f"✗ Also failed: {e2}")
