"""Check platform data in database"""
import sqlite3
import json

conn = sqlite3.connect('elevateai.db')
cursor = conn.cursor()

cursor.execute("""
    SELECT pd.id, u.username, pd.platform_name, pd.data, 
           pd.last_updated, pd.update_status, pd.error_message
    FROM platform_data pd
    JOIN users u ON pd.user_id = u.id
""")

data = cursor.fetchall()

print("=== Platform Data in Database ===\n")
if not data:
    print("No platform data found!")
else:
    for row in data:
        print(f"ID: {row[0]}")
        print(f"User: {row[1]}")
        print(f"Platform: {row[2]}")
        print(f"Data: {row[3][:200] if row[3] else 'None'}...")  # First 200 chars
        print(f"Last Updated: {row[4]}")
        print(f"Status: {row[5]}")
        print(f"Error: {row[6]}")
        print("-" * 50)

conn.close()
