from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("sqlite:///D:/Python/Databases/Main_database.db")

df = pd.read_sql("SELECT * FROM iTunes where Year>2000", engine)

print(df.head())