# REASSIGNS THE TRACKS TO MOVE LIBRARY TO ANOTHER DRIVE
# IN THIS VERSION IT MOVES THE FILES AS IT GOES
# IT DOESN'T USE THE XLM FILE TO IDENTIFY MISSING ID'S
# NOT FINISHED (TERMINAR SE FOR FAZER ISSO)

import Read_PL
import xml.etree.ElementTree as ET
import pandas as pd
from urllib.parse import unquote
from os.path import exists
import ctypes
from ctypes import wintypes

# XML COLS THAT WE WANT TO KEEP
keep_lst = ['Location','Track ID','Artist','Name']





    # INICIALIZA iTunes
    dict = Read_PL.Init_iTunes()
    App = dict['App']
    playlists = dict['PLs']


    # ITUNES ACTUAL LIBRARY
    col_names =  ["Art" , "Title", "ID"] 
    dict = Read_PL.Read_PL(col_names,Do_lib=True,rows=None) 
    App = dict['App']
    # PLs = dict['PLs']
    df_lib = dict['DF']

    ID = [x for x in df_lib["ID"]]
    Track_ID = [id[3]-1 for id in ID]

    df_lib['Track ID'] = Track_ID
    df_lib = df_lib.sort_values(by='Track ID', ascending=True)

    # Join df1 and df2 on the 'Track_no' column
    df = pd.merge(df_lib, df_xml, on='Track ID', how='inner')

    print("\nThe XML df has",df_xml.shape[0],"tracks")

    print("\nThe iTunes library has",df_lib.shape[0],"tracks")

    print("\nThe merged df has",df.shape[0],"tracks")

    # LIST CREATION (list comprehension) 
    Arq = [x for x in df['Location']]
    ID = [x for x in df["ID"]]
    # Assuming 'df' is your DataFrame and 'X', 'Y', 'Z', 'W' are the column names
    match = [(x == z) and (y == w) for x, y, z, w in zip(df["Artist"], df["Name"], df["Art"], df["Title"])]
    mismatch = [1 if not x else 0 for x in match]
    nbr_files = len(Arq)

    # GETS INPUT FROM USER
    Cur_drive = input("\nEnter the current drive:")
    Cur_drive = Cur_drive.strip()
    Dest_drive = input("\nEnter the destination drive:")
    Dest_drive = Dest_drive.strip()
    nbr_files_inp = input("\nNumber of files to move (1 to",nbr_files,") (blank for ALL):")
    if nbr_files != "":
       nbr_files = nbr_files_inp

    # PLAYLIST WITH MIGRATED FILES
    migrated_PL = "Migrated"
    call_PL = Read_PL.Cria_PL(migrated_PL,recria="n")

    # 1st CHECK
    print("\nUpdating file location from",Cur_drive,"to",Dest_drive)
    print("Misaligned files:",sum(mismatch),"\n")
    cnt = 0
    miss = 0
    up_to_date = 0
    found = []
    for i in range(nbr_files):
        New_loc = Arq[i].replace("/", "\\")
        New_loc = New_loc.replace(Cur_drive+":\\", Dest_drive+":\\")
        m = ID[i]
        track = App.GetITObjectByID(*m)
        if exists(New_loc) and match[i] and New_loc != Arq[i]:
           found.append(1)
           print("Updating",i+1,"of",nbr_files,":",Arq[i],"-> ",Dest_drive,":\\")
           track.location = New_loc
           Read_PL.Add_track_to_PL(playlists,"Moved",track)
           cnt = cnt + 1
        elif exists(New_loc):
           up_to_date = up_to_date+1
           found.append(1)
        else:
           miss = miss+1
           found.append(0)

    print("Updated",cnt,"of",nbr_files,"(",miss,"not found)")
    print(up_to_date,"files already up-to-date")
    df["Found"] = found

print("Saving dead tracks to Excel...")
file_nm = "D:\\iTunes\\Excel\\Dead_tracks.xlsx"
# save the dataframe to an Excel file
df_dead = df[ df["Found"] == 0]
df_dead.to_excel(file_nm, index=False)
