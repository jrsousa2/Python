# COMPARE TRACKS IN THE iTUNES XLM LIBRARY FILE WITH THE MP3 DIRECTORY
# IF THERE ARE MISSING FILES, ADD THEM

import sys
sys.path.insert(0, "D:\\Python\\iTunes\Modules")
sys.path.insert(0, "D:\\Python\\WMP")

# from os.path import exists
import Read_PL
from Files import get_Win_files, Set_diff
from os.path import exists


def Add_miss(rows=None):
    # CALLS FUNCTION
    col_names =  ["Arq"] 
    dict = Read_PL.Read_xml(col_names,rows=rows)
    df = dict['DF']
    # App = dict['App']
    PLs = dict['PLs']
    
    # CREATES ARQ WITH ALL FILE NAMES LOWER CASE 
    Arq = [x.lower() for x in df["Arq"] if exists(x)]
    nbr_files = len(Arq)
    Arq_set = set(Arq)
    #Arq_set_lower = {x.lower for x in Arq_set}
    
    # Save df to Excel to check for dupes
    # file_nm = "D:\\Python\\Excel\\XML.xlsx"
    # df.to_excel(file_nm, sheet_name="XML", index=False)

    # LIST OF ALL MP3 FILES THAT ARE IN THE CHOSEN FOLDER
    dir_path = "E:\\MP3"
    print("\nBuilding list of mp3 files in",dir_path)
    # THESE NEXT VARS ARE BOTH LISTS
    Dir_tuple = get_Win_files(dir_path, ".mp3")
    Dir_list = [x for (x,y) in Dir_tuple]
    nbr_dir_files = len(Dir_list)
    print("\nDirectory has",nbr_dir_files,"files")

    print("\nSearching missing files\n")
    # BELOW COMPARISON IS CASE INSENSITIVE
    miss_files = Set_diff(Dir_list, Arq_set)
    miss_files = list(miss_files)
    nbr_miss_files = len(miss_files)

    # STATS
    print("Files in the directory:",nbr_dir_files)
    print("Files in the iTunes XML (that exist):",nbr_files,"(",len(Arq_set),"distinct)")
    print("Missing files to add:",nbr_miss_files,"\n")

    # CHAMA A FUNCAO QUE CRIA A PL
    # CRIA PLAYLIST APENAS SE HOUVER ARQUIVOS 
    Created_PL_name = "Newly_added"
    if nbr_miss_files>0:
       Add_PL =Read_PL.Create_PL(Created_PL_name,recreate="y")

    # READS PLAYLISTS
    for j in range(nbr_miss_files):
        miss_file = miss_files[j]
        print("Adding file",j+1,"of",nbr_miss_files,"missing:",miss_file)
        Read_PL.Add_file_to_PL(PLs,Created_PL_name,miss_file)

# CALLS FUNC ,rows=500
Add_miss()