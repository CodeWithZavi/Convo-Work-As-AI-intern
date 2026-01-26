"""
Quick script to check database tables
"""
from db_config import engine, SessionLocal
from sqlalchemy import text

db = SessionLocal()

try:
    # Check tables
    result = db.execute(text("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public'"))
    tables = [row[0] for row in result]
    
    print("=" * 50)
    print("Database: HotelManagementSystem")
    print("=" * 50)
    print(f"\nTables found: {len(tables)}")
    for table in tables:
        print(f"  ✓ {table}")
    
    # Check data in each table
    if tables:
        print("\n" + "=" * 50)
        print("Table Data")
        print("=" * 50)
        
        for table in tables:
            result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
            count = result.scalar()
            print(f"\n{table}: {count} rows")
            
            if count > 0:
                result = db.execute(text(f"SELECT * FROM {table} LIMIT 3"))
                print(f"  Sample data:")
                for row in result:
                    print(f"    {dict(row._mapping)}")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
