"""
Script to add UUID column to existing essays table
Run this once to upgrade your existing database
"""

from src.database_manager import DatabaseManager

def add_uuid_column():
    """Add UUID column to existing table and populate it"""
    db = DatabaseManager()
    conn = db.get_connection()
    
    if not conn:
        print("Failed to connect to database")
        return
    
    try:
        cursor = conn.cursor()
        
        # Check if uuid column exists
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='essays' AND column_name='uuid'
        """)
        
        if cursor.fetchone():
            print("UUID column already exists!")
            cursor.close()
            conn.close()
            return
        
        print("Adding UUID column...")
        
        # Add UUID column
        cursor.execute("""
            ALTER TABLE essays 
            ADD COLUMN uuid UUID UNIQUE DEFAULT gen_random_uuid()
        """)
        
        # Make it NOT NULL after populating
        cursor.execute("""
            ALTER TABLE essays 
            ALTER COLUMN uuid SET NOT NULL
        """)
        
        conn.commit()
        cursor.close()
        print("✅ UUID column added successfully!")
        print("All existing essays now have unique UUIDs")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("="*50)
    print("UUID Column Migration Script")
    print("="*50)
    add_uuid_column()
