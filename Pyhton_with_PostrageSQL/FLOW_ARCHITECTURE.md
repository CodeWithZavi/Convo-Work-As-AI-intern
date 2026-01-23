# Application Flow & Architecture

## 📊 System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         START: main.py                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
         ┌───────────────────────────────┐
         │   Main Class __init__()       │
         │   - Creates DatabaseManager   │
         │   - Creates EssayLoader       │
         │   - Creates Menu              │
         └───────────┬───────────────────┘
                     │
                     ▼
         ┌───────────────────────────────┐
         │   Main.run()                  │
         │   1. initialize_database()    │
         │   2. menu.run()               │
         └───────────┬───────────────────┘
                     │
    ┌────────────────┴────────────────┐
    │                                 │
    ▼                                 ▼
┌─────────────────────┐    ┌──────────────────────┐
│ initialize_database │    │    menu.run()        │
└──────┬──────────────┘    └──────┬───────────────┘
       │                          │
       │                          │ (after init)
       │                          │
       ▼                          ▼
  [Database Setup Flow]      [User Menu Flow]
```

---

## 🔄 Detailed Flow: Database Initialization

```
main.py: initialize_database()
│
├─► Step 1: DatabaseManager.create_table()
│   │
│   └─► PostgreSQL: CREATE TABLE IF NOT EXISTS essays
│       └─► Table with columns: id, title, content
│
├─► Step 2: DatabaseManager.clear_all_essays()
│   │
│   └─► PostgreSQL: DELETE FROM essays
│   └─► PostgreSQL: ALTER SEQUENCE essays_id_seq RESTART WITH 1
│
├─► Step 3: EssayLoader.load_essays_from_folder()
│   │
│   ├─► os.listdir('essays/')  → Get all .txt files
│   │
│   ├─► Sort files numerically
│   │   └─► essay1.txt, essay2.txt, ..., essay10.txt
│   │
│   ├─► For each file:
│   │   ├─► Extract number from filename (essay7.txt → 7)
│   │   ├─► Read file (line 1 = title, rest = content)
│   │   └─► Add to list: (essay_id, title, content)
│   │
│   └─► Return: [(1, "Title1", "Content1"), (2, "Title2", ...), ...]
│
└─► Step 4: Insert essays with specific IDs
    │
    └─► For each (essay_id, title, content):
        └─► DatabaseManager.insert_essay(title, content, essay_id)
            └─► PostgreSQL: INSERT INTO essays (id, title, content) 
                            VALUES (1, 'Title', 'Content')

Result: Database has essays with IDs matching filenames!
```

---

## 🎯 Detailed Flow: Menu Operations

```
Menu.run()
│
└─► Loop Forever:
    │
    ├─► display_menu()
    │   └─► Print menu options (1-5)
    │
    ├─► Get user input
    │
    └─► Process choice:
        │
        ├─► Choice 1: Show all essays
        │   │
        │   └─► DatabaseManager.get_all_essays()
        │       ├─► PostgreSQL: SELECT id, title, content 
        │       │              FROM essays ORDER BY id
        │       └─► Display each essay
        │
        ├─► Choice 2: Get essay by ID
        │   │
        │   ├─► Get ID from user
        │   └─► DatabaseManager.get_essay_by_id(id)
        │       ├─► PostgreSQL: SELECT * FROM essays WHERE id = ?
        │       └─► Display essay or "Not found"
        │
        ├─► Choice 3: Get title by ID
        │   │
        │   ├─► Get ID from user
        │   └─► DatabaseManager.get_title_by_id(id)
        │       ├─► PostgreSQL: SELECT title FROM essays WHERE id = ?
        │       └─► Display title or "Not found"
        │
        ├─► Choice 4: Get ID by title
        │   │
        │   ├─► Get title from user
        │   └─► DatabaseManager.get_id_by_title(title)
        │       ├─► PostgreSQL: SELECT id FROM essays 
        │       │              WHERE LOWER(title) = LOWER(?)
        │       └─► Display ID or "Not found"
        │
        └─► Choice 5: Exit
            └─► Break loop → End program
