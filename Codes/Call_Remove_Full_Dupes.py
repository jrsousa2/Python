# REMOVE FILES THAT ARE COMPLETELY DUPLICATE
# THAT IS, THESE FILES ARE THE SAME, BUT ARE DUPLICATED IN THE XML LIBRARY
# ADDED DATETIME AND OTHER ATTRIBUTES MAY DIFFER

import pandas as pd
from os.path import exists
import Read_PL

# MAIN CODE
def Remove_full_dupes(rows=None):
    # START
    dict = Read_PL.Init_iTunes()
    App = dict['App']
    PLs = dict['PLs']

    col_names = ["Arq", "PID"]
    df = Read_PL.Read_xml(col_names,rows=rows)
    start_rows = df.shape[0]
    # ADD POS COLUMN
    df['Pos'] = range(1, len(df) + 1)
    
    # SELECT ONLY RELEVANT ROWS
    print("Removing dead tracks\n")
    df = df[df['Arq'] != ""]
    end_rows = df.shape[0]
    print("Library has:",start_rows,"tracks (of which", end_rows,"are valid)\n")

    # CREATES COL. TO GROUP BY
    print("Creating lowercase fullnames list...\n")
    df.loc[:,'Arq2'] = df['Arq'].str.lower()

    # ADD COUNT COL. AND SELECT
    group_list = ["Arq2"]
    print("Calculating dupes\n")
    df.loc[:,'Count'] = df.groupby(group_list)['Pos'].transform('count')
    # SELECT ONLY RELEVANT ROWS
    df = df[df['Count'] > 1]

    # DF INFORMATION
    print("Library df has:",df.shape[0],"dupe tracks\n")

    # SORTS 
    df = df.sort_values(["Count","Arq2","Pos"])
    # Group by columns A and B and assign a unique number to each row within the group
    df['N'] = df.groupby(group_list).cumcount() + 1
    # TAKES THE MAX OF THE ADDED DATE
    df.loc[:,'min_N'] = df.groupby(group_list)['N'].transform('min')

    # SAVES DUPES TO AN EXCEL FILE
    # file_nm = "D:\\iTunes\\Excel\\Dupes.xlsx"
    # save the dataframe to an Excel file
    #df.to_excel(file_nm, index=False)

    # REFRESHES LISTS 
    Arq = [x for x in df['Arq']]
    PID = [x for x in df['PID']]
    N = [x for x in df['N']]
    min_N = [x for x in df['min_N']]
    nbr_files = len(Arq)

    # COUNTS HOW MANY TRACKS WILL BE REMOVED
    Remove_l = [i for i in range(nbr_files) if N[i]>min_N[i]]
    nbr_dupes = len(Remove_l)

    # DUPES
    print("Dupe tracks to be deleted:",nbr_dupes)
    
    # 1o PL
    if nbr_dupes>0:
       Dupes_PL_nm = "Full_Dupes"
       PL_nm = Read_PL.Cria_PL(Dupes_PL_nm,recria="Y")

    # ADDS DUPE TRACKS TO A PL 
    # IT DOESN'T ADD TRACKS WITH MISSING FILES
    miss = 0
    for i in range(nbr_files):
        print("Adding",i+1,"of",nbr_files,"dupe files")
        m = Read_PL.unpack('!ii', Read_PL.a2b_hex(PID[i]))
        track = App.LibraryPlaylist.Tracks.ItemByPersistentID(*m)
        Read_PL.Add_track_to_PL(PLs,Dupes_PL_nm,track)
        if not exists(Arq[i]):
           miss = miss+1

    print("\nThere's",miss,"missing files out of",nbr_files,"\n")

    # REMOVES DUPES
    removed = 0
    for j in range(nbr_dupes):
        i = Remove_l[j]
        print("Checking file",j+1,"of",nbr_dupes,":",Arq[i])
        m = Read_PL.unpack('!ii', Read_PL.a2b_hex(PID[i]))
        track = App.LibraryPlaylist.Tracks.ItemByPersistentID(*m)
        try:
            track.delete()
        except:
            pass
        else:
            removed = removed+1
            print("Removed",removed,"dupe files of",nbr_dupes,":",Arq[i],"\n")
                      
    # FINAL
    print("Removed:",removed,"dupes of",nbr_dupes,"files\n")
    # print("Different dir:",len(Diff_dir),"\n")

    # STATS HAVE TO GO HERE OTHERWISE THEY CAN'T BE SEEN
    print("Dupe files that should've been removed:",nbr_dupes,"of",nbr_files,"(",df['Arq2'].nunique(),"unique files)\n")
    

# CHAMA PROGRAM
Remove_full_dupes(rows=None)
