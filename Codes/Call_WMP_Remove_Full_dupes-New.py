# THIS WAS AN ATTEMPT TO REMOVE DUPES FROM PL's
# THE IDEA IS TO MOVE THE FILE OUT OUT THE FOLDER AND THEN PUT IT BACK
# BUT IT DOESN'T WORK, THE ISSUE MUST BE SOMETHING ELSE

from os.path import exists
from os import rename
import WMP_Read_PL as WMP
import pandas as pd
import Proper
import Files

col_names =  ["Arq"]

# THIS MODULE SETS ARQ TO LOWER CASE FOR THE MERGER
# IT ALSO DEDUPES THE DUPLICATE RECORDS
def df_dedupe(df):
    # MAKES A COPY OF THE ORIGINAL PATH LIST ("ARQ") 
    # BEFORE MAKING IT LOWER CASE
    df["Location"] = df["Arq"].copy()
    # LOWERCASE THE FILE NAME
    df["Arq"] = df["Arq"].str.lower()

    start_rows = df.shape[0]
    
    # GROUPS BY AND COUNT RECS
    df['Count'] = df.groupby(['Arq'])['Pos'].transform('count')

    # SELECT ONLY RELEVANT ROWS
    df = df[df['Count'] > 1]

    dupe_rows = df.shape[0]

    # Eliminate duplicate records based on "Arq" (subset=df["Arq"].str.lower() also works)
    df = df.drop_duplicates(subset="Arq", keep="first")

    end_rows = df.shape[0]
    print("\nInitially df has",start_rows,"tracks (",dupe_rows,"dupes and", end_rows,"deduped)")

    dict = {}
    dict["start_rows"] = start_rows
    dict["end_rows"] = end_rows
    dict["DF"] = df
    return dict

# MOVE FILES BACK AFTER THEY HAVE BEEN TAGGED
def Move_back(dir, WMP_player):
    # READ FOLDER -- AFTER MOVING FILES, OPEN WMP AND WAIT UNTIL IT UPDATES BEFORE RUNNING THIS
    files_tuple = Files.get_Win_files(dir, ".mp3")
    files = [file for (file,file_std) in files_tuple]
    orig_path_lst = []
    for path in files:
        orig_path = Files.read_tag_mutag(path, "WMP_PATH")
        # MOVE FILE INTO ORIGINAL FOLDER
        rename(path, orig_path)
        orig_path_lst.append(orig_path)
    
    # DO UNTIL THE LAST MOVED TRACK IS FOUND IN WMP
    ready = False
    last_moved = orig_path_lst[len(files)-1]
    while(not ready):
       try:
          # ASSIGNS TRACK IN WMP
          WMP_track = WMP_player.mediaCollection.getByAttribute("SourceURL", last_moved).Item(0)
       except:
          pass
       else:
          ready = True

    # AFTER MOVING FILES BACK, WAIT UNTIL WMP UPDATES
    for orig_path in orig_path_lst:
        pos = orig_path_lst.index(orig_path)+1
        nbr_files = len(orig_path_lst)
        # ASSIGNS TRACK IN WMP
        WMP_track = WMP_player.mediaCollection.getByAttribute("SourceURL", orig_path).Item(0)
        # RETRIEVE PLAYS CNT
        tag_plays = Files.read_tag_mutag(orig_path, "WMP_PLAYS")
        cur_plays = int(WMP_track.getItemInfo("UserPlayCount"))
        print("Updating",pos,"of",nbr_files,":",orig_path,":",cur_plays,"->",tag_plays)
        if tag_plays and int(tag_plays)>cur_plays:
           WMP_track.setItemInfo("UserPlayCount", tag_plays)
    print("\nFinished updating\n")

# MAIN CODE
# SRCH_MISS IS USED FOR DEAD TRACKS (NEEDS TO SCAN WHOLE LIBRARY TO BE ABLE TO DELETE TRACKS)
def Dedupe_PL(PL_name=None,PL_nbr=None,Do_lib=False,rows=None, do_cnt=100):
    # WMP
    # CALLS Read_PL FUNCTION 
    print("\nReading the WMP playlist")
    dict = WMP.Read_WMP_PL(col_names,PL_name=PL_name,PL_nbr=PL_nbr,Do_lib=Do_lib,rows=rows,Modify_cols=False) 
    
    # WMP ASSIGNING
    WMP_player = dict["WMP"]
    WMP_lib = dict["Lib"]
    # Read_PL = dict["PL"]
    df = dict["DF"]

    # DEDUPE DF
    dict = df_dedupe(df)
    df2 = dict["DF"]

    # POPULATES LISTS
    Arq = [x for x in df2["Location"]]
    Pos = [x for x in df2["Pos"]]
    nbr_files = len(Arq)

    print("\nThe playlist '",PL_name,"' has",nbr_files,"dupe tracks")

    fix_cnt = 0
    path_mod = 0
    cant_move = 0
    # COMPARE AND CHANGE THE FILES
    fez = False
    for i in range(nbr_files):
        print("\nChecking file",i+1,"of",nbr_files,":", Arq[i])
        track = WMP_player.mediaCollection.getByAttribute("SourceURL", Arq[i]).Item(0)   
        # track = WMP_lib.Item(Pos[i])
        # track = Read_PL.Item(Pos[i])
        # TRACK METADATA
        path = track.sourceURL
        folder = Files.Folder(path)
        file_no_ext = Files.file_wo_ext(path)
        file_no_ext = Proper.Proper(file_no_ext,"file")
        ext = Files.ext(path)
        New_location = folder + file_no_ext + ext
        
        # BEGIN REMOVING FILES
        if exists(path) and not fez:
           print("From",Files.file_w_ext(path),"->",Files.file_w_ext(New_location))
           cols = ["Plays", "Added"]
           track_dict = WMP.WMP_tag_dict(track,cols)
           plays = track_dict["Plays"]
           Added = track.getItemInfo("AcquisitionTime")
           temp_path = "D:\\JR\\" + file_no_ext + ext
           if not exists(temp_path):
              rename(path, temp_path)
              # COUNTS
              prev_plays = Files.read_tag_mutag(temp_path, "WMP_PLAYS")
              if not prev_plays or int(prev_plays) < plays:
                 Files.write_tag(temp_path, "WMP_PLAYS", str(plays))
              # DATE ADDED
              prev_Added = Files.read_tag_mutag(temp_path, "WMP_ADDED") 
              if not prev_Added: # or pd.to_datetime(prev_Added, format="%d/%b/%Y %I:%M:%S %p") < :
                 Files.write_tag(temp_path, "WMP_ADDED", Added)
              # PATH
              prev_path = Files.read_tag_mutag(temp_path, "WMP_PATH")  
              if not prev_path:
                 Files.write_tag(temp_path, "WMP_PATH", New_location)
              fix_cnt = fix_cnt+1
              if fix_cnt>=do_cnt:
                 fez = True
           else:
              cant_move = cant_move+1   
           
        if path.lower() != New_location.lower():
           path_mod = path_mod+1 

    print("\nMoved",fix_cnt,"files\n")
    # CALL CODE THAT MOVES FILES BACK
    if fix_cnt>0:
       Move_back("D:\\JR", WMP_player)   

        
    print("\nFixed case of",fix_cnt,"out of",nbr_files,"files")
    print(cant_move,"files that can't be moved")
    print("Path would be modified for",path_mod,"files\n")

# CALLS PROGRAM 
Dedupe_PL(PL_name="Favorites-Easy", Do_lib=0, rows=None, do_cnt=30)