```

---

## 📁 Component Interaction

```
┌──────────────────────────────────────────────────────────────┐
│                          main.py                             │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │                  Main Class                         │    │
│  │                                                     │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────┐ │    │
│  │  │ db_manager   │  │ essay_loader │  │  menu   │ │    │
│  │  └──────┬───────┘  └──────┬───────┘  └────┬────┘ │    │
│  └─────────┼──────────────────┼───────────────┼──────┘    │
└────────────┼──────────────────┼───────────────┼───────────┘
             │                  │               │
             ▼                  ▼               ▼
    ┌────────────────┐  ┌────────────────┐  ┌──────────┐
    │ src/           │  │ src/           │  │ src/     │
    │ database_      │  │ essay_loader.  │  │ menu.py  │
    │ manager.py     │  │ py             │  │          │
    │                │  │                │  │          │
    │ - connect DB   │  │ - read files   │  │ - UI     │
    │ - CRUD ops     │  │ - parse essays │  │ - input  │
    │ - queries      │  │ - sort files   │  │ - display│
    └────────┬───────┘  └────────────────┘  └─────┬────┘
             │                                     │
             ▼                                     │
    ┌─────────────────┐                          │
    │  PostgreSQL DB  │◄─────────────────────────┘
    │                 │  (queries via db_manager)
    │  essays table:  │
    │  - id           │
    │  - title        │
    │  - content      │
    └─────────────────┘
```

---

## 📝 Step-by-Step Execution Flow

### **When you run: `python main.py`**

**1. Import & Setup** ⚙️
```python
main.py imports:
  ├─► src.database_manager (DatabaseManager)
  ├─► src.essay_loader (EssayLoader)  
  └─► src.menu (Menu)

These import their dependencies:
  ├─► src/config.py (DB_CONFIG, ESSAYS_FOLDER)
  └─► psycopg2 (PostgreSQL connector)
```

**2. Object Creation** 🏗️
```python
Main.__init__():
  ├─► db_manager = DatabaseManager()
  │   └─► Stores DB credentials from config
  │
  ├─► essay_loader = EssayLoader('essays')
  │   └─► Knows where to find essay files
  │
  └─► menu = Menu(db_manager)
      └─► Menu can now use database operations
```

**3. Database Initialization** 💾
```python
Main.initialize_database():
  
  Step 1: Create table
    → db_manager.create_table()
    → SQL: CREATE TABLE IF NOT EXISTS essays (...)
  
  Step 2: Clear old data
    → db_manager.clear_all_essays()
    → SQL: DELETE FROM essays
    → SQL: ALTER SEQUENCE essays_id_seq RESTART WITH 1
  
  Step 3: Load essay files
    → essay_loader.load_essays_from_folder()
    → Returns: [(1, title1, content1), (2, title2, content2), ...]
  
  Step 4: Insert into database
    → For each essay:
      → db_manager.insert_essay(title, content, essay_id)
      → SQL: INSERT INTO essays (id, title, content) VALUES (?, ?, ?)
    
  Output: "Essays loaded: 10"
```

**4. User Interaction** 👤
```python
Main.run() → menu.run():
  
  Loop:
    ├─► Display menu
    ├─► Get user choice (1-5)
    ├─► Execute corresponding function
    │   └─► Each function uses db_manager to query database
    └─► Repeat until user chooses Exit (5)
```

---

## 🔍 Data Flow Example: "Get Essay by ID"

```
User Input: 2 → Get essay by ID
              ↓
         Enter ID: 7
              ↓
    ┌─────────────────────┐
    │ Menu.show_essay_by  │
    │ _id()               │
    └──────────┬──────────┘
               │ Call with ID=7
               ▼
    ┌─────────────────────────────┐
    │ DatabaseManager.get_essay   │
    │ _by_id(7)                   │
    └──────────┬──────────────────┘
               │ Execute SQL
               ▼
    ┌────────────────────────────────────┐
    │ PostgreSQL Database                │
    │ SELECT id, title, content          │
    │ FROM essays WHERE id = 7           │
    └──────────┬─────────────────────────┘
               │ Return data
               ▼
    ┌────────────────────────────┐
    │ Result:                    │
    │ (7, "Unsupervised...", ...) │
    └──────────┬─────────────────┘
               │ Display to user
               ▼
    ╔════════════════════════════════╗
    ║ ID      : 7                    ║
    ║ Title   : Unsupervised Learn...║
    ║ Content : Unsupervised learn...║
    ╚════════════════════════════════╝
