# import os

# directory = r'D:\iTunes\Excel'
# directory = "D://iTunes//Excel"

# if os.path.exists(directory):
#     print("Directory exists.")
# else:
#     print("Directory does not exist.")

import os
import pandas as pd

def Save_Excel(PL_name="BBB", Do_lib=0, rows=None, iTunes=1, col_names=["Arq", "ID"]):
    # Define the file name and path
    file_nm = r'D:\iTunes\Excel\allx.xlsx'
    
    # Log the path
    print(f"Saving to: {file_nm}")
    
    # Ensure the directory exists
    if not os.path.exists(os.path.dirname(file_nm)):
        print("Directory does not exist. Creating directory.")
        os.makedirs(os.path.dirname(file_nm), exist_ok=True)
    else:
        print("Directory exists.")
    
    # Create a sample DataFrame (replace this with your actual data)
    df = pd.DataFrame({"Arq": [1, 2], "ID": [3, 4]})
    
    # Save the DataFrame to Excel
    try:
        df.to_excel(file_nm, sheet_name='Sheet1', index=False)
        print("File saved successfully.")
    except Exception as e:
        print(f"Error saving file: {e}")

import os
print ("ENV",os.getcwd())

Save_Excel()
