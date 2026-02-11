"""Test user search functionality"""
import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_search():
    """Test user search endpoint"""
    
    print("=" * 60)
    print("Testing User Search Functionality")
    print("=" * 60)
    
    # Test 1: Search with short query (should return empty)
    print("\n1. Testing short query (< 2 chars)...")
    response = requests.get(f"{BASE_URL}/profiles/search/users", params={"q": "s"})
    if response.status_code == 200:
        results = response.json()
        print(f"✓ Short query handled correctly: {len(results)} results")
    else:
        print(f"❌ Failed: {response.text}")
    
    # Test 2: Search for existing user
    print("\n2. Searching for 'sree'...")
    response = requests.get(f"{BASE_URL}/profiles/search/users", params={"q": "sree"})
    if response.status_code == 200:
        results = response.json()
        print(f"✓ Found {len(results)} user(s)")
        for user in results:
            print(f"   - @{user['username']}: {user['name']}")
            if user.get('fullName'):
                print(f"     Full Name: {user['fullName']}")
            if user.get('collegeName'):
                print(f"     College: {user['collegeName']}")
    else:
        print(f"❌ Failed: {response.text}")
    
    # Test 3: Search for non-existent user
    print("\n3. Searching for non-existent user...")
    response = requests.get(f"{BASE_URL}/profiles/search/users", params={"q": "nonexistentuser12345"})
    if response.status_code == 200:
        results = response.json()
        print(f"✓ No results found (expected): {len(results)} results")
    else:
        print(f"❌ Failed: {response.text}")
    
    # Test 4: Search with limit
    print("\n4. Testing search with limit=3...")
    response = requests.get(f"{BASE_URL}/profiles/search/users", params={"q": "a", "limit": 3})
    if response.status_code == 200:
        results = response.json()
        print(f"✓ Limited results: {len(results)} results (max 3)")
        for user in results:
            print(f"   - @{user['username']}")
    else:
        print(f"❌ Failed: {response.text}")
    
    print("\n" + "=" * 60)
    print("✅ All search tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    test_search()
