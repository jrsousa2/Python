# LOOKS UP THE DISCOGS DB TO TRY AND UPDATE THE YEAR TAG 
# OF TRACKS IN AN ITUNES PLAYLIST
# IT MAY UPDATE OTHER TAGS SUCH AS GENRE AND ALBUM
# IT DOESN'T NEED AN INITIAL PLAYLIST, IT CREATES THE PLAYLIST FIRST
# FIRST ADDS TR TRACKS IN PLAYLIST

import discogs_client
from requests import get
from timeit import default_timer
from time import sleep
# import openpyxl
# import datetime
from Search import Log_file
import Search
import Read_PL
import Tags
import Images
import Files

Discogs_dwl_folder = "D:\\Z-Covers\\Discogs\\"

Log_artist = "D:\\iTunes\\Log_Artist.txt"
Log_title = "D:\\iTunes\\Log_Title.txt"
Log_year = "D:\\iTunes\\Log_Year.txt"

# SHEETS LAYOUTS (DISABLED FOR NOW)
Art_layout = ["API", "Search", "Cur_Artist", "Nbr_srch_art", "Srch_artists", "Srch_variations"]
Title_layout = ["API", "Search", "Cur_title", "Nbr_srch_title", "Srch_title"]
Year_layout = ["Art", "Title", "Hits", "Master_cnt", "Master_Year", "Release_cnt", "Release_Year"]


# PARAMETER USED TO SEARCH IN DISCOGS
Srch_type = ["master","release"]

# LIST OF SELECTED LABELS
Sel_labels_list = ["Som Livre","WEA","Stiletto","Paradoxx Music","Fieldzz", "Opus/Columbia"]


# CHECK INTERNET CONNECTION
def internet_up():
    online = True
    try:
        response = get("https://www.google.com")
    except:
        online = False
    return online

# SCORE USED TO CHOOSE ALBUM
def Score(dict,Alb_by_art_Year,VA_Year):
    score = 1000*(dict["Alb_by_art"]==True)+100*(dict["Year"]==Alb_by_art_Year)+10*(dict["Year"]==VA_Year)+1*(dict["Type"]=="master")
    return score


# DETERMINES THE ORDER THE SEARCH WILL BE CONDUCTED
# ENSURES ONLY A MAX OF 20 RESULTS ARE RETURNED 
# AS A COMBINATION OF ALL SEARCH PMTS
def Srch_priority(disco,Art,Title,AA,Album,Genre,Year):
    # ASSIGNS THE PRIORITY IN THE SEARCH
    if Tags.Is_Brasil(Genre):
        country = ["Brazil", "US", ""]
    else: 
        country = ["US", "Brazil", ""]

    # SEARCH ONLY MASTERS INITIALLY 
    Res_list = []
    tam = 0
    # SEARCHES Srch_discogs(disco,Res_list,Art,Title,Album,Srch_type,pcountry,pformat="",plabel="")
    if False:
        for i in range(0):
            Res_list = Srch_discogs(disco,Res_list,Art,Title,"","",Srch_type[i],"Brazil",format="Vinyl")
            Res_list = Srch_discogs(disco,Res_list,Art,Title,"","",Srch_type[i],"Brazil")
            # SEARCH BY THE TRACK
            #for srch_label in Sel_labels_list:
                  #Res_list = Srch_discogs(disco,Res_list,Art,Title,"","",Srch_type[i],"Brazil",format="Vinyl",label=srch_label)
        # SEARCH BY THE ALBUM        
        for i in range(0):
            if Album != "":
               Res_list = Srch_discogs(disco,Res_list,"","",AA,Album,Srch_type[i],"Brazil",format="Vinyl")
               Res_list = Srch_discogs(disco,Res_list,"","",AA,Album,Srch_type[i],"Brazil")
               #for srch_label in Sel_labels_list:
                   #Res_list = Srch_discogs(disco,Res_list,"","",AA,Album,Srch_type[i],"Brazil",format="Vinyl",label=srch_label)
    
    # SEARCH BY THE TRACK
    for i in range(2):
        for j in range(3):
            # if (Year==0 or Year<=1991):
            #     Res_list = Srch_discogs(disco,Res_list,Art,Title,"","",Srch_type[i],country[j],format="Vinyl")
            Res_list = Search.Srch_discogs(disco,Res_list,Art,Title,"","",Srch_type[i],country[j],format="CD")
            Res_list = Search.Srch_discogs(disco,Res_list,Art,Title,"","",Srch_type[i],country[j])    

    # SEARCH BY THE ALBUM
    for i in range(2):
        for j in range(3):
            if Album != "":
            #    if (Year==0 or Year<=1991):
            #        Res_list = Srch_discogs(disco,Res_list,"","",AA,Album,Srch_type[i],country[j],format="Vinyl")
               Res_list = Search.Srch_discogs(disco,Res_list,"","",AA,Album,Srch_type[i],country[j],format="CD")
               Res_list = Search.Srch_discogs(disco,Res_list,"","",AA,Album,Srch_type[i],country[j])   

    # RETURN
    return Res_list

