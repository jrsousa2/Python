# READ SQLITE DB AND SUMMARIZE ROWS (TRACKS) BY YEAR
import sqlite3
import pandas as pd

# Open existing SQLite database
with sqlite3.connect(r"D:\Python\Databases\Main_database.db") as conn:

    # Read table
    df = pd.read_sql("SELECT * FROM iTunes where Year>2000", conn)

    # MAKE YEAR INTEGER (INSTEAD OF FLOAT) FOR A NEATER DISPLAY
    df["Year"] = df["Year"].astype(int)

# Summarize rows by Year
year_summary = df.groupby("Year").size().reset_index(name="Count")

print(year_summary)