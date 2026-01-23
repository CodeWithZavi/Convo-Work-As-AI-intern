"""
EssayLoader class - Handles loading essays from files
"""

import os
from .config import ESSAYS_FOLDER


class EssayLoader:
    """Handles loading essays from files"""
    
    def __init__(self, essays_folder=None):
        """Initialize essay loader with folder path"""
        self.essays_folder = essays_folder or ESSAYS_FOLDER
    
    def load_essays_from_folder(self):
        """Load all essays from the essays folder with their IDs"""
        essays = []
        
        if not os.path.exists(self.essays_folder):
            print(f"Error: Folder '{self.essays_folder}' not found")
            return essays
        
        # Get all .txt files in the folder and sort them naturally
        essay_files = [f for f in os.listdir(self.essays_folder) if f.endswith('.txt')]
        # Natural sort to handle essay1, essay2, ... essay10 correctly
        import re
        essay_files.sort(key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0)
        
        for filename in essay_files:
            filepath = os.path.join(self.essays_folder, filename)
            
            # Extract essay number from filename (essay1.txt -> 1)
            import re
            match = re.search(r'(\d+)', filename)
            essay_id = int(match.group(1)) if match else None
            
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                    
                    if not lines:
                        continue
                    
                    title = lines[0].strip()
                    content = "".join(lines[1:]).strip()
                    
                    essays.append((essay_id, title, content))
            except Exception as e:
                print(f"Error reading {filename}: {e}")
        
        return essays
