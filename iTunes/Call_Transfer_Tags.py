# TRANSFERS TAGS BETWEEN FILES
# AQUI DO_DEAD NAO EH MAIS NECESSARIO (JA EXISTE UM PGM ESPECIALMENTE PRA ISSO)
# THERE IS NO NEED TO ONLY DO THIS FOR FILES IN FOLDER MP3
# FOR THE ALBUM, THE COVER IS DELETED IF A MATCHING FILE HAS A BETTER COVER
# IT"S BASED ON A SCORE (BASED ON AA, GENRE, NICE COVER, NOVELA, COVER DIMENSIONS, ETC.)  
# THE COVER IS ATTACHED BASED ON THE BEST SCORE COVER
# I AM NOT CHECKING IF THE FILE EXISTS, AND THE REASON IS CAUSE
# IF TRACKS ARE MISSING, I CAN STILL RETRIEVE THEIR INFORMATION
# COVER INFORMATION IS NOT BEING PULLED IN THE READ_PL CODE
# THE REASON IS CAUSE I ONLY NEED COVER INFO FOR DUPE TRACKS
# A FAZER: COLOCAR IMPROVEMENT PARA LER DUAS PLAYLISTS AO MESMO TEMPO
# Remove Dead tracks (run with whole library for this)
# (removes files that were deleted if they have a match
# with a file that is not missing exists by artist/title).
import pandas as pd
from os.path import exists
from re import match
import Read_PL
import Tags
import Images
import Files
#from Images import hei, wid
# DISABLE PANDAS WARNINGS
pd.options.mode.chained_assignment = None  # default="warn"

# This program will receive a DF and check which files can have tags or art transferred

Log_file = "D:\\Python\\Transfer_tags_log.txt"

# USED FOR GENRES COMPARISON
Genres = ["Favorite","Easy","Novela","Brasil","Tribal","Flash House","Acid House","House","Trance", \
          "Rock","Hip-Hop","Soul","Disco","OneHitWonders","Jovem Pan","R&B","MPB","Rap"]

Priority_lst = ["Alb_not_miss", "Alb_by_art_vl", "Has_cover", "Nice_cover_vl", "Alb_not_great", \
                "Is_novela", "One_hit_wonders", "Is_Now", "Ratio", "Dim600", "Dim550", "Dim500", "Dim450", "Dim400"]

digits = len(Priority_lst)

# THIS CALCULATES A SCORE THAT TELLS ME WHICH COVER IS BETTER
def track_cover_score(track):
    Arq = track.Location
    Art = track.Artist
    Title = track.Name
    Cur_AA = track.AlbumArtist
    Cur_Album = track.Album
    Cur_Genre = track.Genre
    Cur_Group = track.Grouping
    Artobj = track.Artwork
    Artobj_Count = Artobj.Count
    if Artobj_Count>0:
       dict = Images.Img_dims(Arq)
       Has_cover = dict["Has_cover"]
    else:
        Has_cover = False   
    Hei = 0
    Wid = 0
    if Has_cover:
       Hei = dict["Hei"]
       Wid = dict["Wid"]
    # Stdz.Is_DMP3(Arq[i])
    Dim600 = 0
    Dim550 = 0
    Dim500 = 0
    Dim450 = 0
    Dim400 = 0
    Ratio = 0
    if Has_cover>0:
       Dim_not_big = Wid<=700 and Hei<=700
       Dim600 = Wid>=600 and Hei>=600 and Dim_not_big
       Dim550 = Wid>=550 and Hei>=550 and Dim_not_big
       Dim500 = Wid>=500 and Hei>=500 and Dim_not_big
       Dim450 = Wid>=450 and Hei>=450 and Dim_not_big
       Dim400 = Wid>=400 and Hei>=400 and Dim_not_big
       Ratio = min(Wid,Hei)/(max(Wid,Hei)+0.1)>=0.95 and Dim500
    Alb_not_miss = Cur_AA != "" and Cur_Album != ""
    Alb_by_art_vl = Tags.Alb_by_art(Art,Title,Cur_AA)
    Nice_cover_vl = Tags.Nice_cover(Cur_Album,Cur_Group,1*Has_cover) and not Alb_by_art_vl
    Alb_not_great = not Tags.Greatest_Hits(Cur_Album) and not Alb_by_art_vl
    Is_Now = Cur_Album.lower().find("now that's what")>=0
    One_hit_wonders = Cur_Album.lower().replace(" ", "").find("onehitwonder")>=0
    Is_novela = bool(match(r"^\d{4} -", Cur_Album))

    # CREATES LIST WITH FACTORS TO BE CONSIDERED IN THE ORDER OF THEIR PRIORITY    
    Priority = [Alb_not_miss, Alb_by_art_vl, Has_cover, Nice_cover_vl, Alb_not_great, \
                Is_novela, One_hit_wonders, Is_Now, Ratio, Dim600, Dim550, Dim500, Dim450, Dim400]
    score_aux = 0.0
    for i in range(len(Priority)):
        # LEAST POWER IS 0
        power = len(Priority)-i-1
        score_aux = score_aux + (10**power)*Priority[i]
    # Score2 is a dictionary that"ll be returned    
    score = {}
    score["score"] = score_aux
    score["ratio"] = Ratio
    score["alb_not_miss"] = Alb_not_miss
    score["alb_by_art"] = Alb_by_art_vl
    score["Has_cover"] = Has_cover
    return score

