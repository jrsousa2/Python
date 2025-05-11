# TRIES TO RESOLVE THE CONFLICT BETWEEN TAG AND FILE NAMES
from os.path import exists
from os import rename
from re import sub
import time
import Tags
import Busca
import Read_PL

# QUANDO EXISTIR TANTO A TAG QUANTO O FILENAME, USAR O QUE TIVER MAIS PALAVRAS

# MAIN CODE
def Fix_conflict():
    
    # CALLS FUNCTION
    col_names =  ["Arq","Art","Title","AA","Album","Genre", "Year"]
    dic = Read_PL.Read_PL(col_names,PL_nbr=49)
    playlists = dic['PLs']
    tracks = dic['tracks']
    df = dic['DF']
    
    #override_art=False
    # TEST LIST CREATION (list comprehension) 
    Pos = [x for x in df['Pos']]
    Arq = [x for x in df['Arq']]
    Art = [x for x in df['Art']]
    Title = [x for x in df['Title']]
    AA = [x for x in df['AA']]
    Album = [x for x in df['Album']]
    Genre = [x for x in df['Genre']]
    Year = [x for x in df['Year']]

    # List of dictionaries
    main_dic = []
    for i in range(0,len(Arq)):
        dic = {'Arq': Arq[i],'Art': Art[i],'Title': Title[i],'AA': AA[i],'Album': Album[i],'Genre': Genre[i], 'Year': Year[i]}
        main_dic.append(dic)


   # CREATES THE PLAYLISTS
    Read_PL.Create_PL("Right_Both",recreate="y")
    Read_PL.Create_PL("Right_Filename",recreate="y")
    Read_PL.Create_PL("Right_Tags",recreate="y")

    # Initializes list
    to_fix_dic = []
    # CHECKS IF TRACK HAS ART:
    print("Creating list of files that will be checked\n")
    for i in range(0,len(Arq)):
        if exists(Arq[i]):
           m = Pos[i]
           track = tracks.Item(m)
           # CREATES VARS TO USE
           subdir = Tags.Folder(Arq[i])
           file_no_nbr_no_ext = Tags.File_no_nbr_no_ext(Arq[i])
           tag_matches_file = Tags.File_tag_comp(Arq[i],Art[i],Title[i],Genre[i])

           if not tag_matches_file:
              to_fix_dic.append(i)

    print("Files that will be checked:",len(to_fix_dic))
    print("")

    # Initiliazes issue counts
    fixed = {}
    fixed['Searched'] = 0
    fixed['No_result'] = 0
    fixed['Entries'] = 0
    fixed['Found'] = 0
    fixed['Match_title'] = 0
    fixed['Match_album'] = 0
    fixed['Match_both'] = 0
    fixed['wrapper=track'] = 0
    fixed['wrapper=Album'] = 0
    fixed['wrapper=None'] = 0
    fixed['Json exc'] = 0
    fixed['Tags'] = 0
    fixed['Tie-tags'] = 0
    fixed['File'] = 0
    fixed['Tie-file'] = 0
    fixed['Both'] = 0
    fixed['None'] = 0
    fixed['Chgd loc'] = 0
    fixed['Chgd tags'] = 0
    fixed['Tie-Chgd loc'] = 0
    fixed['Tie-Chgd tags'] = 0
    fixed['Loc exc'] = 0
    
    for i in range(0,len(to_fix_dic)):
        n = to_fix_dic[i]
        m = Pos[n]

        if exists(Arq[n]):
            # first try to match by title
            busca = {}
            Achou_tags = Busca.Busca(i,main_dic[n],busca,fixed)
            time.sleep(2.2)
            
            busca = {}
            Achou_file = Busca.Busca(i,main_dic[n],busca,fixed,srch_by="file") 
            time.sleep(2.2)

            # QUANDO EXISTIR TANTO A TAG QUANTO O FILENAME, USAR O QUE TIVER MAIS PALAVRAS
            Tie = False
            if Achou_tags and Achou_file:
               fixed['Both'] = fixed['Both'] + 1
               Read_PL.Add_file_to_PL(playlists,"Right_Both",Arq[n])
               tag_aux = Art[n]+ " - " + Title[n]
               tag_l = tag_aux.split(" ")
               file_aux = Tags.File_no_nbr_no_ext(Arq[n])
               file_l = file_aux.split(" ")
               Tie = True
               Achou_tags = False
               Achou_file = False 
               if len(file_l)>len(tag_l):
                  Achou_file = True
               else:
                  Achou_tags = True

            if Achou_tags:   
               if not Tie:
                  fixed['Tags'] = fixed['Tags'] + 1
               else:
                  fixed['Tie-tags'] = fixed['Tie-tags'] + 1  
               Read_PL.Add_file_to_PL(playlists,"Right_Tags",Arq[n])
               # RENAMES FILE BASED ON THE TAGS
               dic = Tags.tag_2_file(Arq[n],Art[n],Title[n])
               subdir = dic['subdir']
               tag_no_sp_chars_ext = Tags.file_w_ext(dic['fname'])
               tag_no_sp_chars_ext = Tags.finds_valid_file(subdir,tag_no_sp_chars_ext)
               #tags_no_sp_chars = Stdz.file_wo_ext(tag_no_sp_chars_ext)

               track = tracks.Item(m)
               Loc = track.Location
               #tag_no_sp_chars_ext = finds_valid_file(subdir,file_w_ext)
               #nbr = 0
               #while exists(tag_no_sp_chars_ext):
               #      nbr = nbr+1
               #      tag_no_sp_chars_ext = subdir + tags_no_sp_chars + " ("+ str(nbr) +").mp3" 
               # After ensuring that the file doesn't exist, I can rename      
               try:
                  rename(Arq[n], tag_no_sp_chars_ext) 
               except Exception:
                  fixed['Loc exc'] = fixed['Loc exc'] + 1 
               else:
                     track.Location = tag_no_sp_chars_ext
                     if not Tie:
                        fixed['Chgd loc'] = fixed['Chgd loc'] + 1
                     else:
                        fixed['Tie-Chgd loc'] = fixed['Tie-Chgd loc'] + 1
            elif Achou_file:
                 if not Tie:
                    fixed['File'] = fixed['File'] + 1
                 else:
                    fixed['Tie-file'] = fixed['Tie-file'] + 1     
                 Read_PL.Add_file_to_PL(playlists,"Right_Filename",Arq[n])
                 subdir = Tags.Folder(Arq[n])
                 file = Tags.file_wo_ext(Arq[n])
                 Art_Title = file.split(" - ")
                 track = tracks.Item(m)
                 Loc = track.Location
                 if len(Art_Title)==2:
                    track.Artist = Art_Title[0]
                    track.Name = Art_Title[1]
                    if not Tie:
                       fixed['Chgd tags'] = fixed['Chgd tags'] + 1
                    else:
                       fixed['Tie-Chgd tags'] = fixed['Tie-Chgd tags'] + 1
            else:
                fixed['None'] = fixed['None'] + 1

    print("")
    for key in fixed:
        print("List: ",key,"->",fixed[key])
    print("")    

# CALL PGM
Fix_conflict()