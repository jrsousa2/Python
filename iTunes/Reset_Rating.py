# TRY TO RESET ALBUM RATING
from os.path import exists

import sys
sys.path.insert(0, "D:\\Python\\iTunes\Modules")
sys.path.insert(0, "D:\\Python\\WMP")

import Read_PL

def Upgrade(PL_name=None,PL_nbr=None):
    # CALLS FUNCTION "Art","Title","AA","Album"
    col_names =  ["Arq","Covers","AA","Album","ID"] 
    dict = Read_PL.Read_PL(col_names,PL_name=PL_name,PL_nbr=PL_nbr) 
    App = dict['App']
    playlists = dict['PLs']
    df = dict['DF']

    # ONLY DUPES WITH AT LEAST ONE NON-MISSING FILES
    group_list = ["AA","Album"]
    df['Max_arq'] = df.groupby(group_list)['Arq'].transform('max')
    
    # TEST LIST CREATION (list comprehension) 
    Arq = [x for x in df['Arq']]
    Max_arq = [x for x in df['Max_arq']]
    ID = [x for x in df['ID']]
    nbr_files = len(Arq)
    do_list = [i for i in range(nbr_files) if Arq[i]==Max_arq[i]]
    nbr_albums_reset = len(do_list)

    # STATS
    print("\nProcessing",nbr_albums_reset,"files\n")

    # READS PLAYLISTS
    fixed = 0
    for j in range(nbr_albums_reset):
        i = do_list[j]
        m = ID[i]
        track = App.GetITObjectByID(*m)
        print("Resetting album rating of",track.Location)
        track.AlbumRating = 0
  
# CALLS FUNC zzzzz-Albums
Upgrade(PL_name="iPhone-Flagged")


