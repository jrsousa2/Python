from Tags import compress, Remove_dupe_spaces
import Tags
import Files

Log_file = "D:\\Python\\Log_Discogs.txt"

# artist separators
Sep = {}
Sep[","] = 1
Sep["&"] = 1
Sep[" e "] = 1
Sep[" y "] = 1
Sep[" \\ "] = 1
Sep[" / "] = 1
Sep[" feat. "] = 1
Sep["feat"] = 1
Sep[" ft. "] = 1
Sep[" ft "] = 1
Sep[" featuring "] = 1
Sep[" vs. "] = 1
Sep[" vs "] = 1
Sep[" and "] = 1
Sep[" with "] = 1
Sep[" presents "] = 1
Sep[" present "] = 1
Sep[" pres. "] = 1
Sep[" com "] = 1
Sep[" part. "] = 1

# PERFORMS A SEARCH ON DISCOGS
def Srch_discogs(disco,Res_list,Art,Title,AA,Album,srch_type,country,format="",label=""):
    # CHECKS HOW MANY COUNTS ARE
    count_res = count_results(Res_list)
    if count_res<20:
       # READS THE INPUT PMTS
       params = {
       "artist": Tags.coalesce(Art,AA),
       "track": Title,
       "title": Album,
       "type": srch_type,
       "format": format,
       "country": country,
       "label": label}

       # REMOVES EMPTY PARAMETERS
       params = {k: v for k, v in params.items() if v}

       # CALLS THE FUNCTION WITH THE PARAMETERS
       results = disco.search(**params)
       
       # UPDATES LIST
       # ERROS APARECERAM NESSA PARTE
       try:    
          nbr_res = results.count
       except:
          nbr_res = 0 
       if nbr_res>0 and results is not None:
          nbr_pages = results.pages
          dict = {}
          dict["Type"] = srch_type
          dict["Country"] = country
          if Album != "":
             dict["Srch_by"] = "Album"
          else:
              dict["Srch_by"] = "track"   
          dict["Count"] = nbr_res
          dict["Pages"] = nbr_pages
          dict["Results"] = results
          Res_list.append(dict)
    return Res_list 

# THE BELOW IS A LIST CREATED TO SUM THE RESULTS OVER ALL THE RES ENTRIES
def count_results(Res_list):
    count_values = [d["Count"] for d in Res_list if "Count" in d]
    # Use sum function to calculate the total count
    total_searches = 0
    if len(count_values)>0:
       total_searches = sum(count_values)
    return total_searches

# CHECKS IF AN ATTRIB (GIVEN BY A STRING) IS PART OF AN OBJECT
def Check_attrib(Obj,attrib):
    try:
        test2 = getattr(Obj, attrib) is not None #and not getattr(Obj, attrib)
        test1 = hasattr(Obj, attrib)
        Has_attrib = test1 and test2
    except Exception:
        Has_attrib = False
        print("\t\tAttribute",attrib.capitalize(),"not found")
    return Has_attrib

# GETS ATTRIB
def Get_attrib(Obj,attrib):
    if Check_attrib(Obj,"data"):
       try:
          res = Obj.data.get(attrib,[])[0]
       except:
          res = ""
    return res

