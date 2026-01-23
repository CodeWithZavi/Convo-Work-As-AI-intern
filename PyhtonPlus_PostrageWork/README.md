# Essay Management System with PostgreSQL & UUID

## 👨‍💻 Author
**Noman Shakir**  
Working as AI Intern at **Convo, Islamabad**

## 📌 About This Project
This is an internship project developed at Convo, Islamabad. The system demonstrates a complete essay management solution using PostgreSQL with UUID tracking, automatic ID renumbering, and a clean modular architecture. This project showcases database operations, Python OOP principles, and real-world application development.

## 🔗 Repository
**GitHub:** [https://github.com/CodeWithZavi/Convo-Work-As-AI-intern](https://github.com/CodeWithZavi/Convo-Work-As-AI-intern)  
*Future work and updates will be added to this repository.*

---

## 🚀 Quick Start Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/CodeWithZavi/Convo-Work-As-AI-intern.git
cd Convo-Work-As-AI-intern/PyhtonPlus_PostrageWork
```

### 2. Configure Database
Create a `config.py` file in the `src/` folder:
```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'Essays',
    'user': 'postgres',
    'password': 'your_password_here'  # Change this!
}

ESSAYS_FOLDER = 'essays'
```

### 3. Install PostgreSQL
Make sure PostgreSQL is installed and running on your system.

### 4. Install Python Dependencies
```bash
pip install psycopg2
```

### 5. Run the Application
```bash
python main.py
```

### 6. (Optional) Add UUID Column to Existing Database
If you already have essays in the database:
```bash
python add_uuid_column.py
```

---

## 📁 Project Structure

```
PyhtonPlus_PostrageWork/
├── essays/                      # Essay text files
│   ├── essay1.txt
│   ├── essay2.txt
│   └── ...
│
├── src/                         # Source code
│   ├── __init__.py             # Package initialization
│   ├── config.py               # Database configuration (GITIGNORED)
│   ├── database_manager.py     # Database operations
│   ├── essay_loader.py         # Load essays from files
│   └── menu.py                 # User interface
│
├── main.py                      # Main entry point
├── add_uuid_column.py          # UUID migration script
├── check_db.py                 # Database connection test
├── test_load.py                # Test essay loading
├── README.md                   # This file
└── UUID_README.md              # UUID implementation guide
```

---

## 🎯 Features

### ✨ Core Features
- ✅ **PostgreSQL Database** - Persistent storage with ACID compliance
- ✅ **UUID Support** - Each essay has a permanent unique identifier
- ✅ **Auto ID Renumbering** - IDs automatically renumber (1, 2, 3...) after deletion
- ✅ **Interactive Menu** - User-friendly command-line interface
- ✅ **CRUD Operations** - Create, Read, Update, Delete essays
- ✅ **Bulk Loading** - Load multiple essays from text files
- ✅ **Search Functions** - Find by ID, title, or UUID

### 🔐 Security Features
- ✅ **SQL Injection Prevention** - Parameterized queries
- ✅ **Password Protection** - Database credentials in .gitignore
- ✅ **Error Handling** - Graceful error management

---

## 📦 Components

### 1. **database_manager.py** - `DatabaseManager` class

#### Connection & Setup
- `get_connection()` - Establish PostgreSQL connection
- `create_table()` - Create essays table with UUID support

#### CRUD Operations
- `insert_essay(title, content, essay_id=None)` - Add new essay
- `get_all_essays()` - Retrieve all essays with UUIDs
- `get_essay_by_id(essay_id)` - Get specific essay
- `get_title_by_id(essay_id)` - Get only title
- `get_id_by_title(title)` - Search by title
- `delete_essay(essay_id)` - Delete and renumber

#### Maintenance
- `clear_all_essays()` - Remove all essays
- `reset_sequence()` - Reset ID counter
- `reorder_all_ids()` - Renumber all IDs sequentially

### 2. **essay_loader.py** - `EssayLoader` class
- `load_from_file(filepath)` - Load single essay from file
- Automatically reads title from first line
- Generates UUID for each essay

### 3. **menu.py** - `Menu` class
- `display_menu()` - Show menu options
- `show_all_essays()` - Display all essays with ID & UUID
- `show_essay_by_id()` - Search by ID
- `show_title_by_id()` - Get title only
- `show_id_by_title()` - Reverse search
- `insert_new_essay()` - Add new essay
- `delete_essay()` - Remove essay (with confirmation)
- `run()` - Main menu loop

### 4. **main.py** - Application Entry Point
- Initializes database connection
- Creates table if needed
- Loads sample essays
- Runs interactive menu

---

## 📋 Menu Options

```
1. Show all essays       - Display all essays with ID, UUID, title, content
2. Get essay by ID       - Search specific essay by ID number
3. Get title by ID       - Get only the title of an essay
4. Get ID by title       - Find essay ID by searching title
5. Insert new essay      - Add a new essay to database
6. Delete essay          - Remove essay (auto-renumbers IDs)
7. Exit                  - Close application
```

---

## 🗄️ Database Schema

```sql
CREATE TABLE essays (
    id SERIAL PRIMARY KEY,                    -- Sequential ID (1, 2, 3...)
    uuid UUID UNIQUE NOT NULL,                -- Permanent unique identifier
    title VARCHAR(500) NOT NULL,              -- Essay title
    content TEXT NOT NULL                     -- Essay content
);
```

### Why Both ID and UUID?

| Feature | ID (Integer) | UUID |
|---------|-------------|------|
| **User-friendly** | ✅ Easy (type "1") | ❌ Complex |
| **Sequential** | ✅ Always 1, 2, 3... | ❌ Random |
| **Permanent** | ❌ Changes on renumber | ✅ Never changes |
| **Unique globally** | ❌ Only in this DB | ✅ Universally unique |
| **API/Export** | ❌ Not reliable | ✅ Perfect for tracking |

**Best of both worlds:** Users see simple IDs, system tracks with UUIDs!

---

## 🔄 How ID Renumbering Works

### Example Flow:
```
Initial State:
ID: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

