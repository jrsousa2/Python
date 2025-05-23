import os

folder = r"D:\Python\PySpark\Data"
if os.path.exists(folder):
   print("Folder exists")
else:
    print("Folder doesn't exist")  

# os.makedirs(folder)  # create the folder if it doesn't exist

# file_nm = os.path.join(folder, "Samples.xlsx")
# pandas_df.to_excel(file_nm, index=False)
