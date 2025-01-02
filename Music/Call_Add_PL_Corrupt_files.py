# THIS MODULE CREATES A PL FOR CORRUPT FILES 
# ALONG WITH THEIR POSSIBLE NON-CORRUPT VERSION
import pandas as pd
from os.path import exists
import Read_PL
import Tags
import sys

def Corrupt(PL=None):
    # CALLS Read_PL FUNCTION
    col_names =  ["Pos","Arq","Art","Title","Group"]
    dict = Read_PL.Read_PL(col_names,PL_nbr=PL)
    PLs = dict['PLs']
    PL_Name = dict['PL_Name']
    df = dict['DF']

    # CRIA PLAYLISTS
    PL_nm = "Corrupt_files"
    PL = Read_PL.Cria_PL(PL_nm,recria="y")

    # POPULATES LISTS
    Art = [x for x in df['Art']]
    Title = [x for x in df['Title']]
    nbr_files = len(Art)

    # REASSIGNS PLAYLIST BY NAME, SHOULDN'T BE A PROBLEM
    dict = Read_PL.Reassign_PL(PL_Name)
    tracks = dict['tracks']
    result = dict['PL_nbr']

    # Cria nova lista baseada nos nomes
    track_stdz = []
    for i in range(nbr_files):
        track_stdz.append(Tags.Stdz(Art[i])+"-"+Tags.Stdz(Title[i]))

    # CREATES COL. WITH STDZ TRACK NAMES
    df["track_stdz"] = track_stdz
    # FLAGS DUPES
    df.loc[:, 'Count'] = df.groupby('track_stdz')['Pos'].transform('count')

    # RESTRICTS DATA TO DUPE TRACKS
    # SELECT ONLY RELEVANT ROWS
    df = df[df['Count'] > 1]
    num_rows = len(df)

    # CREATES DF COL. CALLED key WITH 1's IF KW IS FOUND IN Group
    df.loc[df['Group'].str.lower().str.contains("erro"), "Erro"] = 1
    # GROUPS VALUES OF key COL CREATED ABOVE by track
    # CREATES COL AND SETS VALUE TO MAX OF OF THE PREVIOUS COL. BY track (=art+title)
    df.loc[:, 'max_Erro'] = df.groupby('track_stdz')["Erro"].transform('max')
    df.loc[:, 'max_Erro'] = df.max_Erro.fillna(0)


    # SORTS THE DF SO THE DUPES APPEAR AT THE TOP
    df = df.sort_values(['max_Erro', 'track_stdz'], ascending=[False, True])

    # RECREATES THE LISTS
    # Pos = [x for x in df['Pos']]
    Arq = [x for x in df['Arq']]
    Art = [x for x in df['Art']]
    Title = [x for x in df['Title']]
    # Group = [x for x in df['Group']]
    Count = [x for x in df["Count"]]
    nbr_files = len(Art)

    # CREATES LIST OF LISTS FOR EACH COL PREVIOUSLY CREATED
    # Erro = [x for x in df["Erro"]]
    max_Erro = [x for x in df["max_Erro"]]
    track_stdz = [x for x in df["track_stdz"]]

    # START
    add_cnt = 0
    # INVERTI A ORDEM
    for i in range(nbr_files):
        add_cnt = add_cnt+1
        # print("Count:",i)
        print (f"\r>> Count: {i+1} Added: {add_cnt}", end='', flush=True)
        #sys.stdout.flush()
        if Count[i]>1 and max_Erro[i]>0:
           Read_PL.Add_file_to_PL(PLs,PL_nm,Arq[i])
  
#CALLS FUNC
Corrupt()