def func_art_match(srch_res,Obj,k,j,Art):
    # CAN ONLY CONTINUE IF NOT OUT OF RANGE
    Has_art_list = False
    split = Tags.Split_AA_Album("","",srch_res["AA_Album"])
    New_AA = split["AA"]
    print("\t\t",srch_res["Type"].capitalize(),"ID:",srch_res["ID"],"--Country:",srch_res["Country"],"--Album:",srch_res["AA_Album"][0:70])
    # CHECK SE PODE CONTINUAR (tirei and Obj_exists abaixo)
    Has_art_list = Check_attrib(Obj,"artists")
    No_excps = (Has_art_list or New_AA != "")
    Names_list = []
    Variations_list = []
    if Has_art_list:
       Arts_obj_list = Obj.artists
       nbr_arts = len(Arts_obj_list)
       if type(Arts_obj_list)==list:
          # LIST OF SINGERS
          if Check_attrib(Arts_obj_list[0],"name"):
             Names_list = [Arts_obj_list[q].name for q in range(nbr_arts)]
          # THIS IS A LIST OF LISTS   
          Has_name_var = Check_attrib(Arts_obj_list[0],"name_variations")
          if Has_name_var:
             if type(Arts_obj_list[0].name_variations)==list:
                try:
                   Variations_list = [Arts_obj_list[q].name_variations for q in range(nbr_arts)]  
                except:
                   print("\t\tIssue with the name variations list")
    # CHECK IF THE ARTISTS MATCH
    Art_match = False
    if No_excps:
       Art_match = Art_srch_list(Art,srch_res["AA_Album"],Names_list,Variations_list)
    dict = {}
    dict["res"] = Art_match   
    return dict 

# THE BELOW IS A LIST OF CLASS OBJECTS
def func_title_match(Obj,k,j,Art,Title):
    dict = {}
    dict["Art_match"] = False
    dict["VA"] = False
    songlist = []
    VA_artists = []
    Is_VA = False
    Title_match = False    
    Has_tracklist = Check_attrib(Obj,"tracklist")
    Art_match = False
    if Has_tracklist:
        tracklist = Obj.tracklist
        nbr_tracks = len(tracklist)
        # THE SAME THING AS ABOVE, ONLY IT"S A LIST OF TRACK TITLES ONLY
        if type(tracklist)==list and len(tracklist)>0:
           if Check_attrib(tracklist[0],"title"):
              songlist = [tracklist[q].title for q in range(nbr_tracks)]
           if Check_attrib(tracklist[0],"artists"):
              Is_VA = True
              Art_match = False
              for q in range(nbr_tracks):
                  nbr_track_arts = len(tracklist[q].artists)
                  track_artists = [tracklist[q].artists[p].name for p in range(nbr_track_arts)]   
                  VA_artists.append(track_artists)
        # SEARCH SONG IN TRACK LIST
        Title_srch = Search_track_in_list(Title,songlist)
        Title_match = Title_srch["res"]
        Title_pos = Title_srch["pos"]
        Art_srch_lst = VA_artists[Title_pos]
        if Is_VA and Art_srch_lst:
           dict["VA"] = True
           Art_match = Art_srch_list(Art,"",Art_srch_lst,[])
           dict["Art_match"] = Art_match
    dict["res"] = Title_match
    return dict

# STANDARDIZES EACH ELEMENT OF A LIST PER THE SIMPLE_STDZ FUNCTION
def Stdz_list(my_list):
    # Use list comprehension to lowercase and remove leading/trailing whitespaces
    my_list = [Tags.Stdz(x) for x in my_list]
    # Return the updated list
    return my_list

# EXPAND LIST OF ARTISTS
# THIS TAKES A LIST OF ARTISTS, AND CREATES A NEW LIST
# BY SPLITTING ALL THE ARTISTS WITH ALL THE ARTISTS DELIMITERS (& , feat. ETC.)
def Split_art_list(my_list,delimiters):
    # Create a new list to store the split elements
    split_list = []
    # Iterate over each element in the list
    for item in my_list:
        # Initialize a temporary list to store the split items for each element
        split_items = [item]
        # Iterate over each delimiter and split the items using string.split()
        for delimiter in delimiters:
            # Create a temporary list to store the split items for current delimiter
            temp_split_items = []
            # Iterate over each item in the split_items list
            for split_item in split_items:
                # Split the item by current delimiter
                temp_split_items.extend(split_item.split(delimiter))
            # Replace the split_items list with temp_split_items for next iteration
            split_items = temp_split_items
        # Extend the split_items to the new list
        split_list.extend(split_items)
    # THE FINAL LIST
    split_list = [x.strip() for x in split_list]
    return split_list

