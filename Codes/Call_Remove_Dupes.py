# REMOVES DUPES
# FIRST CREATES A PLAYLIST, THEN DELETES ALL FILES BUT THE FIRST ONE
# FIRST IN THE ORDER OF THE PLAYLIST
# SKIP FAVORITE FILES FIRST
# CODE CHECKS IF THE SIMPLE COUNT MATCHES THE COUNT OF DISTINCT FILES (NO DUPLICATES)
import pandas as pd
from os.path import exists
#from os import remove
from send2trash import send2trash
import Read_PL
import Tags
import Files

# DISABLE PANDAS WARNINGS
pd.options.mode.chained_assignment = None

Log_file = "D:\\iTunes\\Delete_dupes_log.txt"

def convert_to_sec(time_str):
    min, sec = map(int, time_str.split(":"))
    return 60*min + sec

# THIS MODULE TRANSFER TAGS SUCH AS YEAR, GENRE AND ALBUM WHEN THE ARTIST-TITLE MATCH
def Remove_dupes(PL_name=None,PL_nbr=None,Do_lib=False):

    # CALLS Read_PL FUNCTION ,Do_lib=True,rows=10
    col_names =  ["Arq","Art","Title","ID","Added"] 
    dict = Read_PL.Read_PL(col_names,PL_name=PL_name,PL_nbr=PL_nbr,Do_lib=Do_lib)
    # ASSIGNS
    App = dict["App"]
    PLs = dict["PLs"]
    df = dict["DF"]
    tracks = dict["tracks"]

    # POPULATES LISTS
    Art = [x for x in df["Art"]]
    Title = [x for x in df["Title"]]
    nbr_files = len(Art)

    # Cria nova lista baseada nos nomes
    # ANY TRACK IS INCLUDED, INCLUDING THOSE WITH MISSING FILE
    track_stdz = []
    for i in range(nbr_files):
        track_stdz.append(Tags.Stdz(Art[i]+" & "+Title[i]))

    # CREATES COL. WITH STDZ TRACK NAMES
    df.loc[:, "track_stdz"] = track_stdz
    df.loc[:, "Arq_lower"] = df['Arq'].str.lower()
    # FLAGS DUPES
    df.loc[:, "Count"] = df.groupby("track_stdz")["Pos"].transform("count")
    df.loc[:, "Files"] = df.groupby("track_stdz")["Arq_lower"].transform("nunique")
    

    print("\nPrior to selection, df has",df.shape[0],"rows\n")

    # SELECT ONLY RELEVANT ROWS
    df = df[(df["Count"] > 1) & (df["Count"] == df["Files"])]

    print("The df has",df.shape[0],"dupes\n")

    # SELECT ONLY TRACKS WHERE AT LEAST ONE OF THE DUPES IS NOT MISSING
    Arq = [x for x in df["Arq"]]
    nbr_files = len(Arq)

    # NON-MISSING
    not_miss = [1*exists(Arq[i]) for i in range(nbr_files)]
    # ADDS NOT-MISSING COL. TO DF
    df.loc[:, "not_miss"] = not_miss
    
    # SELECT ONLY NON-MISSING FILES TO COUNT AS DUPES
    df = df[df["not_miss"] == 1]

    print("The df has",df.shape[0],"non-missing files\n")

    # RECALCULATES THE COUNT
    df.loc[:, "Count"] = df.groupby("track_stdz")["Pos"].transform("count")

    # SELECT ONLY RELEVANT ROWS
    df = df[df["Count"] > 1]

    print("After non-missing, the df has",df.shape[0],"dupes\n")

    # CHECKS COVERS ONLY FOR THE DUPES
    ID = [x for x in df["ID"]]
    nbr_files = len(ID)

    # RE-BUILDING OTHER LISTS 
    print("Building tags lists\n")
    #tracks_lst = [playlists.ItemByName(PL_list[i]).Tracks.Item(Pos[i]) for i in range(nbr_files)]
    tracks_lst = [App.GetITObjectByID(*ID[i]) for i in range(nbr_files)]
    list = ["Bitrate","Len"]
    for key in list:
        Col = [getattr(tracks_lst[i], Read_PL.iTu_tag_dict[key]) for i in range(nbr_files)]
        # ADDS TO THE DF
        df.loc[:, key] = Col

    # CREATE TIME IN SECS df["Sec"] 
    df.loc[:, "Sec"] = df["Len"].apply(convert_to_sec)

    # EXCLUDE PAIRS WHERE THE MAX DIFF IN SEC IS GREATER THAN 2 SEC
    df.loc[:, "Max_sec"] = df.groupby("track_stdz")["Sec"].transform("max")
    df.loc[:, "Min_sec"] = df.groupby("track_stdz")["Sec"].transform("min")
    df.loc[:, "Diff"] = df["Max_sec"] - df["Min_sec"]
    
    # MAX DIFF
    max_diff = 3
    df = df[df["Diff"] <= max_diff]
    print("The df has",df.shape[0],"dupes whose difference is less than",max_diff,"seconds\n")

    # SORTS THE DF SO THE DUPES APPEAR AT THE TOP
    df = df.sort_values(["Count","track_stdz","Bitrate", "Added"], ascending=[True, True, False, True])

    # ADD ORDERING COL.
    df['N'] = df.groupby("track_stdz").cumcount() + 1
    df.loc[:,'min_N'] = df.groupby("track_stdz")['N'].transform('min')

    # REFRESHES TRACK LIST
    Arq = [x for x in df["Arq"]]
    ID = [x for x in df["ID"]]
    nbr_files = len(Arq)

    # CRIA PLAYLIST APENAS SE HOUVER ARQUIVOS 
    Created_PL_name = "Dupe_Files"
    if nbr_files>0:
       Move_PL = Read_PL.Cria_PL(Created_PL_name,recria="y")

    # CREATES PLAYLIST
    PID = []
    for i in range(nbr_files):
        m = ID[i]
        track = App.GetITObjectByID(*m)
        file_exists = exists(Arq[i])
        if file_exists and Arq[i]==track.Location:
           print("Adding file:",i+1,"of",nbr_files,":",Files.file_wo_ext(Arq[i]))
           Read_PL.Add_track_to_PL(PLs,Created_PL_name,track) 

    print("\nPreparing list of files to delete\n") 
    # PREPARING TO DELETE THE FILES
    N = [x for x in df['N']]
    min_N = [x for x in df['min_N']]
    to_del_lst = [i for i in range(nbr_files) if N[i]>min_N[i]]
    nbr_files_del = len(to_del_lst)

    # DELETE
    for j in range(nbr_files_del):
        i = to_del_lst[j]
        print("Deleting file",j+1,"of",nbr_files_del,":",Arq[i])
        send2trash(Arq[i])

#CALLS FUNC   PL_nbr="8,33"
Remove_dupes(PL_name="BBB",Do_lib=0)