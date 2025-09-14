# TRIES TO RESOLVE THE CONFLICT BETWEEN TAG AND FILE NAMES
# TO USE THIS CODE, CREATE 3 PLAYLISTS FIRST, AS CREATING THEM FROM SCRATCH FAILS (IS THIS STILL NEEDED?)
# COMPARES IF FILENAMES MATCH THE TAGS (SYNCS FILENAMES WITH TAGS)
from os.path import exists
from os import rename
import Call_Proper
import Read_PL
import Tags
import Files

Log_file = "D:\\Python\\Sync_Tag_vs_file_log.txt"

# 1o ADICIONA TRACKS NA PLAYLIST
def file_vs_tags(PL_name=None,PL_nbr=None,Do_lib=False):

   # CALLS FUNCTION
    col_names =  ["Arq", "ID"]
    dict = Read_PL.Read_PL(col_names,PL_name=PL_name,PL_nbr=PL_nbr,Do_lib=Do_lib)
    App = dict["App"]
    playlists = dict["PLs"]
    df = dict["DF"]

    # TEST LIST CREATION (list comprehension) 
    Arq = [x for x in df["Arq"]]
    ID = [x for x in df["ID"]]
    nbr_files = len(Arq)
  
    confirm = False
    # PLAYLIST NAMES
    Diff_PL_nm = "B_File_ne_Tags"
    File_PL_nm = "B_File_renamed"
    Tag_PL_nm = "B_Tag_renamed"

    method_desc = {}
    method_desc[1] = "Perfect match"
    method_desc[2] = "Eq Title/diff Art"
    method_desc[3] = "Superset"
    method_desc[4] = "Similarity ratio"

    # CRIA PLAYLISTS 
    Diff_PL = Read_PL.Create_PL(Diff_PL_nm, recreate="n")
    File_PL = Read_PL.Create_PL(File_PL_nm, recreate="n")
    Tag_PL = Read_PL.Create_PL(Tag_PL_nm, recreate="n")

    # INICIALIZA
    fixed = {}
    tag_chg = {}
    loc_chg = {}
    fixed["Match"] = 0
    fixed["Mismatch"] = 0
    fixed["Exc"]  = 0
    for i in range(4):
        tag_chg[i+1] = 0
        loc_chg[i+1] = 0

    Files.Print_to_file(Log_file,"\n\n\nTIME: {}\n", Files.track_time())
    # BEGIN
    for i in range(nbr_files):
        if exists(Arq[i]) and Files.Is_DMP3(Arq[i]):
           m = ID[i]
           track = App.GetITObjectByID(*m)
           tag_song = track.Artist + " - " + track.Name
           print("\nChecking file",i+1,"of",nbr_files,"->",Arq[i])
           print("Tags->", tag_song)
           
           dict = Tags.file_tag_comp(track)
           match = dict["match"]
           method = dict["method"]

           # ONLY CASES 2 AND 3 LEAD TO CHANGING THE TAGS (1 CHNAGES THE FILE NAME INSTEAD)
           if match and "Tag_file_match" not in track.Grouping and dict["best"] != "file":
              print("Winning method:",method,"(",method_desc[method],") Best:",dict["best"])
              Files.Print_to_file(Log_file,"\n\nChecking file {} of {} -> {}", i+1, nbr_files, Arq[i])
              Files.Print_to_file(Log_file,"\nTags -> {}", tag_song)
              Files.Print_to_file(Log_file,"\nWinning method: {} ({}) - Best: {}", method, method_desc[method],dict["best"])
              
              fixed["Match"]=fixed["Match"]+1
              synced = False
              # RENAMES TAGS WITH THE FILENAME
              if dict["best"]=="file":
                 New_art = dict["Art"]
                 New_title = dict["Title"]
                 updt = Tags.Rewrite_tags(track,New_art,New_title)
                 if updt:
                    Read_PL.Add_track_to_PL(playlists,Tag_PL_nm,track)
                    tag_chg[method] = tag_chg[method] + 1
                    synced = True
              # FILE AND TAG WERE ALREADY IN SYNC      
              elif dict["best"]=="both":
                   synced = True      
              # RENAMES FILE WITH THE TAGS
              elif dict["best"]=="tags":
                  dict2 = Tags.tag_2_file(track)
                  subdir = dict2["Subdir"]
                  tag_no_sp_chars_ext = dict2["Filename"]
                  tags_no_sp_chars = Files.file_wo_ext(tag_no_sp_chars_ext)
                  tags_no_sp_chars = Call_Proper.Call_Proper(tags_no_sp_chars,Tag="file")

                  # But the files can still be different, if they are, rename and update location
                  # CARACTERES ESPECIAIS NAO CONTAM, SAO "", FAZER COM QUE NAO DE DIFERENCA AQUI
                  track_path = track.Location

                  # CHECK IF TAGS ARE EQUAL FILE NAME
                  # CREATES VARS TO USE
                  # subdir = Files.Folder(Arq[i])
                  file_no_nbr_no_ext = Files.File_no_nbr_no_ext(track_path)
                  file_no_nbr_no_ext = Call_Proper.Call_Proper(file_no_nbr_no_ext,Tag="file")
                  
                  # Maybe only the case of the file name is changing
                  Tags_eq_file_case_insen = tags_no_sp_chars.lower().replace(" ", "") == file_no_nbr_no_ext.lower().replace(" ", "")

                  if not Tags_eq_file_case_insen:
                     # Finds non-overwriting file (NOTE THE BELOW HAS EXTENSION, UNLIKE THE ONE ABOVE)
                     tag_no_sp_chars_ext = Files.file_w_ext(tag_no_sp_chars_ext)
                     tag_no_sp_chars_ext = Files.finds_valid_file(subdir,tag_no_sp_chars_ext)

                     file_from = Files.file_wo_ext(track_path)
                     file_to = Files.file_wo_ext(tag_no_sp_chars_ext)
                     print("\tChanging file name:",Files.file_wo_ext(track_path),"->",Files.file_wo_ext(tag_no_sp_chars_ext),"\n")
                     Files.Print_to_file(Log_file,"\nChanging file name: {} -> {}", file_from, file_to)
                     inp = ""
                     if confirm:
                        inp = input("Press Enter to change file name/path: ")
                     
                     # RENAMES FILE   
                     if inp=="":   
                        try:
                           rename(track_path, tag_no_sp_chars_ext) 
                        except Exception:
                           fixed["Exc"] = fixed["Exc"] + 1 
                        else:
                           synced = True
                           track.Location = tag_no_sp_chars_ext
                           Read_PL.Add_track_to_PL(playlists,File_PL_nm,track)
                           loc_chg[method] = loc_chg[method] + 1
              if synced:
                 Tags.Add_to_tag(track,"Tag_file_match",Tag="Group")         
           
           # DOESN'T MATCH not match
           # if dict["best"] != "both" and "Tag_file_match" in track.Grouping:
           if not match:   
              Read_PL.Add_track_to_PL(playlists,Diff_PL_nm,track)
              fixed["Mismatch"] = fixed["Mismatch"] + 1
           
    # SAINDO DO LOOP    
    print("\nFiles where name doesn't match tags:",fixed["Mismatch"],"(match:",fixed["Match"],")\n")
    Files.Print_to_file(Log_file,"\n\nFiles where name mismatches tags: {} (match {})", fixed["Mismatch"], fixed["Match"])

    Files.Print_to_file(Log_file,"\n\nFinal STATS:")
    for key in fixed:
        print("Final STATS:",key,"->",fixed[key])
        Files.Print_to_file(Log_file,"\nKey: {} -> {}", key, fixed[key])
    print()    
    Files.Print_to_file(Log_file,"\n\nTag updates:")
    for key in tag_chg:
        if tag_chg[key] != 0:
           print("Tag updates:",key,"(",method_desc[key],")->",tag_chg[key])  
           Files.Print_to_file(Log_file,"\nKey: {} ({}) -> {}", key, method_desc[key], tag_chg[key])
    print()
    Files.Print_to_file(Log_file,"\n\nLocation updates:")
    for key in loc_chg:  
        if loc_chg[key] != 0:
           print("Location updates:",key,"(",method_desc[key],")->",loc_chg[key])  
           Files.Print_to_file(Log_file,"\nKey: {} ({}) -> {}", key, method_desc[key], loc_chg[key])
    print()

# CALLS FUNC
file_vs_tags(PL_name="AAA")