def Score_to_text(Score):
    score_txt = "{:0{width}}".format(int(Score), width=digits)
    return score_txt

def Compare_scores(bad_score,best_score):
    bad_score_txt = Score_to_text(bad_score)
    best_score_txt = Score_to_text(best_score)
    bad_lst = [int(digit) for digit in bad_score_txt]
    best_lst = [int(digit) for digit in best_score_txt]
    comp = [i if best_lst[i] > bad_lst[i] else digits+1 for i in range(digits)]
    min_pos = min(comp)
    return Priority_lst[min_pos]

##########################################################
    # ARTWORK 
    # CHECKS IF TRACK HAS ART:
    # ESSE SCORE VAI SER COMPUTADO PELA FUNCAO
    # Do CHECKS IF A TRACK CAN HAVE TAGS CHANGED
    # COVER IS ONLY CAPTURED FOR DUPES, FOR OTHERS IT"S MISSING (NONE)
    # COUNT IS 1 OR MORE (IF DUPE FILES WITH THE SAME ART/TITLE EXIST)
def Do_Covers(df):
    print("\nCreating lists of files that have cover\n")

    # RE-CREATES LISTS AFTER ORDER HAS CHANGED
    # AQUI TODAS AS TRACK ENTRAM, INDEPENDENTE DE SEREM MISSING
    Art = [x for x in df["Art"]]
    Covers = [x for x in df["Covers"]]
    # REFRESH LISTS
    Genre = [x for x in df["Genre"]]
    Album = [x for x in df["Album"]]
    # CALCULATED DO
    Do = []
    for i in range(nbr_files):
        Changeable_Year = not Tags.Genre_is_live(Genre[i]) and not Tags.forbid_art(Art[i]) and exists(Arq[i])
        Changeable_Album = Changeable_Year and not Tags.Nice_cover(Album[i],Genre[i],Covers[i])
        Do.append(Changeable_Album)

    # REDUCES THE LIST OF FILES TO BE PROCESSED
    nbr_files_to_updt = nbr_files

    # REMEMBER THAT THE LENGTH OF THE LIST CANNOT CHANGE
    Covers = []
    Score = []
    tam = nbr_files // 20
    for i in range(nbr_files):
        score_aux = 0
        Has_cover = None
        if (i+1) % tam==0:
            print("Calculated",i+1,"of",nbr_files,"scores")
        m = ID[i]
        track = App.GetITObjectByID(*m)
        # print("Calculando score",i+1,"de",nbr_dupes)
        dict = track_cover_score(track)
        score_aux = dict["score"]
        Has_cover = dict["Has_cover"]
        print("Arq",i+1,":",track.location," Score:",Score_to_text(score_aux))
        # ADDS SCORE    
        Score.append(score_aux)
        Covers.append(Has_cover)

    # ADDS COL. TO DF
    df["Covers"] = Covers
    # df["Covers"] = df["Covers"].astype(int)
    df["Score"] = Score

    # DROP COLUMNS AND PRINT THE DF ON THE SCREEN
    #df2 = df.drop(["Arq","Genre","track_stdz","Arq_lower","Art_sort","Title_sort","Priority"], axis=1)
    # PRINT
    #print(df2.to_string(index=False))

    # CONCATENATE AA+ALBUM
    df["AA@Album"] = df["AA"] +"@" + df["Album"]
    # MAX SCORE PER GROUP (i.e., STDZ ART+TITLE)
    # exemplo: df.loc[:, "max_Erro"] = df.groupby("track_stdz")["Erro"].transform("max")
    df.loc[:,"max_Score"] = df.groupby("track_stdz")["Score"].transform("max")
    # IT"S NOT POSSIBLE TO DO THIS WITH SCORES ONLY, IT REQUIRES A GROUPING
    df.loc[(df["Score"]==df["max_Score"]) & (df["Covers"] == True), "Best_alb_has_cover"] = 1
    df.loc[(df["Score"]==df["max_Score"]) & (df["Covers"] == False), "Best_alb_has_cover"] = 0
    
    # NOW CREATE A COLUMN TO FLAG IF ONE OF THE ALBUMS WITH MAX SCORE HAS A COVER
    # THIS IS A 0/1 FLAG (1 IT HAS, O IT DOESN"T)
    df.loc[:,"max_Best_alb_has_cover"] = df.groupby("track_stdz")["Best_alb_has_cover"].transform("max")
    
    
    # CREATES A COLUMN WHERE ONLY ROWS WITH THE MAX SCORE HAVE THE AA_ALBUM
    # HERE I CAN ONLY SELECT A BEST ALBUM WITH COVER
    df.loc[(df["Score"]==df["max_Score"]) & (df["max_Best_alb_has_cover"]==1) & (df["Covers"] == True), "New_Album"] = df["AA@Album"]
    # HERE I CAN SELECT ANY OF THE BEST ALBUMS
    df.loc[(df["Score"]==df["max_Score"]) & (df["max_Best_alb_has_cover"]==0), "New_Album"] = df["AA@Album"]
    df.New_Album = df.New_Album.fillna("")
    
    # FILLS ALL THE ROWS IN A GROUP WITH THE SAME NEW_ALBUM BY TAKING THE MAX OF PREVIOUS COL.
    df.loc[:,"max_New_Album"] = df.groupby("track_stdz")["New_Album"].transform("max")
    
    # LESSER SCORE ALBUMS RECEIVE THE MAX_NEW_ALBUM COL. FROM THE PREVIOUS STEP REGARDLESS OF BEST ALBUM HAS COVER
    df.loc[(df["Score"]<df["max_Score"]) & (df["Covers"]==False), "picked_Album"] = df["max_New_Album"]
    # LESSER SCORE ALBUMS  RECEIVE THE MAX_NEW_ALBUM COL. FROM THE PREVIOUS STEP IF THE BEST ALBUM HAS COVER
    df.loc[(df["Score"]<df["max_Score"]) & (df["Covers"]==True) & (df["max_Best_alb_has_cover"]==1), "picked_Album"] = df["max_New_Album"]
    df.picked_Album = df.picked_Album.fillna("")

    # DETERMINA TRACK WITH BEST ALBUM (PICKED ALBUM TEM QUE BATER COM O ALBUM DA BEST ALBUM TRACK)
    df.loc[(df["Score"]==df["max_Score"]) & (df["max_Best_alb_has_cover"]==1) & (df["Covers"] == True) & \
           (df["Count"]>1) & (df["max_New_Album"]== df["AA@Album"]), "Best_Album_track"] = df["Arq"] 
    # HERE I CAN SELECT ANY OF THE BEST ALBUMS
    df.loc[(df["Score"]==df["max_Score"]) & (df["max_Best_alb_has_cover"]==0) & \
           (df["Count"]>1) & (df["max_New_Album"]== df["AA@Album"]), "Best_Album_track"] = df["Arq"]
    df.Best_Album_track = df.Best_Album_track.fillna("")

    # NOW TAKE THE MAX OF THE PREVIOUS COL. (THAT'S WHY DF'S ARE SO HARD)
    # exemplo: df.loc[:, "max_Erro"] = df.groupby("track_stdz")["Erro"].transform("max")
    df.loc[:,"max_Best_Album_track"] = df.groupby("track_stdz")["Best_Album_track"].transform("max")

    # TEST LIST CREATION (list comprehension) 
    picked_Album = [x for x in df["picked_Album"]] 
    # Arq_lst = [x for x in df["Arq"]]
    Score = [x for x in df["Score"]]
    # max_Score = [x for x in df["max_Score"]]
    # lesser_score = [x for x in df["lesser_score"]]
    # Best_alb_has_cover = [x for x in df["Best_alb_has_cover"]]
    # max_Best_alb_has_cover = [x for x in df["max_Best_alb_has_cover"]]
    # Best_Album_track = [x for x in df["Best_Album_track"]]
    max_Best_Album_track = [x for x in df["max_Best_Album_track"]]


    # TROUBLESHOOT
    # df.to_excel("D:\\Python\\Excel\\Troubleshoot2.xlsx", index=False)

    # UPDATES THE LOG
    # ALBUMS THAT MAY CHANGE
    # CREATES LIST OF TRACKS WHOSE ALBUME NEED TO BE UPDATED
    do_list = [i for i in range(nbr_files) if picked_Album[i] != "" and Do[i]]
    # RETURN TO LIST
    nbr_files_to_updt = len(do_list)
    Files.Print_to_file(Log_file,"\n\nChecking {} albums whose covers may change ({})\n",nbr_files_to_updt,Files.track_time())
    print("\nTracks that may have covers updated:",nbr_files_to_updt,"\n") 

    # CRIA PLAYLISTS
    if nbr_files_to_updt>0:
       PL_nm = "Transfer_Albs"
       PL = Read_PL.Create_PL(PL_nm,recreate="n")

    # START
    fix_Album = 0
    for j in range(nbr_files_to_updt):
        i = do_list[j]
        # POSITION OF THE FILE WITH BEST COVER
        best_indice = Arq.index(max_Best_Album_track[i])
        # PRINT TO LOG
        print("Checking file",j+1,"of",nbr_files_to_updt,":",Arq[i])
        print("Best cover score:",Score_to_text(Score[best_indice]),"(File:",Arq[best_indice],")")
        print("Score of cover to be upgraded:",Score_to_text(Score[i]))
        attrib = Compare_scores(Score[i],Score[best_indice])
        print("The highest priority differing attribute is",attrib)
        Files.Print_to_file(Log_file,"\nChecking file {} of {}) ({})\n",j+1,nbr_files_to_updt,Files.track_time()) 
        Files.Print_to_file(Log_file,"File) {} Score: {}\n",Arq[i],Score_to_text(Score[i])) 
        Files.Print_to_file(Log_file,"Best cover score: {} (File: {})\n",Score_to_text(Score[best_indice]),Arq[best_indice])
        Files.Print_to_file(Log_file,"The highest priority differing attribute is: {}\n",attrib)
        m = ID[i]
        track = App.GetITObjectByID(*m)
        track_matches = track.location == Arq[i]
        dict2 = Tags.Split_AA_Album("","",picked_Album[i],delim="@")
        New_AA_vl = dict2["AA"]
        New_Album_vl = dict2["Album"]
        New_Album_ok = New_AA_vl  != "" and New_Album_vl != ""
        # CHANGES TAGS AND ATTACHES NEW COVER
        # and Arq[i].find("\\New\\")>=0
        if Do[i] and New_Album_ok and track_matches:
           # ATTACH COVER
           m = ID[best_indice]
           track_best_album = App.GetITObjectByID(*m)
           # JUST TO TEST WHICH FILE HAS THE BEST ALBUM
           best_track_matches = track_best_album.location==Arq[best_indice]
           # FIRST CHECKS IF THE COVER CAN BE DOWNLOADED FROM ITUNES
           dict = Images.Has_artwork(track_best_album)
           Has_new_cover = dict["Has_cover"]
           New_cover_file = dict["image"]
           if Has_new_cover and best_track_matches:
              dict = Images.Attach_cover(Log_file,track,New_AA_vl,New_Album_vl,New_cover_file,fix_Album) 
              if dict["Attached"]:
                 fix_Album = fix_Album+1
                 Best_group = "\\" + track_best_album.Grouping + "\\"
                 New_group = ""
                 Cur_group = track.Grouping
                 if Best_group.lower().find("\\ok\\")>=0:
                    New_group = Tags.Add_to_tag(track,"Ok",Tag="Group") 
                 if New_group != "":
                    # PRINTS ON SCREEN
                    print("Updated Group from",Cur_group,"->",New_group)
                    # ADD ENTRY TO LOG FILE
                    Files.Print_to_file(Log_file,"Updated Group from {}-> {}\n", Cur_group, New_group)
              # add track to PL 
              Read_PL.Add_track_to_PL(playlists,PL_nm,track)
        # BREAK LINE
        print()

    # PRINT FINAL COUNTS INFORMATION
    print("\nTracks that had Albums updated:",fix_Album,"\n")
