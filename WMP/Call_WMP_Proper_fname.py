# UPCASES THE NAMES OF THE FILES IN THE WMP LIBRARY
# SO THAT THEY ARE NOT MISSED WHEN SEARCHED FROM AN ITUNES PL
# CAN ALSO TRY AND FIX THE DUPES IN A WMP PLAYLIST
# THE IDEA IS TO MOVE THE FILE OUT OF D:\MP3 AND PUT IT BACK
# THE ISSUE IS LOSING INFO ABOUT THE FILE (HENCE COUNTS AND DATE ADDED ARE ADDED TO EXT TAGS)
# IT DOESN'T WORK TO FIX THE DUPLICATES IN WMP PLAYLISTS

from os.path import exists
from os import rename
#import Read_PL
import WMP_Read_PL as WMP
import pandas as pd
import Proper
import Files


col_names =  ["Arq"]

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
def Proper_fname(PL_name=None,PL_nbr=None,Do_lib=False,rows=None, do_cnt=100):
    # WMP
    # CALLS Read_PL FUNCTION 
    print("\nReading the WMP playlist")
    dict = WMP.Read_WMP_PL(col_names,PL_name=PL_name,PL_nbr=PL_nbr,Do_lib=Do_lib,rows=rows,Modify_cols=False) 
    
    # WMP ASSIGNING
    df = dict["DF"]
    # USED IF INPUT IS THE WHOLE LIBRARY
    WMP_lib = dict["Lib"]
    # USED IF INPUT IS A PLAYLIST (BASED ON iTunes)
    WMP_player = dict["WMP"]

    # Close the player interface
    # WMP_player.close()

    # POPULATES LISTS
    Arq = [x for x in df["Arq"]]
    Pos = [x for x in df["Pos"]]
    nbr_files = len(Arq)

    print("\nThe WMP library df has",df.shape[0],"tracks")

    fix_cnt = 0
    path_mod = 0
    cant_move = 0
    # COMPARE AND CHANGE THE FILES
    fez = False
    for i in range(nbr_files):
        if (i+1) % 1000==1:
           print("\nChecking file",i+1,"of",nbr_files)
        track = WMP_lib.Item(Pos[i])
        # TRACK METADATA
        path = track.sourceURL
        folder = Files.Folder(path)
        file_no_ext = Files.file_wo_ext(path)
        file_no_ext = Proper.Proper(file_no_ext,"file")
        ext = Files.ext(path)
        New_location = folder + file_no_ext + ext
        #  or "Groove Addiction - Isto É Porno (Original Master)" in path
        if exists(path) and path != New_location and path.lower()==New_location.lower() and not fez and Files.Is_DMP3(path):
           print("From",Files.file_w_ext(path),"->",Files.file_w_ext(New_location))
           cols = ["Plays", "Added"]
           track_dict = WMP.WMP_sel_tags_dict(track,cols)
           plays = track_dict["Plays"]
           Added = track.getItemInfo("AcquisitionTime")
           temp_path = "D:\\JR\\" + file_no_ext + ext
           if not exists(temp_path):
              rename(path, temp_path)
              # temp_path = path
              # COUNTS
              prev_plays = Files.read_tag_mutag(temp_path, "WMP_PLAYS")
              if not prev_plays or int(prev_plays) < plays:
                 Files.write_tag(temp_path, "WMP_PLAYS", str(plays))
              # DATE ADDED
              prev_Added = Files.read_tag_muta(temp_path, "WMP_ADDED") 
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
           
           # track.setItemInfo("SourceURL", New_location)
           # print("Doublecheck SourceURL:",track.getiteminfo("SourceURL"))
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
Proper_fname(Do_lib=1, rows=None, do_cnt=300)

