import sqlite3
import os

# Path to the database file
db_path = os.path.join('instance', 'local.db')

# Check if the database file exists
if not os.path.exists(db_path):
    print(f"Database file not found at {db_path}")
    exit(1)

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Check if the new columns already exist
    cursor.execute("PRAGMA table_info(company)")
    columns = [column[1] for column in cursor.fetchall()]
    
    # Add new columns if they don't exist
    if "email" not in columns:
        cursor.execute("ALTER TABLE company ADD COLUMN email TEXT")
        print("Added email column")
    
    if "bank_details" not in columns:
        cursor.execute("ALTER TABLE company ADD COLUMN bank_details TEXT")
        print("Added bank_details column")
    
    if "request_id" not in columns:
        cursor.execute("ALTER TABLE company ADD COLUMN request_id TEXT")
        print("Added request_id column")
    
    if "last_checked" not in columns:
        cursor.execute("ALTER TABLE company ADD COLUMN last_checked TIMESTAMP")
        print("Added last_checked column")
    
    # Commit changes
    conn.commit()
    print("Database migration completed successfully!")
    
except Exception as e:
    print(f"Error during migration: {e}")
    conn.rollback()
finally:
    conn.close()