#### END OF COVER - THE MOST CONVOLUTED 

#####################################################################
########################### YEAR LOGIC
def Do_Year(df):
    # YEAR LOGIC
    print("\nYear Update:\n")

    # RE-CREATES LISTS AFTER ORDER HAS CHANGED
    # AQUI TODAS AS TRACK ENTRAM, INDEPENDENTE DE SEREM MISSING
    Art = [x for x in df["Art"]]
    Genre = [x for x in df["Genre"]]
    # ADDITIONAL LISTS
    Year = [x for x in df["Year"]]

    # CALCULATED DO
    Do = []
    for i in range(len(Arq)):
        Changeable_Year = not Tags.Genre_is_live(Genre[i]) and not Tags.forbid_art(Art[i]) and exists(Arq[i])
        Do.append(Changeable_Year)

    # UPDATES THE LOG
    Files.Print_to_file(Log_file,"\n\nChecking Year tag: ({} files)\n",Files.track_time(),nbr_files)

    # CRIA COL. YR
    df.loc[df["Year"] != 0, "Year_gt_0"] = df["Year"]
    df.loc[df["Year"] == 0, "Year_gt_0"] = None

    # Minimo transformado .astype(int)
    df["min_Year"] = df.groupby("track_stdz")["Year_gt_0"].transform("min")
    df.min_Year = df.min_Year.fillna(0)
    df["min_Year"] = df["min_Year"].astype(int)

    # TEST LIST CREATION (list comprehension) 
    min_Year = [x for x in df["min_Year"]]
    # CHECKS and Arq[i].find("\\New\\")>=0
    do_list = [i for i in range(nbr_files) if (Year[i]==0 or (Year[i]>min_Year[i])) and min_Year[i] != 0 and Do[i]]
    nbr_files_to_updt = len(do_list)

    # PRINTS RESULT BEFORE UPDATE
    print("Tracks that may have Year tag updated:",nbr_files_to_updt,"\n")
    Files.Print_to_file(Log_file,"Tracks that may have Year tag updated: {}\n",nbr_files_to_updt)

    # CRIA PLAYLISTS
    if nbr_files_to_updt>0:
       PL_nm = "Transfer_Year"
       PL = Read_PL.Create_PL(PL_nm,recreate="n")

    # CREATES LIST OF TRACKS WHOSE YEAR IS NOT THE MIN YEAR
    fix_Year = 0
    for j in range(nbr_files_to_updt):
        i = do_list[j]
        # PRINT TO LOG
        print("Checking file",j+1,"of",nbr_files_to_updt,":",Arq[i])
        Files.Print_to_file(Log_file,"\nChecking file {} of {}) ({})\n",j+1,nbr_files_to_updt,Files.track_time()) 
        Files.Print_to_file(Log_file,"File) {}\n",Arq[i])
        file_nm = Files.file_wo_ext(Arq[i])
        # PLAYLIST
        m = ID[i]
        track = App.GetITObjectByID(*m)
        print("From",track.Year,"to",min_Year[i],"\n")
        if track.Location != Arq[i]:
           track = None 
        # TRY
        try: 
           track.Year = int(min_Year[i])
        except:   
            pass
        else:
            fix_Year = fix_Year+1
            # PRINTS ON SCREEN
            print("Updated Year of",file_nm)
            print("From",Year[i],"->",min_Year[i],"(",fix_Year,"updates)\n")
            # ADD ENTRY TO LOG FILE
            Files.Print_to_file(Log_file,"Updated Year of {}\n",file_nm)
            Files.Print_to_file(Log_file,"From {}-> {} ({} updates)\n", Year[i], min_Year[i], fix_Year)
            # add track to PL 
            Read_PL.Add_track_to_PL(playlists,PL_nm,track) 

    #print("")
    print("\nTracks that had Year updated:",fix_Year,"\n")
    Files.Print_to_file(Log_file,"\n\nTracks that had Year updated: {}\n",fix_Year)

