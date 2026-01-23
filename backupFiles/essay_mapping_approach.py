import os


class EssayDictionary:
    """Handles essay storage using nested dictionary structure"""
    
    def __init__(self):
        self.essays = {}
        self.essay_id = 1
    
    def load_from_folder(self, folder='essays'):
        """Load essays from folder into dictionary"""
        if not os.path.exists(folder):
            print(f"Error: Folder '{folder}' not found")
            return
        
        # Get all .txt files in the folder
        essay_files = [f for f in os.listdir(folder) if f.endswith('.txt')]
        
        for filename in essay_files:
            filepath = os.path.join(folder, filename)
            
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                    
                    if not lines:
                        continue
                    
                    self.essays[self.essay_id] = {
                        "meta": {
                            "title": lines[0].strip()
                        },
                        "data": {
                            "content": "".join(lines[1:]).strip()
                        }
                    }
                    
                    self.essay_id += 1
            except Exception as e:
                print(f"Error reading {filename}: {e}")
        
        print(f"Essays loaded: {len(self.essays)}")
    
    def get_all_essays(self):
        """Return all essays"""
        return self.essays
    
    def get_essay_by_id(self, eid):
        """Get essay by ID"""
        return self.essays.get(eid)
    
    def get_title_by_id(self, eid):
        """Get title by ID"""
        essay = self.essays.get(eid)
        if essay:
            return essay['meta']['title']
        return None
    
    def get_id_by_title(self, title):
        """Get ID by title"""
        for eid, essay in self.essays.items():
            if essay['meta']['title'].lower() == title.lower():
                return eid
        return None


class Menu:
    """Handles user menu interactions"""
    
    def __init__(self, essay_dict):
        self.essay_dict = essay_dict
    
    def display_menu(self):
        """Display menu options"""
        print("\nMenu:")
        print("1. Show all essays")
        print("2. Get essay by ID")
        print("3. Get title by ID")
        print("4. Get ID by title")
        print("5. Exit")
    
    def show_all_essays(self):
        """Display all essays"""
        essays = self.essay_dict.get_all_essays()
        
        if not essays:
            print("No essays found")
            return
        
        for eid, essay in essays.items():
            print(f"ID      : {eid}")
            print(f"Title   : {essay['meta']['title']}")
            print(f"Content : {essay['data']['content']}")
    
    def show_essay_by_id(self):
        """Get and display essay by ID"""
        eid_input = input("Enter essay ID: ").strip()
        
        if not eid_input.isdigit():
            print("Invalid ID")
            return
        
        essay = self.essay_dict.get_essay_by_id(int(eid_input))
        
        if essay:
            print(f"ID      : {eid_input}")
            print(f"Title   : {essay['meta']['title']}")
            print(f"Content : {essay['data']['content']}")
        else:
            print("Essay not found")
    
    def show_title_by_id(self):
        """Get and display title by ID"""
        eid_input = input("Enter essay ID: ").strip()
        
        if not eid_input.isdigit():
            print("Invalid ID")
            return
        
        title = self.essay_dict.get_title_by_id(int(eid_input))
        
        if title:
            print(f"Title: {title}")
        else:
            print("Essay not found")
    
    def show_id_by_title(self):
        """Get and display ID by title"""
        title_input = input("Enter essay title: ").strip()
        essay_id = self.essay_dict.get_id_by_title(title_input)
        
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
        self.essay_dict = EssayDictionary()
        self.menu = Menu(self.essay_dict)
    
    def run(self):
        """Run the main application"""
        self.essay_dict.load_from_folder('essays')
        self.menu.run()


if __name__ == "__main__":
    app = Main()
    app.run()
