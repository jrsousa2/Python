# CREATES A SQLITE DB FROM AN EXCEL FILE
import sqlite3
import pandas as pd

# Read Excel
df = pd.read_excel("employees.xlsx")

# Create (or open) SQLite database file
conn = sqlite3.connect("Main_database.db")

# Write DataFrame to a table
df.to_sql("employees", conn, if_exists="replace", index=False)

conn.close()