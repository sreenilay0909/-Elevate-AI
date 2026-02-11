"""Test GeeksforGeeks Practice API"""
import requests
import json

username = "sreenilay"

# Try practice API endpoints
endpoints = [
    f"https://practiceapi.geeksforgeeks.org/api/v1/user/{username}/",
    f"https://practiceapi.geeksforgeeks.org/api/user/{username}/",
    f"https://practiceapi.geeksforgeeks.org/api/vr/user/{username}/",
    f"https://practiceapi.geeksforgeeks.org/api/latest/user/{username}/",
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Referer': f'https://www.geeksforgeeks.org/profile/{username}/',
}

print(f"Testing Practice API for user: {username}\n")

for url in endpoints:
    print(f"Trying: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"  ✓ SUCCESS! Got JSON response")
                print(f"  Keys: {list(data.keys())}")
                
                # Save response
                with open('gfg_success_response.json', 'w') as f:
                    json.dump(data, f, indent=2)
                print(f"  ✓ Saved to gfg_success_response.json")
                
                # Print sample data
                print(f"\n  Sample data:")
                print(json.dumps(data, indent=2)[:500])
                break
            except json.JSONDecodeError:
                print(f"  ✗ Not JSON: {response.text[:100]}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    print()