# Measure execution time of using for loop
def Search_track_in_list(song,songlist):
    # Convert the search string to lowercase (or uppercase)
    song_stdz = Tags.Stdz(song)
    stdz_songlist = Stdz_list(songlist)
    dict = {}
    Found = song_stdz in stdz_songlist
    dict["res"] = Found
    if Found:
       indice = stdz_songlist.index(song_stdz) 
       dict["pos"] = indice
    else:
        dict["pos"] = -1   
    return dict

# BUILDS ARTIST SEARCH LIST
def Art_srch_list(Cur_Art,Srch_AA_Album,Names_list,Variations_list):
    # FIRST NEEDS TO CONVERT ARTIST TO LIST
    delimiters = list(Sep.keys())
    # ADDS ONE BLANK SPACE BEFORE AND AFTER EACH ELEMENT OF THE LIST
    Art_list = [Cur_Art]
    Art_list = Split_art_list(Art_list,delimiters)

    # BUILDS THE SRCH ARTISTS LIST
    if len(Names_list)>0:
       print("\t\tArtists list OK, checking artists")
    else:
        print("\t\tChecking Album artist (artists list exception)")
        split = Tags.Split_AA_Album("","",Srch_AA_Album)
        Srch_AA = split["AA"]
        Srch_Album = split["Album"]
        Names_list = []
        if Srch_AA != "":
           Names_list = [Srch_AA]

    # SPLIT THE SRCH ARTIST LIST
    Srch_art_list = Split_art_list(Names_list,delimiters)
    nbr_srch_arts = len(Srch_art_list)

    # COMPARES THE TWO
    set_curr = set(Stdz_list(Art_list))
    set_srch = set(Stdz_list(Srch_art_list))
    Art_match = set_curr == set_srch

    # CHECK ARTIST NAME VARIATIONS 
    # HERE THE CHECK WILL NOT CONSIDER STDZ
    nbr_actual_arts = len(Art_list)
    Variations_list = [x for x in Variations_list if x is not None]
    nbr_vari_arts = len(Variations_list)
    if not Art_match and nbr_actual_arts==nbr_vari_arts and nbr_actual_arts>0:
       # CONSTROI LISTA DE ARTIST ALIASES 
       artists_alias = []
       for i in range(nbr_actual_arts):
           if Variations_list[i] is not None:
              artists_alias.extend(Variations_list[i])
       Art_match = True
       artists_alias = {Tags.Stdz(x) for x in artists_alias}
       i = 0
       while (Art_match and i<nbr_actual_arts):
              print("\t\tChecking artist",i+1,"of",nbr_actual_arts,"in variations list:",Art_list[i])
              if Tags.Stdz(Art_list[i]) not in artists_alias:
                 Art_match = False
              i=i+1 
       Files.Print_to_file(Log_file,"Searched artist ({}) in variation list. Found? {}\n", Cur_Art, Art_match)       
    return Art_match

# Function to check if two strings have common words 
# SIMILARITY RATIO
def similar_ratio(base, comp, thres = 0.95):
    # Tokenize the strings into words (split on whitespace)
    base = compress(base.lower())
    base = Remove_dupe_spaces(base)
    comp = compress(comp.lower())
    comp = Remove_dupe_spaces(comp)
    words_base = base.split(" ")
    words_comp = comp.split(" ")

    # MAX SCORE
    base_len = len(base.replace(" ",""))
    comp_len = len(comp.replace(" ",""))
    max_len = max(base_len, comp_len)

    # Convert word lists to sets for faster intersection
    set1 = set(words_base)
    set2 = set(words_comp)

    # Check for common words using set intersection
    common_words = list(set1.intersection(set2))
    common_len = sum(len(word) for word in common_words)
    ratio = round(common_len / max_len, 5)

    Hit = ratio > thres
    
    # THESE METRICS BELOW ARE ALMOST ALL LENGTHS
    dict = {"base": base_len, "comp": comp_len, "common": common_len, "max": max_len, "ratio": ratio, "match": Hit}
    # If common_words is not empty, they have common words
    return dict