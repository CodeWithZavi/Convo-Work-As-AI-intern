# 🚀 Quick Setup Guide

## Step-by-Step Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/CodeWithZavi/Convo-Work-As-AI-intern.git
cd Convo-Work-As-AI-intern/PyhtonPlus_PostrageWork
```

### 2️⃣ Install PostgreSQL
Make sure PostgreSQL is installed and running on your system.
- **Windows:** Download from [postgresql.org](https://www.postgresql.org/download/)
- **Mac:** `brew install postgresql`
- **Linux:** `sudo apt-get install postgresql`

### 3️⃣ Create Database
```sql
-- Open PostgreSQL command line
psql -U postgres

-- Create database
CREATE DATABASE "Essays";
```

### 4️⃣ Configure Database Connection
```bash
# Copy example config
cp src/config.example.py src/config.py

# Edit config.py with your credentials
# Change 'your_password_here' to your actual PostgreSQL password
```

### 5️⃣ Install Python Dependencies
```bash
pip install psycopg2
# or if that fails:
pip install psycopg2-binary
```

### 6️⃣ Run the Application
```bash
python main.py
```

---

## ✅ Verification Steps

### Test Database Connection
```bash
python check_db.py
```
**Expected Output:** Shows all essays in database

### Test Essay Loading
```bash
python test_load.py
```
**Expected Output:** Loads sample essays into database

### Add UUID Support (if needed)
```bash
python add_uuid_column.py
```
**Expected Output:** ✅ UUID column added successfully!

---

## 🔐 Security Note

⚠️ **NEVER commit your real database password to GitHub!**

The `src/config.py` file is in `.gitignore` to prevent this.

---

## 🆘 Troubleshooting

### Error: "psycopg2 module not found"
```bash
pip install psycopg2-binary
```

### Error: "Could not connect to database"
- Check PostgreSQL is running
- Verify database credentials in `src/config.py`
- Ensure database "Essays" exists

### Error: "Permission denied"
- Check PostgreSQL user has correct permissions
- Try connecting with psql first to verify credentials

---

## 📖 Need Help?

See the [Full README](README.md) for detailed documentation.

---

**Happy Coding! 🎉**