# MAIN CODE
def Call_discogs(PL_name=None,PL_nbr=None):
    # CALLS FUNCTION
    col_names =  ["Arq","Art","Title","AA","Album","Year","Genre","Group","Covers","ID"]
    dict = Read_PL.Read_PL(col_names,PL_name=PL_name,PL_nbr=PL_nbr)
    iTunesApp = dict["App"]
    PLs = dict["PLs"]
    df = dict["DF"]
    # PL_main_nm = dict["PL_Name"]
    tracks = dict["tracks"]

    # CREATES LISTS FROM ALL COLUMNS (NEED TO BE DECLARED TO CLEAR ERROR MSGS)
    # TEST LIST CREATION (list comprehension)        
    Arq = [x for x in df["Arq"]]
    Art = [x for x in df["Art"]]
    Title = [x for x in df["Title"]]
    AA = [x for x in df["AA"]]
    Album = [x for x in df["Album"]]
    Year = [x for x in df["Year"]]
    Genre = [x for x in df["Genre"]]
    Group = [x for x in df["Group"]]
    Covers = [x for x in df["Covers"]]
    ID = [x for x in df["ID"]]

    # CALLS THE DISCOGS OBJECT (NEEDS USER TOKEN)
    my_user_token = input("Enter DISCOGS user token")
    # Open the file in read mode
    with open("D:\\iTunes\\Music\\Discogs_token.dat", 'r') as file:
         # Read the first line and strip any extra whitespace
         my_user_token = file.readline().strip()

    disco = discogs_client.Client("ExampleApplication/0.1", user_token=my_user_token)

    # CRIA PLAYLIST PARA ARQUIVOS ATUALIZADOS
    # Create_PL(PL_fix_nm,recreate="y")
    PL_nm = {}
    PL_nm["Year"] = "Updt_Year"
    PL_nm["Genre"] = "Updt_Genre"
    PL_nm["Album"] = "Updt_AA_Album"
    #PL_nm["Attached"] = "Updt_Attached"
    PL_nm["Not_found"] = "Updt_Not_found"
    for key in PL_nm.keys():
        My_PL = Read_PL.Create_PL(PL_nm[key]) 

    # LOADS VINYL TEMPLATE
    vinyl_resized = Images.Read_and_resize("D:\\Z-Covers\\Vinyl\\template.jpg")

    # ADDS FILES IN THE EXCEL SHEET TO THE PLAYLIST
    # TAMBEM CONSTROI A LISTA DE ARQUIVOS QUE TERAO O YEAR ATUALIZADOS
    To_fix_list = []
    fixed = {}
    Stat_list = ["Processed", "Hits", "Total API", "API calls", "Total searches","Searches","Skipped", \
                 "Year", "Album", "Genre", "Attached", "Deleted", "Attach exc"]
    # INITIALIZE STATS
    for key in Stat_list:
        fixed[key] = 0
    miss = 0
    nbr_files = tracks.Count
    
    print("\n")
    print("Starting code at",Files.track_time(),"\n")
    # USED FOR IMAGE RETRIEVING
    img_func = {"master": disco.master, "release": disco.release}
    elapsed_time = 0
    time_lim_sec = 40
    Online = internet_up()
    i = 0
    while (Online and i<nbr_files):
        if (i+1) % 100==0:
            if not internet_up():
               sleep(5) 
            if not internet_up():
               Online = False
               Files.Print_to_file(Log_file,"INTERNET IS DOWN: {}\n\n",Files.track_time())
               print("INTERNET IS DOWN:",Files.track_time(),"\n")
            else:
                Files.Print_to_file(Log_file,"INTERNET IS OK: {}\n\n",Files.track_time())   
        # IF INTERNET OK
        fixed["Processed"] = i+1
        file_exists = Files.exists(Arq[i])
        file_nm = Files.File_no_nbr_no_ext(Arq[i])
        m = ID[i]
        # ASSIGNS TRACK WITH TUPLE
        track = iTunesApp.GetITObjectByID(*m)
        #track = tracks.Item(*m)
        Curr_loc = track.Location
        if not file_exists:
           miss=miss+1
        if file_exists and Arq[i]==Curr_loc and Online and Files.Is_DMP3(Arq[i]):
           Files.Print_to_file(Log_file,"Searching file {} of {}--{}\n",i+1,nbr_files,Arq[i])
           Files.Print_to_file(Log_file,"START: {}\n",Files.track_time())
           print("Searching file",i+1,"of",nbr_files,":",file_nm,"(",Files.track_time(),")")
           # SEARCH STARTS HERE:    
           Res_list = Srch_priority(disco,Art[i],Title[i],AA[i],Album[i],Genre[i],Year[i])
           nbr_calls = len(Res_list)
           count_res = Search.count_results(Res_list)
           fixed["Total API"] = nbr_calls
           fixed["Total searches"] = count_res
           for j in range(0,nbr_calls):
               dict = Res_list[j]
               print("API call",j+1,"of",nbr_calls,"-Type:",dict["Type"],"-By:",dict["Srch_by"],"-Count:",dict["Count"])
           # START OF LOGIC
           # INITIALIZE LISTS
           print("")
           List = []
           Actual_match = False
           k = 0
           fixed["API calls"] = 0
           fixed["Searches"] = 0
           fixed["Skipped"] = 0
           # Get the current time
           start_time = default_timer()
           elapsed_time = 0
           IDs_searched = set([])
           srch_res = {}
           while (k<nbr_calls and elapsed_time<time_lim_sec):
                  API = Res_list[k]
                  # MOST OF THE RESULTS INFO GO HERE
                  srch_res["Type"] = API["Type"]
                  srch_res["Srch_by"] = API["Srch_by"]
                  # BELOW IS PER CALL
                  nbr_res = API["Count"]                 
                  nbr_pages = API["Pages"]
                  results = API["Results"]
                  nbr_matches = min(nbr_res,20)
                  fixed["API calls"] = fixed["API calls"] + 1
                  # START OF LOGIC
                  print("API call",k+1,"of",nbr_calls,"-Type:",srch_res["Type"],"-By:",srch_res["Srch_by"],"-Count:",nbr_res)
                  j = 0
                  while(j<nbr_matches and fixed["Searches"]<20 and elapsed_time<time_lim_sec):
                        # ONLY CONSIDER SEARCH IF THERE IS NO EXCEPTION UPON READING
                        try:
                            Obj = results[j]
                        except Exception:
                            Obj = None
                            Obj_exists = False
                        else:
                            Obj_exists = True 
                        type_ID = None
                        srch_res["ID"] = None
                        srch_res["Year"] = 0
                        srch_res["Main_ID"] = None
                        srch_res["AA_Album"] = None
                        srch_res["Country"] = None
                        srch_res["Genre"] = None
                        srch_res["VA"] = False
                        if Obj_exists:
                           if Search.Check_attrib(Obj,"id"):
                              srch_res["ID"] = Obj.id
                           if Search.Check_attrib(Obj,"year"):
                              srch_res["Year"] = int(Obj.year) 
                           srch_res["AA_Album"] = Tags.coalesce(Obj.title,"")
                           # THE BELOW IS A DICTIONARY VALUE
                           srch_res["Style"] = Search.Get_attrib(Obj,"style")
                           # THE BELOW IS THE SAME AS THE ABOVE, EXCEPT IT'S NOT A LIST
                           srch_res["Country"] = Obj.data.get("country","")
                           if Search.Check_attrib(Obj,"genres"):
                              srch_res["Genre"] = Obj.genres[0]
                           # FIRST LETTER OF THE TYPE (M/R)
                           # type_ID = srch_res["Type"][0]+str(srch_res["ID"])
                           type_ID = srch_res["Type"][0]+str(srch_res["Year"])+Tags.Stdz(srch_res["AA_Album"])
                        Skip = False 
                        # IF SEARCHED BEFORE DON'T SEARCH AGAIN  
                        if type_ID in IDs_searched:
                           Skip = True 
                           fixed["Skipped"]=fixed["Skipped"]+1
                        if type_ID is not None:
                           IDs_searched.add(type_ID)   
                        if not Skip and type_ID is not None: 
                           print("\tChecking result",j+1,"of",nbr_matches)
                           # ONLY UPDATE COUNT IF SEARCHING
                           fixed["Searches"] = fixed["Searches"] + 1  
                           # CALL ART MATCH
                           Art_match_dic = Search.func_art_match(srch_res,Obj,k,j,Art[i])
                           Art_match = Art_match_dic["res"]
                           # CALL TITLE MATCH
                           Title_match_dic = Search.func_title_match(Obj,k,j,Art[i],Title[i])
                           Title_match = Title_match_dic["res"]
                           # REPEAT SEARCH FOR ARTIST IF VARIOUS ARTISTS
                           if not Art_match and Title_match_dic["Art_match"]:
                              Art_match = True
                              srch_res["VA"] = True
                           Live_check = Tags.Album_is_live(Genre[i],srch_res["AA_Album"])==Tags.Genre_is_live(Genre[i])   
                           if Art_match and Title_match and srch_res["Year"]>0 and Live_check:
                              print("\t\tTrack found in album",srch_res["AA_Album"])
                              srch_res["Label"] = Search.Get_attrib(Obj,"label")
                              srch_res["Format"] = Search.Get_attrib(Obj,"format")
                              split = Tags.Split_AA_Album(Art[i],Title[i],srch_res["AA_Album"])
                              srch_res["AA"] = split["AA"]
                              srch_res["Album"] = split["Album"]
                              srch_res["quality"] = split["quality"]
                              srch_res["Alb_by_art"] = Tags.Alb_by_art(Art[i],Title[i],srch_res["AA"])
                              if Search.Check_attrib(Obj,"main_release") and Search.Check_attrib(Obj.main_release,"id"):
                                 srch_res["Main_ID"] = Obj.main_release.id
                              # ADDS RES TO LIST
                              List.append(srch_res.copy())
                              Actual_match = True
                        # CHECK ELAPSED TIME (AFTER EACH j ROUTINE)
                        end_time = default_timer()
                        elapsed_time = end_time - start_time
                        # INCREMENT COUNTER
                        j = j+1        
                  # END OF FOR j
                  # CHECK ELAPSED TIME AGAIN (AFTER EACH k ROUTINE)
                  end_time = default_timer()
                  elapsed_time = end_time - start_time
                  k = k+1
           # END OF FOR k
           # END OF SEARCH FOR FILE
           # UPDATE GROUPING 
           New_Grouping = Tags.Add_to_tag(track,"Searched",Tag="Group")
           # SAVE MISMATCH EXCEL FILES
           print("Search ended",Files.track_time(),"with",int(elapsed_time),"seconds elapsed") 
           # THIS BLOCK IS TO CARRY OUT THE TAG UPDATE RIGHT AWAY
           # AFTER THE SEARCH ON A GIVEN FILE IS DONE
           # HERE THE PRIORITY IS RESPECTED WITH THE MIN
           tam = len(List)
           if tam>0:
              fixed["Hits"] = fixed["Hits"]+1
              print("FOUND! :",file_nm)
              To_fix_list.append(i)
              # TEST YEAR ACCURACY:
              Mast_l = [List[i]["Year"] for i in range(tam) if List[i]["Type"] == "master"]
              Mast_cnt = len(Mast_l)
              Mast_Year = min(Mast_l, default=9999)
              Rel_l = [List[i]["Year"] for i in range(tam) if List[i]["Type"] == "release"]
              Rel_cnt = len(Rel_l)
              Rel_Year = min(Rel_l, default=9999)
              Master_picked = False
              # YEAR LOGIC
              if 0 < Mast_Year < 9999:
                 New_Year = Mast_Year
                 Master_picked = True
              else:   
                  New_Year = Rel_Year
              # WRITE COMPARISON TO EXCEL  
              # PICK THE TRACK
              Alb_by_art_l = [List[i]["Year"] for i in range(tam) if List[i]["Alb_by_art"]==True]
              Alb_by_art_Year = min(Alb_by_art_l, default=9999)
              VA_l = [List[i]["Year"] for i in range(tam) if List[i]["Alb_by_art"]==False]
              VA_Year = min(VA_l, default=9999)
              #df = pd.DataFrame(data) 
              # SCORE LIST
              score_l = [Score(List[i],Alb_by_art_Year,VA_Year) for i in range(tam)]
              max_score = max(score_l)
              # THE CHOSEN ALBUM    
              indice = score_l.index(max_score)
              srch_res = List[indice]
              # UPDATE LOG  
              Files.Print_to_file(Log_file,"FOUND! : {}\n",file_nm)
              Files.Print_to_file(Log_file,"TIME: {}\n",Files.track_time())
              Files.Print_to_file(Log_file,"Search type: {} ID: {} Label: {}\n",srch_res["Type"],srch_res["ID"],srch_res["Label"])
              Files.Print_to_file(Log_file,"Processed: {} Hits: {} Search by: {}\n",fixed["Processed"], fixed["Hits"], srch_res["Srch_by"])
              Files.Print_to_file(Log_file,"API calls: {} Searches: {} Skips: {}\n",fixed["API calls"], fixed["Searches"], fixed["Skipped"])
              
              # THIS IS TO KNOW IF A RY IS LESS THAN THE CURRENT YEAR
              if Rel_Year < Mast_Year < 9999 and (Rel_Year<Year[i] or Year[i]==0):
                 add_tag = "RY=" + str(Rel_Year)
                 New_Grouping = Tags.Add_to_tag(track,add_tag,Tag="Group")

              # YEAR
              if (Year[i]==0 or Year[i]>New_Year+1) and New_Year>0:
                  track.Year = New_Year
                  fixed["Year"] = fixed["Year"] +1
                  print("\tUpdated Year of",file_nm,"|| From",Year[i],"->",New_Year)
                  Files.Print_to_file(Log_file,"Updated Year of {} || From {} -> {}\n",file_nm, Year[i], New_Year)
                  Read_PL.Add_track_to_PL(PLs,PL_nm["Year"],track)

              # GENRE
              Cur_Genre = track.Genre
              New_Genre_vl = Tags.coalesce(srch_res["Style"], srch_res["Genre"])
              New_Genre = Tags.Add_to_tag(track,New_Genre_vl)
              if New_Genre != "":
                 fixed["Genre"] = fixed["Genre"] +1
                 print("\tUpdated Genre of",file_nm,"|| From",Genre[i],"->",New_Genre)
                 Files.Print_to_file(Log_file,"Updated Genre of {} || From {} -> {} (added {})\n",file_nm, Cur_Genre, New_Genre, New_Genre_vl)
                 Read_PL.Add_track_to_PL(PLs,PL_nm["Genre"],track)

              # ALBUM
              srch_AA = srch_res["AA"]
              srch_Album = srch_res["Album"]
              Cur_AA = track.AlbumArtist
              Cur_Album = track.Album
              Cur_covers = Covers[i]
              # IMAGE IS BASED ON THE ID, SO IF THE COVER IS RIGHT, THE ID IS RIGHT
              try:
                 images_collec = img_func[srch_res["Type"]](srch_res["ID"]).images
              except:
                 images_collec = None
              Has_image = False
              if images_collec is not None:
                 # AQUI TEM QUE COLOCAR EM FUNCAO DO TIPO
                 if type(images_collec)==list and len(images_collec)>0:
                    img = img_func[srch_res["Type"]](srch_res["ID"]).images[0]
                    Has_image = True
                 else:
                     Files.Print_to_file(Log_file,"Image of {} is not a list (image exists)\n",file_nm)   
              if images_collec is None:
                 Files.Print_to_file(Log_file,"Image of {} is None (image doesn't exist)\n",file_nm)   
              # ALBUM SELECTION LOGIC
              Curr_Album_blank = Cur_AA=="" and Cur_Album==""
              Nice_cover_vl = Tags.Nice_cover(Cur_Album,Cur_Genre,Cur_covers)
              Alb_by_art_vl = Tags.Alb_by_art(Art[i],Title[i],srch_AA)
              Alb_not_great = not Tags.Greatest_Hits(Cur_Album) and Alb_by_art_vl
              srch_Album_pop = srch_AA != "" and srch_Album != "" and Has_image 
              Albums_eq = Cur_AA==srch_AA and Cur_Album==srch_Album and Cur_covers==0
              VA_wo_cover = Tags.Is_VA(Cur_AA) and not Nice_cover_vl and Cur_covers==0
              VA = Tags.Is_VA(Cur_AA) and not Nice_cover_vl and Alb_by_art_vl

              # Alb_is_Brasil = srch_res["Country"]=="Brazil" and Cur_covers==0
              By_art_wo_cover = Tags.Alb_by_art(Art[i],Title[i],Cur_AA) and Tags.Alb_by_art(Art[i],Title[i],srch_AA) \
                                and not Tags.Nice_cover(Cur_Album,Cur_Genre,Cur_covers) and Cur_covers==0
              Updt_Album = srch_Album_pop and (Curr_Album_blank or VA_wo_cover or Albums_eq or By_art_wo_cover or VA)
              if Updt_Album and Has_image:
                 # AQUI TEM QUE COLOCAR EM FUNCAO DO TIPO
                 URL = img["uri"]
                 New_cover_file = Images.Dwld_cover(Arq[i],srch_AA,srch_Album,URL,Discogs_dwl_folder,Remove_accent=True)
                 new_cover_resized = Images.Read_and_resize(New_cover_file)
                 vinil_dict = Images.Compare_imgs(new_cover_resized, vinyl_resized, threshold = 0.37)
                 Files.Print_to_file(Log_file,"Cover vinyl match: {} \\ Score: {}\n",vinil_dict["match"], vinil_dict["metric"])
                 print("Cover vinyl match:",vinil_dict["match"],"\\ Score:",vinil_dict["metric"],"\n")
                 attachf = {}
                 attachf["Tag_updt"] = False
                 if vinil_dict["match"]==False or Cur_covers==0:
                    attachf = Images.Attach_cover(Log_file,track,srch_AA,srch_Album,New_cover_file,fixed["Album"],VA=True)
                 if attachf["Tag_updt"]:
                    if vinil_dict["match"]:
                       New_Grouping = Tags.Add_to_tag(track,"VinylCover",Tag="Group")
                    fixed["Album"] = fixed["Album"]+1
                    Read_PL.Add_track_to_PL(PLs,PL_nm["Album"],track)
                    # UPDATES GROUPING
                    # add_tag = srch_res["Type"]+"\\Country="+srch_res["Country"]+"\\Label="+srch_res["Label"]+"\\Format="+srch_res["Format"]
                    New_Grouping = Tags.Add_to_tag(track,srch_res["Type"],Tag="Group")
                    if srch_res["quality"] != "accurate":
                       New_Grouping = Tags.Add_to_tag(track,srch_res["quality"],Tag="Group")
                    if srch_res["VA"] == True:
                       New_Grouping = Tags.Add_to_tag(track,"\\Various",Tag="Group")   
                 if attachf["Attached"]:
                    fixed["Attached"] = fixed["Attached"]+1
                    New_Grouping = Tags.Add_to_tag(track,"Attached",Tag="Group")
                    #Create_PL.Add_track_to_PL(PLs,PL_nm["Attached"],track)
                 if attachf["Deleted"]:
                    fixed["Deleted"] = fixed["Deleted"]+1
                 if attachf["Exception"]:
                    fixed["Attach exc"] = fixed["Attach exc"]+1 
              # UPDATE GROUPING ONLY AT THE END OF THE BLOCK
              New_Grouping = Tags.Add_to_tag(track,"Found",Tag="Group") 
           else:   
                print("\tNOT FOUND! :",file_nm,"\n")
                Read_PL.Add_track_to_PL(PLs,PL_nm["Not_found"],track)
           # FINAL DO IF SE ACHOU
           print("\tSTATS")  
           for key in fixed.keys():
               print("\t",key,":",fixed[key]) 
           print("")
           # REMOVE TRACK FROM PL AFTER SEARCH
           Read_PL.Remove_track_from_PL(track)
           # END OF IF LIST NOT EMPTY
           # print("")
        # LEFT THE IF FILE EXISTS
        # BREAK ONE LINE IN THE FILE
        Files.Print_to_file(Log_file,"\n")  
        i = i+1 

    # LEFT THE FILE LOOP
    # NUMERO DE ARQUIVOS ATUALIZADOS
    print("\n\nFinal:",fixed["Hits"],"hits out of",nbr_files,"tracks\n")

    # MISSING FILES
    print(miss,"files missing\n")        
    
# CALLS FUNC
Call_discogs(PL_name="Playlist 2")