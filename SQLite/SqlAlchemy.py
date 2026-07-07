from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("sqlite:///D:/Python/Excel/Main_database.db")

df = pd.read_sql("SELECT * FROM iTunes", engine)

print(df.head())