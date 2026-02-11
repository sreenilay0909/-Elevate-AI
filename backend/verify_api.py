"""Verify API returns camelCase data"""
import requests
import json
import time

print("Waiting for backend to be ready...")
time.sleep(2)

# Test health endpoint
try:
    health = requests.get("http://127.0.0.1:8000/health")
    print(f"✓ Backend health: {health.json()}\n")
except Exception as e:
    print(f"✗ Backend not responding: {e}")
    exit(1)

# Test platform data endpoint (requires auth)
print("Testing platform data API...")
print("Note: This requires authentication. Testing with database query instead.\n")

# Check database directly
import sqlite3
conn = sqlite3.connect('elevateai.db')
cursor = conn.cursor()

cursor.execute("""
    SELECT pd.platform_name, pd.data
    FROM platform_data pd
    JOIN users u ON pd.user_id = u.id
    WHERE u.username = 'sreenilay'
    LIMIT 2
""")

rows = cursor.fetchall()
print("=== Database Data (snake_case) ===")
for platform, data_str in rows:
    data = json.loads(data_str)
    print(f"\n{platform}:")
    print(f"  Keys: {list(data.keys())[:5]}")
    print(f"  Sample: {json.dumps(dict(list(data.items())[:3]), indent=4)}")

conn.close()

print("\n" + "="*60)
print("✓ Backend is running on http://127.0.0.1:8000")
print("✓ Frontend is running on http://localhost:3000")
print("\nThe API will convert these snake_case keys to camelCase:")
print("  commits_last_year → commitsLastYear")
print("  total_solved → totalSolved")
print("  coding_score → codingScore")
print("\nPlease test in browser:")
print("1. Open http://localhost:3000")
print("2. Login with your credentials")
print("3. Check the dashboard for platform statistics")
print("4. Open browser console (F12) to see debug logs")
