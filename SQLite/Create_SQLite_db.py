# CREATES A SQLITE DB 
# LOADS A DB TABLE FROM AN EXCEL FILE
import sqlite3
import pandas as pd

# Read Excel
df = pd.read_excel(r"D:\Python\Excel\ALL-Nov20.xlsx", usecols="A:J")

# COLS WHOSE VALUES HAVE MIXED TYPES: WILL BE CONVERTED TO STRING
cols = ["Art", "Title", "AA", "Album", "Location", "Length", "Genre"]

# COLS IN THE LIST WILL BE CONVERTED TO STR
for col in cols:
    df[col] = df[col].astype(str)

# CHECK SIMPLE TYPES PER INPUT COL
print("DTypes:")
print(df.dtypes)

# DO A DEEP DIVE INTO THE COL TYPES
print("\n\nTYPES PER COL:")
for col in df.select_dtypes(include="object"):
    print(col, df[col].map(type).value_counts())

# Create (or open) SQLite database file
with sqlite3.connect(r"D:\Python\Databases\Main_database.db") as conn:
    # Write DataFrame to a table (FAIL IF TABLE HAS BEEN LOADED ALREADY
    df.to_sql("iTunes", conn, if_exists="fail", index=False)

    # CHECK IF THE DB TABLE WAS CREATED
    print("\n\nPrinting 5 lines of the table\n")
    print(pd.read_sql("SELECT * FROM iTunes LIMIT 5", conn))

