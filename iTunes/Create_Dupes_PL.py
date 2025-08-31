# IDENTIFIES DUPE SONGS (IGNORING PARTS BETWEEN BRACKETS)
# CREATES A PLAYLIST WITH THE DUPES

import pandas as pd
from os.path import exists

import sys
sys.path.insert(0, "D:\\Python\\iTunes\Modules")
sys.path.insert(0, "D:\\Python\\WMP")

import Read_PL
import Tags
from Files import file_wo_ext

# DISABLE PANDAS WARNINGS
pd.options.mode.chained_assignment = None


# THIS MODULE TRANSFER TAGS SUCH AS YEAR, GENRE AND ALBUM WHEN THE ARTIST-TITLE MATCH
def Dupes_PL(rows=None):

    # READS XML
    col_names = ["Arq","Art","Title","Genre","PID", "Added", "Group"]

    # READ XML
    dict = Read_PL.Read_xml(col_names,rows=rows,track_time=True)
    App = dict['App']
    PLs = dict['PLs']
    df = dict['DF']

    # DISPLAY NUMBER OF ROWS
    print("\nThe df has",df.shape[0],"total files\n")

    # SELECT ONLY FAVORITES
    df = df[df["Genre"].str.contains("Favo", na=False)]

    # DISPLAY NUMBER OF ROWS
    print("The df has",df.shape[0],"favorite files\n")

    # SELECT ONLY NON DUPE-TAGGED (~ iIS FOR NOT)
    df = df[~df["Grouping"].str.contains("Dupe", na=False)]

    # DISPLAY NUMBER OF ROWS
    print("The df has",df.shape[0],"non dupe-tagged favorite files\n")

    # ADDS COL TO DF
    df["Title_std"] = df["Title"].str.rsplit("(", n=1).str[0].str.strip()

    # ADDS NEW COL.
    df["track_stdz"] = (df["Art"] + " & " + df["Title_std"]).map(Tags.Stdz)


    # CREATES COL. WITH STDZ TRACK NAMES
    # df.loc[:, "track_stdz"] = track_stdz
    df.loc[:, "Arq_lower"] = df['Arq'].str.lower()
    
    # SELECT ONLY TRACKS WHERE AT LEAST ONE OF THE DUPES IS NOT MISSING
    Arq = [x for x in df["Arq"]]
    nbr_files = len(Arq)

    # NON-MISSING FILES ONLY
    not_miss = [1*exists(Arq[i]) for i in range(nbr_files)]

    # ADDS NOT-MISSING COL. TO DF
    df.loc[:, "not_miss"] = not_miss
    
    # SELECT ONLY NON-MISSING FILES TO COUNT AS DUPES
    df = df[df["not_miss"] == 1]

    print("The df has",df.shape[0],"non-missing files\n")

    # COUNTS DISTINCT FILES PER GROUP
    df.loc[:, "Dist_files"] = df.groupby("track_stdz")["Arq_lower"].transform("nunique")
    
    # SELECT ONLY GROUPS WHERE THERE ARE MORE THAN 1 DISTINCT FILE (NO FALSE DUPE)
    df = df[(df["Dist_files"]>1)]

    print("After non-missing, the df has",df.shape[0],"dupes\n")

    # SORTS THE DF SO THE DUPES APPEAR AT THE TOP
    df = df.sort_values(["Dist_files","track_stdz", "Added"], ascending=[True, True, True])

    # REFRESHES TRACK LIST
    Arq = [x for x in df["Arq"]]
    PID2 = [x for x in df["PID2"]]
    nbr_files = len(Arq)

    # CRIA PLAYLIST APENAS SE HOUVER ARQUIVOS 
    Dupes_PL_name = "Dupe_Files"
    if nbr_files>0:
       Dupes_PL = Read_PL.Create_PL(Dupes_PL_name,recreate="y")

    print("\nAdding dupe files to playlist\n") 

    # CREATES PLAYLIST
    PID = []
    for i in range(nbr_files):
        m = PID2[i]
        track = App.LibraryPlaylist.Tracks.ItemByPersistentID(*m)
        
        #track = App.GetITObjectByID(*m)
        file_exists = exists(Arq[i])
        if file_exists and Arq[i]==track.Location:
           print("Adding file ",i+1,"of",nbr_files,":",file_wo_ext(Arq[i]))
           Read_PL.Add_track_to_PL(PLs,Dupes_PL_name,track) 

# CALLS FUNCTION
Dupes_PL(rows=5000)