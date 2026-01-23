"""
DatabaseManager class - Handles all PostgreSQL database operations
"""

import psycopg2
from psycopg2 import Error
from .config import DB_CONFIG


class DatabaseManager:
    """Handles all database operations for essays"""
    
    def __init__(self, host=None, database=None, user=None, password=None):
        """Initialize database manager with config"""
        self.config = {
            'host': host or DB_CONFIG['host'],
            'database': database or DB_CONFIG['database'],
            'user': user or DB_CONFIG['user'],
            'password': password or DB_CONFIG['password']
        }
    
    def get_connection(self):
        """Establish connection to PostgreSQL database"""
        try:
            return psycopg2.connect(**self.config)
        except Error as e:
            print(f"Error connecting to PostgreSQL: {e}")
            return None
    
    def create_table(self):
        """Create essays table if it doesn't exist"""
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS essays (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(500) NOT NULL,
                        content TEXT NOT NULL
                    )
                """)
                conn.commit()
                cursor.close()
                print("Table created successfully")
            except Error as e:
                print(f"Error creating table: {e}")
            finally:
                conn.close()
    
    def clear_all_essays(self):
        """Clear all essays from database"""
        conn = self.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM essays")
            conn.commit()
            cursor.close()
        except Error as e:
            print(f"Error clearing essays: {e}")
        finally:
            conn.close()
    
    def reset_sequence(self):
        """Reset the ID sequence to continue from the highest ID"""
        conn = self.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT setval('essays_id_seq', COALESCE((SELECT MAX(id) FROM essays), 0) + 1, false)")
            conn.commit()
            cursor.close()
        except Error as e:
            print(f"Error resetting sequence: {e}")
        finally:
            conn.close()
    
    def insert_essay(self, title, content, essay_id=None):
        """Insert a single essay into database with specific ID"""
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            if essay_id:
                # Insert with specific ID
                cursor.execute(
                    "INSERT INTO essays (id, title, content) VALUES (%s, %s, %s)",
                    (essay_id, title, content)
                )
            else:
                # Insert with auto-increment ID
                cursor.execute(
                    "INSERT INTO essays (title, content) VALUES (%s, %s)",
                    (title, content)
                )
            conn.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error inserting essay: {e}")
            return False
        finally:
            conn.close()
    
    def get_all_essays(self):
        """Retrieve all essays from database"""
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, content FROM essays ORDER BY id")
            essays = cursor.fetchall()
            cursor.close()
            return essays
        except Error as e:
            print(f"Error fetching essays: {e}")
            return []
        finally:
            conn.close()
    
    def get_essay_by_id(self, essay_id):
        """Retrieve essay by ID"""
        conn = self.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, content FROM essays WHERE id = %s", (essay_id,))
            essay = cursor.fetchone()
            cursor.close()
            return essay
        except Error as e:
            print(f"Error fetching essay: {e}")
            return None
        finally:
            conn.close()
    
    def get_title_by_id(self, essay_id):
        """Retrieve only title by ID"""
        conn = self.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT title FROM essays WHERE id = %s", (essay_id,))
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else None
        except Error as e:
            print(f"Error fetching title: {e}")
            return None
        finally:
            conn.close()
    
    def get_id_by_title(self, title):
        """Retrieve essay ID by title"""
        conn = self.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM essays WHERE LOWER(title) = LOWER(%s)", (title,))
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else None
        except Error as e:
            print(f"Error fetching ID: {e}")
            return None
        finally:
            conn.close()
    
    def delete_essay(self, essay_id):
        """Delete essay by ID"""
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM essays WHERE id = %s", (essay_id,))
            rows_deleted = cursor.rowcount
            conn.commit()
            cursor.close()
            return rows_deleted > 0
        except Error as e:
            print(f"Error deleting essay: {e}")
            return False
        finally:
            conn.close()