#####################################################################
########################### GENRE LOGIC
def Do_Genre(df):
    # GENRE LOGIC
    print("\nGenre Updates\n")

    # RE-CREATES LISTS AFTER ORDER HAS CHANGED
    # AQUI TODAS AS TRACK ENTRAM, INDEPENDENTE DE SEREM MISSING
    Genre = [x for x in df["Genre"]]

    # UPDATES THE LOG
    Files.Print_to_file(Log_file,"\n\nChecking Genre tag ({} files): {}\n",nbr_files,Files.track_time())
    
    # LOGIC
    #print("")
    Cols = {}
    Max = {}
    for i in range(len(Genres)):
        Cols[Genres[i]] = Genres[i] + "_max"
    
    # GENRE LOGIC
    # FIRST CREATE A NEW COLUMN IN THE DF
    New_Genre = ["@" + x.lower().replace("\\","@") + "@" for x in Genre]
    df["New_Genre"] = New_Genre
    # PRINT ONLY SELECTED COLS OF THE DF
    # print(df.loc[:, ["Genre", "New_Genre"]])
    # FIX IS A DICTIONARY OF LISTS
    fix = {}
    for key in Cols:
        Str_to_look = "@"+key.lower()+"@"
        # CREATES DF COL. CALLED key WITH 1"s IF KW IS FOUND IN GENRE
        df.loc[df["New_Genre"].str.contains(Str_to_look), key] = 1
        # GROUPS VALUES OF key COL CREATED ABOVE by track
        # CREATES COL AND SETS VALUE TO MAX OF OF THE PREVIOUS COL. BY track (=art+title)
        df[Cols[key]] = df.groupby("track_stdz")[key].transform("max")
        # CREATES LIST OF LISTS FOR EACH COL PREVIOUSLY CREATED
        Max[key] = [x for x in df[Cols[key]]]
        fix[key] = []

    # CREATES LIST OF TRACKS GENRE NEEDS TO BE UPDATED
    dist_list = [i for i in range(nbr_files) for key in Cols if (New_Genre[i].find(key.lower())==-1 and Max[key][i]==1 and exists(Arq[i]))]
    dist_list = set(dist_list)
    dist_list.discard(None)
    # RETURN TO LIST
    do_list = list(dist_list)
    nbr_files_to_updt = len(do_list)

    # PRINTS RESULT BEFORE UPDATE
    print("Tracks that may have Genre tag updated:",nbr_files_to_updt,"\n")
    Files.Print_to_file(Log_file,"Tracks that may have Genre tag updated: {}\n",nbr_files_to_updt)

    # CRIA PLAYLISTS
    if nbr_files_to_updt>0:
       PL_nm = "Transfer_Genre"
       PL = Read_PL.Create_PL(PL_nm,recreate="n")

    # START
    fix_Genre = 0
    # INVERTI A ORDEM
    for j in range(nbr_files_to_updt):
        i = do_list[j]
        # PRINT TO LOG
        print("\nChecking file",j+1,"of",nbr_files_to_updt,Arq[i])
        Files.Print_to_file(Log_file,"\nChecking file {} of {}) ({})\n",j+1,nbr_files_to_updt,Files.track_time()) 
        Files.Print_to_file(Log_file,"File) {}\n",Arq[i]) 
        file_nm = Files.file_wo_ext(Arq[i])
        m = ID[i]
        track = App.GetITObjectByID(*m)
        Start_genre = track.Genre
        for key in Cols:
            Str_to_look = key.lower() # "@"+key.lower()+"@"
            if New_Genre[i].find(Str_to_look)==-1 and Max[key][i]==1 and track.Location==Arq[i]:
               Cur_genre = track.Genre
               # THE BELOW IS TO DOUBLECHECK
               if Cur_genre.find(Str_to_look)==-1 and Max[key][i]==1:
                  # Updates Genre
                  New_genre = Tags.Add_to_tag(track,key)
                  if New_genre != "":
                     fix_Genre = fix_Genre+1
                     fix[key].append(i)
        
        # PRINTS ON SCREEN
        End_genre = track.Genre
        print("Updated Genre from",Start_genre,"->",End_genre,"(",fix_Genre,"updates)")
        # ADD ENTRY TO LOG FILE
        Files.Print_to_file(Log_file,"Updated Genre from {}-> {} ({} updates)\n", Start_genre, End_genre, fix_Genre)
        # BREAK LINE PER FILE        
        print("") 
        Files.Print_to_file(Log_file,"")
    
    # ADD track to PL
    for j in range(nbr_files_to_updt):
        i = do_list[j]
        m = ID[i]
        track = App.GetITObjectByID(*m)
        Read_PL.Add_track_to_PL(playlists,PL_nm,track)
    
    # PRINTS
    print("\nFiles that had Genre updated:",nbr_files_to_updt,"\n")
    Files.Print_to_file(Log_file,"\nFiles that had Genre updated: {}\n",nbr_files_to_updt)
    # PRINTS A SUMMARY
    if fix_Genre>0:
       print("\nGenre Update summary:\n")
       Files.Print_to_file(Log_file,"\nGenre Update summary: {}\n\n",Files.track_time())

       # CHATGPT code
       # Calculate the number of tracks for each key
       track_counts = {key: len(value) for key, value in fix.items() if len(value) != 0}

       # Sort the keys by the number of tracks in descending order
       sorted_keys = sorted(track_counts.keys(), key=lambda key: track_counts[key], reverse=True)

       # Print the results in descending order of track count
       for key in sorted_keys:
           print("Tracks that had", key, "added to Genre:", track_counts[key]," Doublecheck:",len(fix[key]))
           Files.Print_to_file(Log_file,"Tracks that had {} added to Genre: {}\n",key,track_counts[key])
    
    #    for key in Cols:
    #        if len(fix[key]) !=0:
    #           print("Tracks that had",key,"added to Genre:",len(fix[key]))
    #           Files.Print_to_file(Log_file,"Tracks that had {} added to Genre: {}\n",key,len(fix[key]))
       print("")

