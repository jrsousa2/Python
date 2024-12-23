# REMOVE FILES THAT ARE COMPLETELY DUPLICATE
# THAT IS, THESE FILES ARE THE SAME, BUT ARE DUPLICATED IN THE PLAYLIST
# ADDED DATETIME AND OTHER ATTRIBUTES MAY DIFFER

import win32com.client
import pandas as pd
import WMP_Read_PL


# MAIN CODE
def Remove_dupes(PL_name=None,PL_nbr=None,Do_lib=False,rows=None):
    # CALLS FUNCTION
    col_names = ["Arq"]
    dict = WMP_Read_PL.Read_WMP_PL(col_names,PL_name=PL_name,PL_nbr=PL_nbr,Do_lib=Do_lib,rows=rows)
    
    # ASSIGNS
    wmp = dict['WMP']
    playlists = dict['PLs']
    Read_PL = dict['PL']
    df = dict['DF']
    library = dict['Lib']
    # list = [getattr(PL, 'name', None) for PL in playlists if PL is not None]

    # DF INFORMATION
    msg_source = "Library" if Do_lib else "Playlist"
    print()
    print(msg_source,"has:",df.shape[0],"tracks\n")

    # CHANGE POS TO INTEGER
    df['Pos'] = df['Pos'].astype(int)

    # CREATES COL. TO GROUP BY
    print("Creating lower fullnames list\n")
    df["Arq2"] = df['Arq'].str.lower()

    # ADD COUNT COL. AND SELECT
    group_list = ["PL_nbr","Arq2"]
    print("Calculating dupes\n")
    df.loc[:,'Count'] = df.groupby(group_list)['Pos'].transform('count')
    # SELECT ONLY RELEVANT ROWS
    df = df[df['Count'] > 1]

    # DF INFORMATION
    print(msg_source,"has:",df.shape[0],"dupe tracks\n")

    # SORTS 
    sort_group = group_list.copy()
    sort_group.insert(0, "Count")
    sort_group.append("Pos")
    df = df.sort_values(sort_group)

    # Group by columns A and B and assign a unique number to each row within the group
    df['N'] = df.groupby(group_list).cumcount() + 1

    # TAKES THE MAX OF THE ADDED DATE
    df.loc[:,'min_N'] = df.groupby(group_list)['N'].transform('min')

    # REFRESHES LISTS 
    Pos = [x for x in df['Pos']]
    Arq = [x for x in df['Arq']]
    N = [x for x in df['N']]
    min_N = [x for x in df['min_N']]
    PL_nbr = [x for x in df['PL_nbr']]
    PL_name = [x for x in df['PL_name']]
    unique_PL = list(set(PL_name))
    nbr_files = len(Arq)

    # COUNTS HOW MANY TRACKS WILL BE REMOVED
    #Keep_l = [i for i in range(nbr_files) if N[i]==min_N[i]]
    # REMOVE ONLY ONCE
    Remove_l = [i for i in range(nbr_files) if N[i]==min_N[i]]
    Remove_PL_l = [PL_name[i] for i in range(nbr_files) if N[i]>min_N[i]]
    nbr_dupes = len(Remove_l)

    # STATS HAVE TO GO HERE OTHERWISE THEY CAN'T BE SEEN
    print("Dupe files that should be removed:",nbr_dupes,"of",nbr_files)
    print(df['Arq2'].nunique(),"unique files\n")

    # RESULT BY PLAYLIST
    nbr_PLs = len(unique_PL)
    for i in range(nbr_PLs):
        print(i+1,")",unique_PL[i],":",PL_name.count(unique_PL[i]),"dupe tracks,",Remove_PL_l.count(unique_PL[i]),"to be deleted")
    
    # 1o PL
    if nbr_dupes>0:
       Dupes_PL_nm = "Dupes_new"

    removed = 0
    failed = 0
    for j in range(nbr_dupes):
        i = Remove_l[j]
        m = Pos[i]
        # m = Pos[i]-removed
        if not Do_lib:
           # Read_PL = playlists[PL_nbr[i]]
           track = Read_PL.Item(m)
        else:
           track = library[m]   
        ref_valid = track.sourceURL==Arq[i]
        print("Checking file:",Arq[i])
        # TRY TO REMOVE
        if ref_valid:
           try:
              if not Do_lib:
                 # DOESN'T WORK)
                 Read_PL.removeItem(track) 
              else:
                  wmp.mediaCollection.remove(track,True) 
              #media.setDelete(track,True)
           except:
                 failed = failed+1
           else:   
               removed = removed+1
               ret = wmp.mediaCollection.add(Arq[i]) 
           # STATS    
           print("Removed",removed,"dupe files of",nbr_dupes,"(",failed,"fails)\n")     

# CHAMA PROGRAM PL_name="Mp3-Not D:\mp3"
Remove_dupes(PL_name="Favorites")
