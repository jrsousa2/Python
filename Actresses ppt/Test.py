import openpyxl

def modify_excel(input_file):
    try:
        # Open the Excel file to read and modify it
        workbook = openpyxl.load_workbook(input_file)
        sheet = workbook.active

        # Modify a value
        sheet['A1'] = 'Updated Value'

        # Save changes back to the same file
        workbook.save(input_file)
        
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Ensure workbook is closed properly (although openpyxl should handle this)
        del workbook  # Explicitly remove reference to workbook, if needed

# Example usage
input_file = "D:\\Book1.xlsx"
modify_excel(input_file)
