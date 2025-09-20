import plistlib
import pandas as pd

plist_path = r"C:\Users\JR Sousa\AppData\Roaming\Apple Computer\MobileSync\Backup\00008101-000601C22232001E\Manifest.plist"

with open(plist_path, "rb") as f:
    plist_data = plistlib.load(f)

# plist_data is usually a dict, flatten to DataFrame
df = pd.json_normalize(plist_data)

excel_path = r"D:\Python\Excel\Manifest.xlsx"
df.to_excel(excel_path, index=False)
print(f"Saved Excel file to {excel_path}")
