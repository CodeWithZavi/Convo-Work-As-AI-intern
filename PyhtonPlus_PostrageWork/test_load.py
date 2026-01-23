from src.essay_loader import EssayLoader
from src.database_manager import DatabaseManager

# Test loading
loader = EssayLoader()
essays = loader.load_essays_from_folder()

print(f"Loaded {len(essays)} essays")
for i, essay in enumerate(essays[:3]):
    print(f"{i+1}. ID: {essay[0]}, Title: {essay[1][:40]}")

# Test inserting
print("\n--- Testing Database Insert ---")
db = DatabaseManager()
db.create_table()
db.clear_all_essays()

for essay_id, title, content in essays[:2]:
    result = db.insert_essay(title, content, essay_id)
    print(f"Insert essay {essay_id}: {result}")
