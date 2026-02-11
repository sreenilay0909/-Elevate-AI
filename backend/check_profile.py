"""Quick script to check profile data in database"""
import sqlite3

# Connect to database
conn = sqlite3.connect('elevateai.db')
cursor = conn.cursor()

# Get all user profiles
cursor.execute("""
    SELECT up.id, u.username, u.email, 
           up.github_username, up.leetcode_username, 
           up.geeksforgeeks_username, up.codechef_username,
           up.hackerrank_username, up.devpost_username, up.devto_username
    FROM user_profiles up
    JOIN users u ON up.user_id = u.id
""")

profiles = cursor.fetchall()

print("=== User Profiles in Database ===\n")
for profile in profiles:
    print(f"ID: {profile[0]}")
    print(f"Username: {profile[1]}")
    print(f"Email: {profile[2]}")
    print(f"GitHub: {profile[3]}")
    print(f"LeetCode: {profile[4]}")
    print(f"GeeksforGeeks: {profile[5]}")
    print(f"CodeChef: {profile[6]}")
    print(f"HackerRank: {profile[7]}")
    print(f"DevPost: {profile[8]}")
    print(f"Dev.to: {profile[9]}")
    print("-" * 50)

conn.close()
