"""Add LinkedIn URL column to user_profiles table"""
import sqlite3

conn = sqlite3.connect('elevateai.db')
cursor = conn.cursor()

try:
    # Check if column already exists
    cursor.execute("PRAGMA table_info(user_profiles)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'linkedin_url' not in columns:
        print("Adding linkedin_url column...")
        cursor.execute("ALTER TABLE user_profiles ADD COLUMN linkedin_url VARCHAR(500)")
        conn.commit()
        print("✓ Column added successfully!")
    else:
        print("✓ Column already exists!")
        
except Exception as e:
    print(f"✗ Error: {e}")
    conn.rollback()
finally:
    conn.close()
