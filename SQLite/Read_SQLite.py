import sqlite3
import pandas as pd

# Path to your Manifest.db file
db_path = r"C:\Users\JR Sousa\AppData\Roaming\Apple Computer\MobileSync\Backup\00008101-000601C22232001E\Manifest.db"

# Connect to the SQLite database
conn = sqlite3.connect(db_path)

# Query the tables
tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("Tables in Manifest.db:")
print(tables)

# Example: read the 'Files' table (common in iOS backups)
try:
    df = pd.read_sql_query("SELECT * FROM Files;", conn)
except Exception as e:
    print("Error reading 'Files' table:", e)
    # If Files table doesn't exist, read another table
    df = pd.read_sql_query("SELECT * FROM Manifest;", conn)

# Save to Excel
excel_path = r"D:\Python\Excel\Manifest_db.xlsx"
df.to_excel(excel_path, index=False)
print(f"Saved Excel file to {excel_path}")

# Close connection
conn.close()
