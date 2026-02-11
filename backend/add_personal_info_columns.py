"""Add personal information columns to user_profiles table"""
import sqlite3

def add_columns():
    conn = sqlite3.connect('elevateai.db')
    cursor = conn.cursor()
    
    # List of new columns to add
    new_columns = [
        ("full_name", "VARCHAR(200)"),
        ("gender", "VARCHAR(50)"),
        ("profile_picture_url", "VARCHAR(500)"),
        ("contact_number", "VARCHAR(20)"),
        ("bio", "VARCHAR(1000)"),
        ("college_name", "VARCHAR(200)"),
        ("degree", "VARCHAR(200)"),
        ("field_of_study", "VARCHAR(200)"),
        ("current_year", "VARCHAR(50)"),
        ("graduation_year", "INTEGER"),
        ("skills", "VARCHAR(1000)"),
    ]
    
    # Check existing columns
    cursor.execute("PRAGMA table_info(user_profiles)")
    existing_columns = [row[1] for row in cursor.fetchall()]
    
    # Add new columns if they don't exist
    for column_name, column_type in new_columns:
        if column_name not in existing_columns:
            try:
                cursor.execute(f"ALTER TABLE user_profiles ADD COLUMN {column_name} {column_type}")
                print(f"✓ Added column: {column_name}")
            except sqlite3.OperationalError as e:
                print(f"✗ Error adding {column_name}: {e}")
        else:
            print(f"- Column {column_name} already exists")
    
    conn.commit()
    conn.close()
    print("\n✓ Database migration completed!")

if __name__ == "__main__":
    add_columns()
