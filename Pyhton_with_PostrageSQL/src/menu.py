"""
Menu class - Handles user menu interactions
"""


class Menu:
    """Handles user menu interactions"""
    
    def __init__(self, db_manager):
        """Initialize menu with database manager"""
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
