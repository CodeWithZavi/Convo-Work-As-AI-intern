import os
import psycopg2
from psycopg2 import Error


class DatabaseManager:
    """Handles all database operations for essays"""
    
    def __init__(self, host='localhost', database='Essays', user='postgres', password='zavian'):
        self.config = {
            'host': host,
            'database': database,
            'user': user,
            'password': password
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
            cursor.execute("ALTER SEQUENCE essays_id_seq RESTART WITH 1")
            conn.commit()
            cursor.close()
        except Error as e:
            print(f"Error clearing essays: {e}")
        finally:
            conn.close()
    
    def insert_essay(self, title, content):
        """Insert a single essay into database"""
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
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


class EssayLoader:
    """Handles loading essays from files"""
    
    def __init__(self, essays_folder='essays'):
        self.essays_folder = essays_folder
    
    def load_essays_from_folder(self):
        """Load all essays from the essays folder"""
        essays = []
        
        if not os.path.exists(self.essays_folder):
            print(f"Error: Folder '{self.essays_folder}' not found")
            return essays
        
        # Get all .txt files in the folder and sort them
        essay_files = [f for f in os.listdir(self.essays_folder) if f.endswith('.txt')]
        essay_files.sort()  # Sort files to maintain order
        
        for filename in essay_files:
            filepath = os.path.join(self.essays_folder, filename)
            
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                    
                    if not lines:
                        continue
                    
                    title = lines[0].strip()
                    content = "".join(lines[1:]).strip()
                    
                    essays.append((title, content))
            except Exception as e:
                print(f"Error reading {filename}: {e}")
        
        return essays


class Menu:
    """Handles user menu interactions"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def display_menu(self):
        """Display menu options"""
        print("\n" + "="*50)
        print("Menu:")
        print("1. Show all essays")
        print("2. Get essay by ID")
        print("3. Get title by ID")
        print("4. Get ID by title")
        print("5. Exit")
        print("="*50)
    
    def show_all_essays(self):
        """Display all essays"""
        essays = self.db_manager.get_all_essays()
        
        if not essays:
            print("No essays found")
            return
        
        for essay in essays:
            print(f"\nID      : {essay[0]}")
            print(f"Title   : {essay[1]}")
            print(f"Content : {essay[2]}")
    
    def show_essay_by_id(self):
        """Get and display essay by ID"""
        eid_input = input("Enter essay ID: ").strip()
        
        if not eid_input.isdigit():
            print("Invalid ID")
            return
        
        essay = self.db_manager.get_essay_by_id(int(eid_input))
        
        if essay:
            print(f"\nID      : {essay[0]}")
            print(f"Title   : {essay[1]}")
            print(f"Content : {essay[2]}")
        else:
            print("Essay not found")
    
    def show_title_by_id(self):
        """Get and display title by ID"""
        eid_input = input("Enter essay ID: ").strip()
        
        if not eid_input.isdigit():
            print("Invalid ID")
            return
        
        title = self.db_manager.get_title_by_id(int(eid_input))
        
        if title:
            print(f"Title: {title}")
        else:
            print("Essay not found")
    
    def show_id_by_title(self):
        """Get and display ID by title"""
        title_input = input("Enter essay title: ").strip()
        essay_id = self.db_manager.get_id_by_title(title_input)
        
        if essay_id:
            print(f"ID: {essay_id}")
        else:
            print("Essay not found")
    
    def run(self):
        """Run the menu loop"""
        while True:
            self.display_menu()
            choice = input("Choose: ").strip()
            
            if choice == "1":
                self.show_all_essays()
            elif choice == "2":
                self.show_essay_by_id()
            elif choice == "3":
                self.show_title_by_id()
            elif choice == "4":
                self.show_id_by_title()
            elif choice == "5":
                print("Exiting program.")
                break
            else:
                print("Invalid choice")


class Main:
    """Main class that orchestrates the entire application"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.essay_loader = EssayLoader('essays')
        self.menu = Menu(self.db_manager)
    
    def initialize_database(self):
        """Initialize database and load essays"""
        print("Initializing database...")
        
        # Create table
        self.db_manager.create_table()
        
        # Clear existing data
        self.db_manager.clear_all_essays()
        
        # Load essays from folder
        essays = self.essay_loader.load_essays_from_folder()
        
        # Insert essays into database
        essays_loaded = 0
        for title, content in essays:
            if self.db_manager.insert_essay(title, content):
                essays_loaded += 1
        
        print(f"Essays loaded: {essays_loaded}")
    
    def run(self):
        """Run the main application"""
        self.initialize_database()
        self.menu.run()


if __name__ == "__main__":
    app = Main()
    app.run()