↓ Delete ID 5

After Deletion:
ID: 1, 2, 3, 4, 5, 6, 7, 8, 9  ← All IDs renumbered!
(Old 6→5, Old 7→6, Old 8→7, etc.)

UUIDs remain unchanged for tracking
```

---

## 🛠️ Configuration

### Database Configuration (`src/config.py`)
```python
DB_CONFIG = {
    'host': 'localhost',         # Database server
    'database': 'Essays',        # Database name
    'user': 'postgres',          # Username
    'password': 'your_password'  # Your password
}

ESSAYS_FOLDER = 'essays'        # Folder with essay files
```

⚠️ **Important:** Never commit `config.py` with real passwords!

### Essay File Format
Create `.txt` files in the `essays/` folder:

```
Your Essay Title Here
This is the first paragraph of your essay content.

This is the second paragraph.
You can have multiple paragraphs.
```

**Format:**
- **Line 1:** Title
- **Rest:** Content

---

## 🔐 Security Best Practices

### .gitignore Protection
The following files are ignored to protect sensitive data:
- `src/config.py` - Contains database password
- `__pycache__/` - Python cache files
- `*.pyc` - Compiled Python files
- `.env` - Environment variables

### Setting Up Your Own Config
1. Copy `config.example.py` (if provided) to `config.py`
2. Update with your database credentials
3. Never commit `config.py` to GitHub

---

## 🧪 Testing

### Check Database Connection
```bash
python check_db.py
```

### Test Essay Loading
```bash
python test_load.py
```

### Add UUID to Existing Database
```bash
python add_uuid_column.py
```

---

## 💡 Usage Examples

### Adding a New Essay
```
Menu → 5 (Insert new essay)
Enter title: My New Essay
Enter content: Type your content here.
Press Enter twice to finish.
✅ Essay inserted successfully!
```

### Deleting an Essay
```
Menu → 6 (Delete essay)
Enter ID: 5
Are you sure? (yes/no): yes
✅ Essay deleted successfully!
(All IDs automatically renumbered)
```

### Searching by Title
```
Menu → 4 (Get ID by title)
Enter title: Machine Learning
→ ID: 2
```

---

## 🎓 Learning Outcomes

This project demonstrates:
- 🔹 **Database Design** - PostgreSQL schema with constraints
- 🔹 **Python OOP** - Classes, methods, encapsulation
- 🔹 **CRUD Operations** - Create, Read, Update, Delete
- 🔹 **UUID Implementation** - Permanent unique identifiers
- 🔹 **SQL Injection Prevention** - Parameterized queries
- 🔹 **Error Handling** - Try-except blocks, graceful failures
- 🔹 **Modular Architecture** - Separation of concerns
- 🔹 **User Interface** - Command-line menu system
- 🔹 **File I/O** - Reading essay files
- 🔹 **Git Best Practices** - .gitignore for security

---

## 🚧 Future Enhancements

- [ ] Add essay update/edit functionality
- [ ] Implement full-text search
- [ ] Add user authentication
- [ ] Create REST API endpoints
- [ ] Build web interface (Flask/Django)
- [ ] Add export to PDF/Word
- [ ] Implement tags/categories
- [ ] Add version history
- [ ] Multi-language support

---

## 📚 Additional Documentation

- [UUID_README.md](UUID_README.md) - UUID implementation details
- [FLOW_ARCHITECTURE.md](FLOW_ARCHITECTURE.md) - System architecture
- [SIMPLE_FLOW_DIAGRAM.md](SIMPLE_FLOW_DIAGRAM.md) - Flow diagrams

---

## 🤝 Contributing

This is an internship project at Convo, Islamabad. Future updates and improvements will be added to this repository.

---

## 📄 License

This project is part of internship work at Convo, Islamabad.

---

## 📞 Contact

**Noman Shakir**  
AI Intern - Convo, Islamabad  
**Repository:** [https://github.com/CodeWithZavi/Convo-Work-As-AI-intern](https://github.com/CodeWithZavi/Convo-Work-As-AI-intern)

---

*Built with 💙 at Convo, Islamabad*

## 📁 Project Structure

```
TodayTask/
├── essays/                      # Folder containing all essay text files
│   ├── essay1.txt
│   ├── essay2.txt
│   └── ...
│
├── src/                         # Database approach (PostgreSQL)
│   ├── __init__.py             # Package initialization
│   ├── config.py               # Database configuration
│   ├── database_manager.py     # DatabaseManager class
│   ├── essay_loader.py         # EssayLoader class
│   └── menu.py                 # Menu class
│
├── src_mapping/                 # Dictionary approach (In-memory)
│   ├── __init__.py             # Package initialization
│   ├── config.py               # Configuration
│   ├── essay_dictionary.py     # EssayDictionary class
│   └── menu.py                 # Menu class
│
├── main.py                      # Entry point for database approach
├── main_mapping.py              # Entry point for dictionary approach
├── essay_database.py            # (Legacy - single file version)
└── essay_mapping_approach.py    # (Legacy - single file version)
```

## 🚀 How to Run

### Database Approach (PostgreSQL)
```bash
python main.py
```

### Dictionary Approach (In-memory)
```bash
python main_mapping.py
```

## 📦 Components

### Database Approach (`src/`)

#### 1. **config.py**
- Database connection settings
- Essays folder path configuration

#### 2. **database_manager.py** - `DatabaseManager` class
- `get_connection()` - Establish PostgreSQL connection
- `create_table()` - Create essays table
- `clear_all_essays()` - Clear all essays from database
- `insert_essay(title, content)` - Insert single essay
- `get_all_essays()` - Retrieve all essays
- `get_essay_by_id(essay_id)` - Get essay by ID
- `get_title_by_id(essay_id)` - Get title by ID
- `get_id_by_title(title)` - Get ID by title

#### 3. **essay_loader.py** - `EssayLoader` class
- `load_essays_from_folder()` - Load all essays from folder
- Automatically sorts files for correct order
- Handles file reading and error handling

#### 4. **menu.py** - `Menu` class
- `display_menu()` - Show menu options
- `show_all_essays()` - Display all essays
- `show_essay_by_id()` - Get and display essay by ID
- `show_title_by_id()` - Get and display title by ID
- `show_id_by_title()` - Get and display ID by title
- `run()` - Run menu loop

#### 5. **main.py** - `Main` class
- Orchestrates all components
- Initializes database
- Loads essays
- Runs the application

### Dictionary Approach (`src_mapping/`)

#### 1. **config.py**
- Essays folder path configuration

#### 2. **essay_dictionary.py** - `EssayDictionary` class
- `load_from_folder()` - Load essays into dictionary
- `get_all_essays()` - Return all essays
- `get_essay_by_id(eid)` - Get essay by ID
- `get_title_by_id(eid)` - Get title by ID
- `get_id_by_title(title)` - Get ID by title
- Uses nested dictionary structure:
  ```python
  {
    1: {
      "meta": {"title": "Essay Title"},
      "data": {"content": "Essay content..."}
    }
  }
  ```

#### 3. **menu.py** - `Menu` class
- Same functionality as database approach menu
- Works with EssayDictionary instead of database

#### 4. **main_mapping.py** - `Main` class
- Orchestrates dictionary approach components
- Loads essays into memory
- Runs the application

## 🎯 Features

✅ **Modular Design** - Separated into logical components
✅ **Two Storage Options** - Database (PostgreSQL) or In-memory (Dictionary)
✅ **Automatic File Loading** - Reads all .txt files from essays folder
✅ **Sorted Loading** - Essays loaded in correct numerical order
✅ **Clean Architecture** - Each class has single responsibility
✅ **Easy to Extend** - Add new features without modifying existing code
✅ **Interactive Menu** - User-friendly command-line interface

## 📋 Menu Options

1. **Show all essays** - Display all essays with ID, title, and content
2. **Get essay by ID** - Search and display specific essay by ID
3. **Get title by ID** - Get only the title of an essay
4. **Get ID by title** - Find essay ID by searching title
5. **Exit** - Close the application

## 🛠️ Configuration

### Database Configuration (`src/config.py`)
```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'Essays',
    'user': 'postgres',
    'password': 'zavian'
}
```

### Essays Folder
- All essay files should be in the `essays/` folder
- Files should be `.txt` format
- First line: Essay title
- Remaining lines: Essay content

## 🔄 Adding New Essays

1. Create a new `.txt` file in the `essays/` folder
2. First line: Essay title
3. Rest of the file: Essay content
4. Run the application - it will automatically load the new essay

## 💡 Advantages

**Database Approach:**
- Persistent storage
- Can handle large datasets
- SQL query capabilities
- Multi-user support

**Dictionary Approach:**
- Fast in-memory access
- No database setup required
- Simple data structure
- Good for small datasets

## 📝 Notes

- The old single-file versions (`essay_database.py` and `essay_mapping_approach.py`) are kept for reference
- Use the new modular structure (`main.py` and `main_mapping.py`) for better maintainability
- Essays are automatically sorted by filename when loaded