#############################################################
########################### COUNTS LOGIC    
def Do_Counts(df):
    # COUNTS LOGIC
    print("\nCounts Update\n")

    # create a dictionary to store attribute names
    tag_dict = {"Plays": "PlayedCount", "Skips": "SkippedCount"}

    # RE-CREATES LISTS AFTER ORDER HAS CHANGED
    # AQUI TODAS AS TRACK ENTRAM, INDEPENDENTE DE SEREM MISSING
    Plays = [x for x in df["Plays"]]
    Skips = [x for x in df["Skips"]]

    # UPDATES THE LOG
    Files.Print_to_file(Log_file,"\n\nChecking Counts tags ({} files): {}\n",nbr_files,Files.track_time())
    
    # CREATES LIST OF TRACKS WHOSE PLAYS/SKIPS COUNT IS LESS THAN THE MAX
    # PLAY COUNT LOGIC
    Max = {}
    Cols = {}
    Metrics = ["Plays","Skips"]
    for i in range(len(Metrics)):
        Cols[Metrics[i]] = Metrics[i] + "_max"

    # INICIALIZA FIX (UM DICIONARIO DE LISTAS)
    fix = {}
    for key in Cols:
        # GROUPS VALUES OF key COL CREATED ABOVE by track
        # CREATES COL AND SETS VALUE TO MAX OF OF THE PREVIOUS max{Key} COL. BY track (=art+title)
        df[Cols[key]] = df.groupby("track_stdz")[key].transform("max").astype(int)
        # CREATES LIST OF LISTS FOR EACH COL PREVIOUSLY CREATED
        Max[key] = [x for x in df[Cols[key]]]
        fix[key] = []

    # CREATES LIST OF TRACKS WHOSE COUNTS NEED TO BE UPDATED
    # count_list = [i if (Plays[i] != Max[key][i] or Skips[i] != Max[key][i]) else None for i in range(nbr_files) for key in Metrics]
    Plays_l = [i for i in range(nbr_files) if (Plays[i] != Max["Plays"][i] and exists(Arq[i]))]
    Skips_l = [i for i in range(nbr_files) if (Skips[i] != Max["Skips"][i] and exists(Arq[i]))]
    dist_list = Plays_l + Skips_l
    dist_list = set(dist_list)
    dist_list.discard(None)
    # RETURN TO LIST
    do_list = list(dist_list)
    nbr_files_to_updt = len(do_list)

    # CRIA PLAYLISTS
    if nbr_files_to_updt>0:
       PL_nm = "Transfer_Counts"
       PL = Read_PL.Create_PL(PL_nm,recreate="n")

    # PRINTS RESULT BEFORE UPDATE
    print("Tracks that may have Count tags updated:",nbr_files_to_updt,"\n")
    Files.Print_to_file(Log_file,"Tracks that may have Count tags updated: {}\n",nbr_files_to_updt)

    # START
    fixed_count = {}
    fixed_count["Plays"] = 0
    fixed_count["Skips"] = 0
    for j in range(nbr_files_to_updt):
        i = do_list[j]
        # PRINT TO LOG
        print("Checking file",j+1,"of",nbr_files_to_updt,":",Arq[i])
        Files.Print_to_file(Log_file,"\nChecking file {} of {}) ({})\n",j+1,nbr_files_to_updt,Files.track_time()) 
        Files.Print_to_file(Log_file,"File) {}\n",Arq[i])
        track = tracks_lst[i]
        tag_assign = {"Plays": track.PlayedCount, "Skips": track.SkippedCount}
        for key in Metrics:
            Cur_count = tag_assign[key]
            # CHANGES TRACK COUNTS    
            if Cur_count < Max[key][i]:
               attr_name = tag_dict[key]
               # PRINTS
               print("Updating",key,"from",Cur_count,"->",Max[key][i],"(",fixed_count[key],"updates)")
               # ADD ENTRY TO LOG FILE
               Files.Print_to_file(Log_file,"Updated {} from {}-> {} ({} updates)\n",key, Cur_count, Max[key][i], fixed_count[key])
               # Uupdate the attribute value of the track object dynamically
               setattr(track, attr_name, Max[key][i])
               fixed_count[key] = fixed_count[key]+1    
               fix[key].append(i)
        # BREAK LINE
        print()
        Files.Print_to_file(Log_file,"\n")       
    
    # ADD TRACKS TO PL
    # DOESN"T NEED TO CHECK IF FILE EXISTS, MISSING FILES ARE NOT ADDED
    for j in range(nbr_files_to_updt):
        i = do_list[j]
        track = tracks_lst[i]
        Read_PL.Add_track_to_PL(playlists,PL_nm,track)

    # PRINTS A SUMMARY
    print("\nCounts Update summary:\n")
    Files.Print_to_file(Log_file,"\n\nCounts Update summary: {}\n",Files.track_time())
    for key in Cols:
        print("Tracks that had",key,"updated:",len(fix[key]))
        Files.Print_to_file(Log_file,"Tracks that had {} updated: {}\n",key,len(fix[key]))    