```

---

## 🎨 File Structure & Responsibilities

```
TodayTask/
│
├─► main.py
│   └─► ROLE: Entry point, orchestrates everything
│   └─► Creates: DatabaseManager, EssayLoader, Menu
│   └─► Calls: initialize_database() → menu.run()
│
├─► src/
│   │
│   ├─► config.py
│   │   └─► ROLE: Configuration settings
│   │   └─► Contains: DB credentials, folder paths
│   │
│   ├─► database_manager.py
│   │   └─► ROLE: All database operations
│   │   └─► Methods:
│   │       ├─► get_connection() → Connect to PostgreSQL
│   │       ├─► create_table() → Create essays table
│   │       ├─► clear_all_essays() → Delete all + reset sequence
│   │       ├─► insert_essay() → Insert with specific ID
│   │       ├─► get_all_essays() → Fetch all
│   │       ├─► get_essay_by_id() → Fetch by ID
│   │       ├─► get_title_by_id() → Get title only
│   │       └─► get_id_by_title() → Search by title
│   │
│   ├─► essay_loader.py
│   │   └─► ROLE: Read essays from files
│   │   └─► Methods:
│   │       └─► load_essays_from_folder()
│   │           ├─► List all .txt files
│   │           ├─► Sort numerically (essay1, essay2, ...)
│   │           ├─► Extract ID from filename
│   │           ├─► Read title (line 1) & content (rest)
│   │           └─► Return: [(id, title, content), ...]
│   │
│   └─► menu.py
│       └─► ROLE: User interface & interaction
│       └─► Methods:
│           ├─► display_menu() → Show options
│           ├─► show_all_essays() → Display all
│           ├─► show_essay_by_id() → Display specific essay
│           ├─► show_title_by_id() → Display title
│           ├─► show_id_by_title() → Search by title
│           └─► run() → Main menu loop
│
└─► essays/
    ├─► essay1.txt  → ID: 1
    ├─► essay2.txt  → ID: 2
    ├─► ...
    └─► essay10.txt → ID: 10
```

---

## ⚡ Key Features

### **ID Matching Guarantee**
```
essay1.txt  ──► Extract number "1"  ──► INSERT with ID=1  ──► Database ID: 1 ✓
essay2.txt  ──► Extract number "2"  ──► INSERT with ID=2  ──► Database ID: 2 ✓
essay10.txt ──► Extract number "10" ──► INSERT with ID=10 ──► Database ID: 10 ✓
```

### **Numeric Sorting**
```
Before: essay1.txt, essay10.txt, essay2.txt, essay3.txt (wrong!)
After:  essay1.txt, essay2.txt, essay3.txt, ..., essay10.txt (correct!)

Method: Extract number from filename and sort by integer value
```

### **Error Handling**
```
Each component handles errors:
├─► DatabaseManager: Connection failures, SQL errors
├─► EssayLoader: File not found, read errors
└─► Menu: Invalid input, essay not found
```

---

## 🚀 Quick Reference

| Want to... | File to edit | Method to change |
|-----------|-------------|------------------|
| Change DB credentials | `src/config.py` | `DB_CONFIG` |
| Change essays folder | `src/config.py` | `ESSAYS_FOLDER` |
| Modify SQL queries | `src/database_manager.py` | Specific method |
| Change file reading logic | `src/essay_loader.py` | `load_essays_from_folder()` |
| Modify menu options | `src/menu.py` | Add new method + update `run()` |
| Change startup behavior | `main.py` | `Main.__init__()` or `run()` |

---

## 📚 Execution Summary

```
python main.py
      │
      ├─► Create components (db_manager, essay_loader, menu)
      │
      ├─► Initialize database
      │   ├─► Create table
      │   ├─► Clear old data
      │   ├─► Load essays from files (with IDs from filenames)
      │   └─► Insert into database with matching IDs
      │
      └─► Run menu loop
          ├─► Show menu
          ├─► Get user input
          ├─► Execute database queries
          └─► Display results
              └─► Repeat until Exit
```

**Result**: Clean, modular, maintainable code with guaranteed ID matching! ✨
