# TRIES TO RESOLVE THE CONFLICT BETWEEN TAG AND FILE NAMES
# CREATES A PLAYLIST WITH MISMATCHES FOUND
# THIS WILL SOLVE SOME OF THE EASY MISMATCHES AS WELL
# ESSA EH A VERSAO EXPRESS
# TO USE THIS CODE, CREATE 3 PLAYLISTS FIRST, AS CREATING THEM FROM SCRATCH FAILS
# COMPARES IF FILENAMES MATCH THE TAGS (SYNCS FILENAMES WITH TAGS)

from os.path import exists
from os import rename
import Read_PL
import Proper
import Files
import Tags


# 1o ADICIONA TRACKS NA PLAYLIST
def file_vs_tags(PL_name=None,PL_nbr=None,Do_lib=False,rows=None):
   # CALLS FUNCTION
    col_names =  ["Arq","Art","Title","Genre", "ID"]
    dict = Read_PL.Read_PL(col_names,PL_name=PL_name,PL_nbr=PL_nbr,Do_lib=Do_lib,rows=rows)
    App = dict['App']
    playlists = dict['PLs']
    df = dict['DF']
    
    # TEST LIST CREATION (list comprehension) 
    Arq = [x for x in df['Arq']]
    Art = [x for x in df['Art']]
    Title = [x for x in df['Title']]
    Genre = [x for x in df['Genre']]
    ID = [x for x in df['ID']]
    nbr_files = len(Arq)

    to_fix = []
    # PLAYLIST NAMES
    Diff_PL_nm = "File_ne_Tags-quick"
    Diff_PL = Read_PL.Cria_PL(Diff_PL_nm, recria="n")

    # FIX  
    mismatch = 0
    fixed = 0
    for i in range(nbr_files):
        if exists(Arq[i]):
           tags = Art[i] + " - " + Title[i]
           filename = Files.file_wo_ext(Arq[i])
           print("\nChecking File",i+1,"of",nbr_files,"->",filename,"// Tags:",tags)
           m = ID[i]
           track = App.GetITObjectByID(*m)
           if track.location != Arq[i]:
              Erro = True 

           # CREATES VARS TO USE
           subdir = Files.Folder(Arq[i])
           file_no_nbr_no_ext = Files.File_no_nbr_no_ext(Arq[i])

           # 1ST APPROACH
           Title2 = Title[i].replace(" / ",", ")
           Title2 = Title2.replace(" \\ ",", ")
           tags2 = Files.Replace_spec_chars(Art[i] + " - " + Title2)
           file_no_nbr_no_ext = Files.File_no_nbr_no_ext(Arq[i])
           tag_matches_file0 = tags2.lower() == file_no_nbr_no_ext.lower()
           if tag_matches_file0:
              print("Adding flag to Grouping")
              Tags.Add_to_tag(track,"Tag_file_match",Tag="Group")

           # CHANGES EASIER ONES 
           tags2 = Files.Replace_spec_chars(Art[i] + " - " + Title2,"_")
           tags2 = tags2.replace(" ","_")
           file_no_nbr_no_ext = file_no_nbr_no_ext.replace(" ","_")
           tag_matches_file4 = tags2.lower() == file_no_nbr_no_ext.lower()
           dict = Tags.similar_ratio(tags, filename)
           ratio_obs = dict["ratio"]
           print("Similarity:",ratio_obs)
           if not tag_matches_file0 and (tag_matches_file4 or ratio_obs > 0.98):
              Read_PL.Add_track_to_PL(playlists,Diff_PL_nm,track)
              print("Changing filename:",filename + ".mp3")
              print("To->",Files.Replace_spec_chars(tags,"_") + ".mp3")
              dict = Tags.tag_2_file(Arq[i],Art[i],Title[i])  
              subdir = dict['Subdir']
              tag_no_sp_chars_ext = dict['Filename']
              New_path = subdir + tag_no_sp_chars_ext
              rename(Arq[i], New_path) 
              track.Location = New_path 
              fixed = fixed+1
              print("Filename fixed!\n")
              Tags.Add_to_tag(track,"Tag_file_match",Tag="Group") 


           # 1ST APPROACH
           tag_matches_file1 = Tags.File_tag_comp(Arq[i],Art[i],Title[i],Genre[i])

           # 2ND APPROACH 
           tag_matches_file2 = False
           if False and not tag_matches_file1:
              aux_dic = Tags.File_tag_comp2(Arq[i],Art[i],Title[i])
              tag_matches_file2 = aux_dic['res']

           # 3RD APPROACH 
           tag_matches_file3 = False
           if False and not tag_matches_file1 and not tag_matches_file2:
              aux_dic = Tags.File_tag_comp3(Arq[i],Art[i],Title[i])
              tag_matches_file3 = aux_dic['res']

           # The idea is to rename all the files that I know match (no missing words) based on the tags
           # If they don't match I can't do this, as it's possible a word is missing or artists don't match
           if False and not (tag_matches_file0 or tag_matches_file1 or tag_matches_file2 or tag_matches_file3):
              mismatch = mismatch + 1
              print("\nChecked",i+1,"\\ Mismatch:",mismatch,"\\ Fixed:",fixed)
              print("\nFilename:",filename)
              print("Tags:",tags)
              Read_PL.Add_track_to_PL(playlists,Diff_PL_nm,track)
              dict = Tags.similar_ratio(tags, filename)
              ratio_obs = dict["ratio"]
              print("Similarity:",ratio_obs)
              if ratio_obs > 0.60:
                  inp = ""
                  print("The file name and tags match:",ratio_obs)
                  inp = input("Press T to change tags // F to change filename: ")
                  if inp.upper()=="T":
                     print("Changing tags:",tags,"->",filename)
                     dict = Files.file_to_art_title(Arq[i])
                     Split_ok = dict['Ok']
                     New_art = dict['Art']
                     New_title = dict['Title']
                     if Split_ok and exists(Arq[i]):
                        modif = Tags.Rewrite_tags(track,New_art,New_title)
                        if modif:
                           fixed = fixed+1
                  elif inp.upper()=="F":
                     print("Changing filename:",filename + ".mp3")
                     print("To->",Files.Replace_spec_chars(tags) + ".mp3")
                     dict = Tags.tag_2_file(Arq[i],Art[i],Title[i])  
                     subdir = dict['Subdir']
                     tag_no_sp_chars_ext = dict['Filename']
                     New_path = subdir + tag_no_sp_chars_ext
                     rename(Arq[i], New_path) 
                     track.Location = New_path 
                     fixed = fixed+1
                     print("Filename fixed!\n")
           
           # DISPLAY INFO
           print("Fixed",fixed)

# CALLS FUNC
file_vs_tags(PL_name="zzz-sync",rows=None)