#############################################################
########################### DEAD TRACKS LOGIC    
def Do_Dead(df):
    # COUNTS LOGIC
    print("\nDead tracks removal\n")

    # UPDATES THE LOG
    Files.Print_to_file(Log_file,"\n\nChecking dead tracks ({} files): {}\n",nbr_files,Files.track_time())

    # CREATES LIST OF DEAD TRACKS 
    do_list = [i for i in range(nbr_files) if Arq[i]==""]
    nbr_files_to_updt = len(do_list)

    # NAO CRIA PLAYLISTS PQ ARQ IS MISSING

    # PRINTS RESULT BEFORE UPDATE
    print("Tracks that are missing:",nbr_files_to_updt,"\n")
    Files.Print_to_file(Log_file,"TIME: {}\n",Files.track_time())
    Files.Print_to_file(Log_file,"Tracks that may be removed: {}\n",nbr_files_to_updt)

    # START
    removed = 0
    failed = 0
    for j in range(nbr_files_to_updt):
        i = do_list[j]
        try:
            #track = tracks_lst[i]
            m = ID[i]
            track = App.GetITObjectByID(*m)
            print("Trying to delete",j+1,"of",nbr_files_to_updt,":",track.Artist," - ",track.Name,"(path=",track.Location,")")
            # PRINT TO LOG
            Files.Print_to_file(Log_file,"Trying to delete {} of {}: {} - {}\n",j+1,nbr_files_to_updt,track.Artist,track.Name)
            track.delete()
        except:
              failed = failed+1
              print("Failed to removed:",failed,"tracks\n")
        else:
            removed = removed+1
            print("Removed",removed,"dead tracks (",failed," failed)\n")

