"""Add code column to email_tokens table"""
import sqlite3

# Connect to database
conn = sqlite3.connect('elevateai.db')
cursor = conn.cursor()

try:
    # Check if column already exists
    cursor.execute("PRAGMA table_info(email_tokens)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'code' not in columns:
        # Add code column
        cursor.execute("ALTER TABLE email_tokens ADD COLUMN code VARCHAR(6)")
        conn.commit()
        print("✅ Successfully added 'code' column to email_tokens table")
    else:
        print("ℹ️  'code' column already exists in email_tokens table")
        
except Exception as e:
    print(f"❌ Error: {e}")
    conn.rollback()
finally:
    conn.close()
