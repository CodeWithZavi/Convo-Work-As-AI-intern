"""
Main entry point for Essay Database Management System
This uses PostgreSQL database for storage
"""

from src.database_manager import DatabaseManager
from src.essay_loader import EssayLoader
from src.menu import Menu


class Main:
    """Main class that orchestrates the entire application"""
    
    def __init__(self):
        """Initialize all components"""
        self.db_manager = DatabaseManager()
        self.essay_loader = EssayLoader()
        self.menu = Menu(self.db_manager)
    
    def initialize_database(self):
        """Initialize database and load essays"""
        print("Initializing database...")
        
        # Create table
        self.db_manager.create_table()
        
        # Clear existing data
        self.db_manager.clear_all_essays()
        
        # Load essays from folder (now includes essay IDs)
        essays = self.essay_loader.load_essays_from_folder()
        
        # Insert essays into database with their correct IDs
        essays_loaded = 0
        for essay_id, title, content in essays:
            if self.db_manager.insert_essay(title, content, essay_id):
                essays_loaded += 1
        
        # Reset sequence to continue from the highest ID
        self.db_manager.reset_sequence()
        
        print(f"Essays loaded: {essays_loaded}")
    
    def run(self):
        """Run the main application"""
        self.initialize_database()
        self.menu.run()


if __name__ == "__main__":
    app = Main()
    app.run()