######################################################################################
######################################################################################
# THIS MODULE TRANSFER TAGS SUCH AS YEAR, GENRE AND ALBUM WHEN THE ARTIST-TITLE MATCH
def Transfer(PL_name=None,PL_nbr=None,Do_lib=False,rows=None,call_Covers=1, call_Dead=0):
    global App
    global playlists
    global tracks_lst
    global nbr_files
    global Arq
    global ID

    if call_Dead:
       Do_lib = True 
    # CALLS Read_PL FUNCTION ,Do_lib=True,rows=10
    col_names =  ["Arq","Art","Title","ID"] 
    dict = Read_PL.Read_PL(col_names,PL_name=PL_name,PL_nbr=PL_nbr,Do_lib=Do_lib,rows=rows)
    # ASSIGNS
    App = dict["App"]
    playlists = dict["PLs"]
    df = dict["DF"]

    # POPULATES LISTS
    Art = [x for x in df["Art"]]
    Title = [x for x in df["Title"]]

    # Cria nova lista baseada nos nomes
    # ANY TRACK IS INCLUDED, INCLUDING THOSE WITH MISSING FILE
    track_stdz = []
    for i in range(len(Art)):
        track_stdz.append(Tags.Stdz(Art[i]+" & "+Title[i]))

    # CREATES COL. WITH STDZ TRACK NAMES
    df.loc[:, "track_stdz"] = track_stdz
    # FLAGS DUPES
    df["Count"] = df.groupby("track_stdz")["Pos"].transform("count")

    print("\nPrior to selection, df has",df.shape[0],"rows\n")

    # SELECT ONLY RELEVANT ROWS
    df = df[df["Count"] > 1]

    print("The df has",df.shape[0],"dupes")

    # SELECT ONLY TRACKS WHERE AT LEAST ONE OF THE DUPES IS NOT MISSING
    Arq = [x for x in df["Arq"]]
    not_miss = [1*exists(Arq[i]) for i in range(len(Arq))]
    # ADDS NOT-MISSING COL. TO DF
    df.loc[:, "not_miss"] = not_miss
    # ONLY DUPES WITH AT LEAST ONE NON-MISSING FILES
    df["sum_not_miss"] = df.groupby("track_stdz")["not_miss"].transform("sum")
    
    # SELECT ONLY RELEVANT ROWS
    df = df[df["sum_not_miss"] >= 1]

    print("The df has",df.shape[0],"dupes with at least one non-missing file")

    # PAIRS WITH ONE DEAD TRACK
    df["Dead"] = df.groupby("track_stdz")["not_miss"].transform("nunique")

    # CHECKS COVERS ONLY FOR THE DUPES
    ID = [x for x in df["ID"]]
    nbr_files = len(ID)

    # RE-BUILDING OTHER LISTS 
    print("\nBuilding tags lists...")
    #tracks_lst = [playlists.ItemByName(PL_list[i]).Tracks.Item(Pos[i]) for i in range(nbr_files)]
    tracks_lst = [App.GetITObjectByID(*ID[i]) for i in range(nbr_files)]
    list = ["AA","Album","Genre","Year","Plays","Skips"]
    for key in list:
        Col = [getattr(tracks_lst[i], Read_PL.iTu_tag_dict[key]) for i in range(nbr_files)]
        # ADDS TO THE DF
        df.loc[:, key] = Col
    
    # COUNT IF GENRES MATCH BETWEEN THE DUPES
    Genre = [x for x in df["Genre"]]
    Genre_count = [len(set(x.split("\\")).intersection(Genres)) for x in Genre]
    # ADDS TO THE DF
    df.loc[:, "Genre_count"] = Genre_count

    # 1 IF ARQ != "", 0 OTHERWISE (ARQ POPULATED)
    df["Arq_miss"] = df["Arq"].apply(lambda x: 1 if x == "" else 0)

    # COVERS    
    # WHAT WILL BE RUN
    # LOGIC TO DISPLAY IN THE LOG
    tam = nbr_files // 20
    if call_Covers:
        print("\nBuilding cover list...\n")
        Covers = []
        for i in range(nbr_files):
            if (i+1) % tam==0:
                print("Checked",i+1,"of",nbr_files,"covers")
            track = tracks_lst[i]
            Art_cnt = track.Artwork.count
            # ADDS SCORE    
            Covers.append(Art_cnt)
        # ADDS TO THE DF    
        df.loc[:, "Covers"] = Covers
        df["Covers"] = df["Covers"].astype(int)
    else:
        # ALL COVERS ARE EQUAL IF NOT NEEDED TOR RUN
        df.loc[:, "Covers"] = 1
    
    # NOW SELECT ONLY ROWS WHERE THE DATA MAY CHANGE
    # concatenate columns A and B into a new column C
    # ADDS COVER COL. TO DF 
    df["Key"] = df["AA"] +"@"+ df["Album"] +"@"+ df["Genre_count"].astype(str) +"@"+ df["Plays"].astype(str)+"@"+ \
                df["Skips"].astype(str)+"@"+df["Covers"].astype(str)+df["Arq_miss"].astype(str)

    # NOW SELECT ONLY ROWS WHERE THE DATA MAY CHANGE
    # ADDS KEY COL. TO DF
    df["dist_Key"] = df.groupby("track_stdz")["Key"].transform("nunique")

    # BELOW TO FORCE GROUPS WHERE ONE AT LEAST ONE IS DEAD
    df["Key"] = df["not_miss"].astype(str)
    df["dist_Key"] = df.groupby("track_stdz")["Key"].transform("nunique")

    # SELECT ONLY TRACKS THAT MATTER
    df = df[df["dist_Key"] > 1]

    print("\nThe df has",df.shape[0],"dupes with at least one tag differing")

    # SAVES DUPES TO AN EXCEL FILE
    # df2 = df[df["Dead"]>1]
    file_nm = "D:\\Python\\Excel\\Test.xlsx"
    # save the dataframe to an Excel file
    df.to_excel(file_nm, index=False)

    # ONLY DUPES IN 2 DIFFERENT PL"s (TIRAR ISSO DEPOIS)
    # SELECT ONLY RELEVANT ROWS
    # df["dist_PL"] = df.groupby("track_stdz")["PL"].transform("nunique")
    # df = df[df["dist_PL"] > 1]
    
    # TESTA DUPES
    #df["dist_arq"] = df.groupby("track_stdz")["Arq_lower"].transform("nunique")
    #df = df[df["dist_arq"]==1] 
    
    # SORTS DF
    # CRIA COL. LOCATION IN LOWER CASE (THE DIRECT SYNTAX IS NOT NICE)
    df["Arq_lower"] = df["Arq"].str.lower()
    # SORTS THE DF SO THE DUPES APPEAR AT THE TOP
    df = df.sort_values(["Count","track_stdz","Arq_lower"], ascending=[True, True, True])

    # REFRESHES TRACK LIST
    Arq = [x for x in df["Arq"]]
    ID = [x for x in df["ID"]]
    # BUILDING OTHER LISTS 
    print("\nBuilding tags lists again")
    nbr_files = len(ID)
    tracks_lst = [App.GetITObjectByID(*ID[i]) for i in range(nbr_files)]

    # CREATES A NEW PLAYLIST TO SAVE DUPES IF NEEDED TO RE-RUN MANY TIMES
    # CRIA PLAYLISTS
    
    if nbr_files>0:
       PL_nm = "Transfer_Dupes"
       PL = Read_PL.Create_PL(PL_nm,recreate="n")

       # ADD TRACKS TO NEW PL
       # DOESN"T NEED TO CHECK IF FILE EXISTS, MISSING FILES ARE NOT ADDED
       if not PL["PL_exists"]:
          non_blank = len([item for item in Arq if item != ""])
          print("Adding",non_blank,"non-missing files to playlist")
          for i in range(nbr_files):
              track = tracks_lst[i]
              Read_PL.Add_track_to_PL(playlists,PL_nm,track)


    # MANUALLY SET THESE PARAMETERS
    if nbr_files>0:
       if call_Covers:
                   Do_Covers(df)

       call_Year = 0
       if call_Year:
                   Do_Year(df)

       call_Genre = 0
       if call_Genre:
                   Do_Genre(df)
        
       call_Counts = 0
       if call_Counts or call_Dead:
                   Do_Counts(df)

       # NAO MAIS NECESSARIO 
       if call_Dead and Do_lib:
                     Do_Dead(df)

#CALLS FUNC Transfer_Dupes
Transfer(PL_name="AAA",Do_lib=1,rows=None,call_Covers=0, call_Dead=1)