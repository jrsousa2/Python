import pandas as pd
# import Excel

def print_to_file(seq, novela, actors, file_name="D:\\Videos\\Novelas\\2o video\\names.txt"):

    # Open the file for writing
    with open(file_name, "a") as f:
         # SKIP LINE
         f.write("\n\n")
         f.write("Novela {}: {}".format(seq+1,novela))
         f.write("\n\n")
    #"Step {}. This is {} of {}.".format(var1, var2, var3)
    #Files.Print_to_file(Log_file,"\nChecking file {} of {}) ({})\n",j+1,nbr_files_to_updt,Files.track_time())

    # Split the list into two equal parts
    half = len(actors) // 2
    col1 = actors[:half]  # First half for column 1
    col2 = actors[half:]  # Second half for column 2

    # Determine the max length of names in col1 for consistent alignment
    max_len = max(len(name) for name in col1) + 2  # Adding extra space for padding

    # Open the file for writing
    with open(file_name, "a") as f:
        for name1, name2 in zip(col1, col2):
            # Write to the file with the - separator, aligning the first column names
            f.write(f"• {name1.ljust(max_len)}• {name2}\n")
        

# START OF THE PGM
# Load the Excel file into a DataFrame
df = pd.read_excel("D:\\Videos\\Novelas\\2o video\\Atores.xlsx", sheet_name="Main")

# Grouping the DataFrame by 'Novela' and creating a list of lists
lists = [group["Atriz"].tolist() for _, group in df.groupby("Novela", sort=False)]
nbr = len(lists)

# Get the distinct values of the 'Novela' column while preserving order
novelas = list(dict.fromkeys(df['Novela']))

# PRINTS
for i in range(nbr):
    print_to_file(i,novelas[i], lists[i])
