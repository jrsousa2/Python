import pandas as pd
from pysqlcipher3 import dbapi2 as sqlite

db_path = r"C:\Users\JR Sousa\AppData\Roaming\Apple Computer\MobileSync\Backup\00008101-000601C22232001E\Manifest.db"

conn = sqlite.connect(db_path)
c = conn.cursor()

# Replace 'your_password_here' with your iTunes backup password
c.execute("PRAGMA key='My99life';")
c.execute("PRAGMA cipher_compatibility = 4;")

tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
print(tables)
