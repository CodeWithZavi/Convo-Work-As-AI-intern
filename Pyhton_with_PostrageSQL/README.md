# Essay Management System

A modular essay management system with two different approaches for storing and retrieving essays.

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
