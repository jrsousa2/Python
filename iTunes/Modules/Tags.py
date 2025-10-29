# SUBROUTINE CALLED BY OTHER CODES
#import re
# from re import sub
import re
from os.path import exists
from unidecode import unidecode
from Search import similar_ratio

import sys
sys.path.insert(0, "D:\\Python\\iTunes\Modules")
#sys.path.insert(0, "D:\\Python\\WMP")

from Proper import Proper
import Read_PL
import Files


# USADO PARA ORDENAR COMO OS GENRES APARECEM NA TAG GENRE
Genre_order_list = ["Brasil","iPhone","Favorite","Easy","Novela","Pop","Rock","Alternative","Hip-Hop","Rap","Searched","Found","Attached","Brazil"]

# Word replacements
Kw = {}

# create a dictionary to store attribute names
local_tags_dict = {"genre": "Genre", "group": "Grouping"}

# DON'T CHANGE THE FIRST 10 POSITIONS BELOW */
# String replacement
Kw["ck"]="k"
Kw["ie"]="i"
Kw["ei"]="i"
Kw["ks"]="x"
Kw["sch"]="x"
Kw["ch"]="x"
Kw["sh"]="x"
Kw["in' "]="in "
Kw["in` "]="in "
Kw["ing "]="in "

# Brackets tem que vir primeiro
Kw["("]=" "
Kw[")"]=" "
Kw["["]=" "
Kw["]"]=" "

delim = " ^ "
# artist logic
Kw["+"] = delim
Kw[","] = delim
Kw["&"] = delim
Kw["e"] = delim
Kw["y"] = delim
Kw["\\"] = delim
Kw["/"] = delim
Kw["-"] = delim
Kw["feat."] = delim
Kw["ft."] = delim
Kw["ft"] = delim
Kw["featuring"] = delim
Kw["feat"] = delim
Kw["vs."] = delim
Kw["vs"] = delim
Kw["and"] = delim
Kw["with"] = delim
Kw["presents"] = delim
Kw["present"] = delim
Kw["pres."] = delim
Kw["com"] = delim
Kw["part."] = delim
Kw["com participação especial de"] = delim
Kw["participação especial de"] = delim
Kw["participação especial"] = delim
Kw["participação de"] = delim
Kw["participação"] = delim

# word replacement: 
# THEY ARE REPLACED ONLY IF THEY ARE PRECEDED/SUCCEEDED BY SPACES 
Kw["the"]=""
Kw["o"]=""
Kw["a"]=""
Kw["'"]=""
Kw["os"]=""
Kw["as"]=""
Kw["dj"]=""
Kw["version"]="" 
Kw["remastered"]=""
Kw["single"]=""
Kw["inch"] = ""
Kw["''"] = ""
Kw["rmx"] = "renix"
Kw["junior "]="jr"
Kw["you"]="u"
Kw["volume"]="vol"
Kw["to"]="2"
Kw["one"]="1"
Kw["two"]="2"
Kw["three"]="3"
Kw["four"]="4"
Kw["five"]="5"
Kw["six"]="6"
Kw["seven"]="7"
Kw["eight"]="8"
Kw["nine"]="9"
Kw["ten"]="10"
Kw["twenty"]="20"
Kw["thirty"]="30"
Kw["forty"]="40"
Kw["fifty"]="50"
Kw["sixty"]="60"
Kw["seventy"]="70"
Kw["eighty"]="80"
Kw["ninety"]="90"

# GREATEST HITS
Great = []
Great.append('best of')
Great.append('perfil')
Great.append('grandes')
Great.append('melhor')
Great.append('lo mejor')
Great.append(' mejor ')
Great.append('sempre')
Great.append('anniversary')
Great.append('anniversaire')
Great.append('recordings')
Great.append('retrospective')
Great.append('rhino hi-five')
Great.append('rhino hi five')
Great.append('maiores')
Great.append('sucesso')
Great.append('singles')
Great.append('gold')
Great.append('hits')
Great.append('classics')
Great.append('concert')
Great.append('collect')
Great.append('coletânea')
Great.append('coleção')
Great.append('collection')
Great.append('millenium')
Great.append('maxxim')
Great.append('ultimate')
Great.append('anthology')
Great.append('antologia')
Great.append('complete')
Great.append('compilation')
Great.append('seleção')
Great.append('selecao')
Great.append('edição')
Great.append('edition')
Great.append('exitos')
Great.append('éxitos')
Great.append('70')
Great.append('80')
Great.append('90')
Great.append('especial')
Great.append(' tour ')
Great.append(' years ')
Great.append(' anos ')
Great.append('platinum')
Great.append('série')
Great.append('series')
Great.append('mtv')
Great.append('essential')
Great.append('essencial')
Great.append('20 mais')
Great.append('historia')
Great.append('design of a decade')


# Nice cover
Nice_lst = []
Nice_lst.append('7 melhores')
Nice_lst.append('jovem pan')
Nice_lst.append('melhores jp')
Nice_lst.append('soundtrack')
Nice_lst.append(' ost ')
Nice_lst.append('motion picture')

# CONVERTE CARACTERES ESPECIAIS PARA ANSI
# TB SUBSTITUI CARACTERES COMO $ PARA s ETC.
def Replace_letters(Str):
    New_str = unidecode(Str)
    New_str = New_str.lower()
    trans_aux = New_str.maketrans("/$zmy", "\ssni")
    trans = {**trans_aux}
    New_str = New_str.translate(trans)
    return New_str

# THE BELOW ARE NOT SEARCHED WITH ENCLOSING SPACES
No_spc_kws = ["ie", "ei", "ks", "sch", "ch", "sh", "in' ", "ing", "(" , ")" , "[" , "]" , ",", "'"]

# REPLACES KEYS in SUBSTITUTION LIST
Kw_old = dict(Kw)
for key in Kw_old:
    old_key = key
    new_key = Replace_letters(old_key)
    Kw[new_key] = Kw.pop(old_key)

def Remove_dupe_spaces(str):
    New_str = re.sub(' +',' ', str)
    return New_str

# Example code to remove characters from a string
# Remove characters except blank spaces, letters (a to z), and numbers (0 to 9)
def Remove_spec_chars(text):
    text = "".join(c for c in text if c.isalnum() or c.isspace())
    return text

# COMECO DA LOGICA DE SUBSTITUICOES
# DOESN'T MODIFY THE PASSED PMT 
def Simple_stdz(Str):
    New_str = ""
    if Str != "":    
        New_str = Replace_letters(Str)

        # replaces double-letters
        for i in range(ord('a'),ord('z')+1):
            New_str = New_str.replace(chr(i)+chr(i),chr(i))

        # BELOW REMOVES DUPE SPACES 
        New_str = " " + New_str.strip() + " " #REMOVES LEADING AND TRAILING SPACES

        # KEYWORD REPLACEMENT
        for key in Kw:
            if key not in No_spc_kws:
               New_str = New_str.replace(" "+key+" "," "+Kw[key]+" ") 
            else:
                New_str = New_str.replace(key,Kw[key]) 

        # REMOVING DUPE SPACES AGAIN */
        New_str = Remove_spec_chars(New_str)
        New_str = re.sub(' +',' ',New_str)
        New_str = New_str.strip() 
    return New_str

# COMECO DA LOGICA DE SUBSTITUICOES
# DOESN'T MODIFY THE PASSED PMT 
def Stdz(Str):
    New_str = ""
    if Str != "":    
        New_str = Replace_letters(Str)

        # replaces double-letters
        for i in range(ord('a'),ord('z')+1):
            New_str = New_str.replace(chr(i)+chr(i),chr(i))

        # BELOW REMOVES DUPE SPACES 
        New_str = " " + New_str.strip() + " " #REMOVES LEADING AND TRAILING SPACES

        # KEYWORD REPLACEMENT
        for key in Kw:
            if key not in No_spc_kws:
               New_str = New_str.replace(" "+key+" "," "+Kw[key]+" ") 
            else:
                New_str = New_str.replace(key,Kw[key]) 

        # REPLACES CHARS EXCEPT A FEW
        New_str = "".join([c for c in New_str if ("a"<=c<="z" or "0"<=c<="9" or c in [" ","^"])])

        # REMOVING DUPE SPACES AGAIN */
        New_str = re.sub(" +"," ",New_str)
        New_str = New_str.strip()    

        #if Tag.lower()=="art":
        # New_str = New_str.replace("^^","^")
        # sub("\^+", "^", New_str)
        New_str = re.sub("\s*\^+\s*", "^", New_str) 
        New_str = New_str.split("^")
        New_str = [x.strip() for x in New_str]
        New_str.sort()
        New_str = "^".join(New_str)

        # REMOVE ALL SPACES
        #New_str = New_str.replace(" ", "")

    return New_str

# RIGHT FOLDER
def Is_Brasil(Genre):
    if "brasil" in Genre.lower():
        Brasil = True
    else:
        Brasil = False
    return Brasil

# RIGHT FOLDER
def Is_Fave(Genre):
    if "favorite" in Genre.lower():
        Fave = True
    else:
        Fave = False
    return Fave

def order_list(original_list, order_list):
    # Create a dictionary to store the index of each element in order_list
    order_dict = {element: index for index, element in enumerate(order_list)}
    
    # Sort the original list by the index of each element in order_dict if it exists,
    # otherwise by the original order of the element in the original list
    return sorted(original_list, key=lambda element: order_dict.get(element, len(order_list)))

# adds or initiates the genre
def Add_to_tag(track,New_tag,Tag="Genre"):
    # Updates Genre
    # CURRENT VALUE
    tag_assign = {"Genre": track.Genre, "Group": track.Grouping}
    Cur_tag = tag_assign[Tag]
    # CORRIGE AS BARRAS DE / PARA \     
    Cur = Cur_tag.replace(" / ","\\").strip()
    Cur = Cur.replace("/","\\").strip()
    Cur = Cur.replace(" \\ ","\\").strip()
    Cur_lst = Cur.split("\\")
    Cur_lst_order = Cur_lst
    Cur_lst = set(Cur_lst)
    # ORDENA A LISTA 
    Cur_lst = order_list(list(Cur_lst),Cur_lst_order)
    Cur_lst_lower = [x.lower() for x in Cur_lst]
    # NEW TO ADD
    New = New_tag.replace("Brazilian","Brasil")
    New = New.replace("Rock & Roll","Rock")
    New = New.replace("Hip Hop","Hip-Hop")
    New = New.replace("RnB","R&B")
    New = New.replace("RNB","R&B")
    New = New.replace("Rhythm & Blues","R&B")
    New = New.replace("Contemporary","")
    New = New.replace("Bossanova","Bossa Nova")
    if Is_Brasil(Cur_tag):
       New = New.replace("Latino","Brasil")
       New = New.replace("Latin","Brasil")
       New = New.replace("Worldwide","Brasil")
    if Is_Fave(Cur_tag):
       New = New.replace("OneHitWonders","")
    New = New.replace("/","\\").strip()
    New_lst = New.split("\\")

    # FIXES ELEMENTS IN LIST
    New_lst = [x.strip() for x in New_lst]
    
    for i in range(len(New_lst)):
        aux = New_lst[i].lower().strip()
        if aux != "" and aux not in Cur_lst_lower:
           Cur_lst.append(New_lst[i])
    
    # ORDENA A LISTA 
    Cur_lst_ordered = order_list(Cur_lst,Genre_order_list)

    # REMOVE BLANKS
    if "" in Cur_lst_ordered:
       Cur_lst_ordered.remove("")

    # FINAL
    Str = "\\".join(Cur_lst_ordered)
    if Str != "":
       Str = Str + "\\"
    if Str == Cur_tag:
       Str = "" 
    if Str != "":
       # check if the tag is valid
       if Tag.lower() in local_tags_dict:
          # get the attribute name from the dictionary
          attr_name = local_tags_dict[Tag.lower()]
          # update the attribute value of the track object dynamically
          setattr(track, attr_name, Str)
       else:
          print("Invalid tag in function Add_to_tag()")
    return Str
    # images_collec = img_func[srch_type](srch_ID).images

# adds or initiates the genre
# FULL_MATCH MEANS THE REM_TAG (VALUE TO BE REMOVED) NEEDS TO BE AN ELEMENT OF THE TAG LIST OF VALUES
# NOT FULL_MATCH MEANS REM_TAG CAN BE FOUND IN ANY ELEMENT OF THE TAG LIST OF VALUES
def Rem_from_tag(track,Rem_tag,Tag="Genre",Full_match=True):
    # Updates Genre
    Rem_lst = [x.lower().strip() for x in Rem_tag]
    # CURRENT VALUE
    tag_assign = {"Genre": track.Genre, "Group": track.Grouping}
    Cur_tag = tag_assign[Tag]
    # CORRIGE AS BARRAS DE / PARA \     
    Cur_lst = Cur_tag.split("\\")
    # FIXES ELEMENTS IN LIST
    Cur_lst = [x.strip() for x in Cur_lst]
    Cur_lst_order = Cur_lst
    Cur_lst = list(set(Cur_lst))
    # ORDENA A LISTA 
    Cur_lst = order_list(Cur_lst,Cur_lst_order)
    # REMOVE ELEMENT
    if Full_match:
                 New_lst = [x for x in Cur_lst if x.lower() not in Rem_lst and x != ""]
    else:
        New_lst = [x for x in Cur_lst if x.lower().find(Rem_tag.lower())==-1 and x != ""]             
    # ORDENA A LISTA 
    # Cur_lst_ordered = order_list(Cur_lst,Genre_order_list)
    # FINAL
    Str = "\\".join(New_lst)
    if Str != "":
       Str = Str + "\\"
    if Str == Cur_tag:
       Str = "" 
    if Str != "":
       # check if the tag is valid
       if Tag.lower() in local_tags_dict:
          # get the attribute name from the dictionary
          attr_name = local_tags_dict[Tag.lower()]
          # update the attribute value of the track object dynamically
          setattr(track, attr_name, Str)
       else:
          print("Invalid tag in function Handle_tag()")
    return Str

# Updates Genre 
def Uptd_genre(playlists,track,New_genre,Updt_cnt,arq):
    # ADDS NEW GENRE OR NOT
    New_genre = Add_to_tag(track,New_genre)
    if New_genre != '':
        track.Genre = New_genre
        Updt_cnt = Updt_cnt+1
        # add track to PL 
        Read_PL.Add_file_to_PL(playlists,"Found_Genre",arq)

# Updates YEAR 
def Uptd_year(playlists,track,New_year,Updt_cnt,arq):
    # UPDATE YEAR BY RE-READING MP3 TAG
    Cur_Year = track.Year
    Year_updated = False
    if New_year != 0:
       if Cur_Year>New_year or Cur_Year==0:
           track.Year = New_year
           Updt_cnt = Updt_cnt+1
           # add track to PL 
           Read_PL.Add_file_to_PL(playlists,"Found_Year",arq)  
           if Cur_Year>New_year:
              Year_updated = True
    return Year_updated           


# CHECK IF AA IS V.A.
VA=["various","vários","varios","ministry of sound","soundtrack","promo only","theme","promo","artist"]
def Is_VA(AA):
    AA_std = Stdz(AA)
    if AA_std in ['varios','various','va','v.a.']:
       res = True
    else:
       res = False
    return res

def Alb_by_art(Art,Title,AA):
    Art_std = Stdz(Art).split("^")
    AA_std = Stdz(AA).split("^")
    Title_std = Stdz(Title).split("^")
    Tags_non_null = Art.strip() != '' and AA.strip() != ''
    # searches Art in AA
    Achou1 = Tags_non_null
    for i in range(0,len(Art_std)):
        if Art_std[i] not in AA_std:
           Achou1 = False
    # searches AA in Art
    Achou2 = Tags_non_null
    for i in range(0,len(AA_std)):
        if AA_std[i] not in Art_std:
           Achou2 = False
    # searches AA in Title
    Achou3 = Tags_non_null and Title != ''
    for i in range(0,len(AA_std)):
        if AA_std[i] not in Title_std:
            Achou3 = False        
    res = Achou1 or Achou2 or Achou3
    return res

# COLETANEAS (TYPE OF KEYWORD THAT ARE UNDESIRABLE)
def Greatest_Hits(Album):
    Is_greatest = False
    for i in range(0,len(Great)):
        if Album.lower().find(Great[i])>=0:
           Is_greatest = True
    return Is_greatest        
           

# COLETANEAS (TYPE OF KEYWORD THAT ARE UNDESIRABLE)
def Nice_cover(Album,Group,Covers):
    Cur_group = "\\" + Group.lower().strip() + "\\"
    Is_Nice = Cur_group.find("\\ok\\")>=0
    if Covers>0:
       for i in range(len(Nice_lst)):
             if Album.lower().find(Nice_lst[i].lower())>=0:
                Is_Nice = True
    return Is_Nice

# RIGHT FOLDER
def Genre_is_live(Genre):
    Live = "live" in Genre.lower()
    return Live

def Album_is_live(Genre,Album):
    Live = False
    if "brasil" in Genre.lower() and Album.lower().find("ao vivo")>=0:
        Live = True
    if "brasil" not in Genre.lower():
        if Album.lower().find("live at")>=0:
           Live = True
        if Album.lower().find("live in")>=0:
           Live = True   
        if Album.lower().find("(live")>=0:
           Live = True 
        if Album.lower().find("[live")>=0:
           Live = True     
    return Live

# THE SIMPLEST COMPARISON 
# ONLY COMPLICATION IS THAT IT DISREGARDS "AO VIVO" IF GENRE HAS "LIVE"

# 2ND APPROACH
# CHECKS IF ALL THE INFO IN THE ARTIST TAG IS CONTAINED IN THE FILENAME (OR VICE-VERSA)
# PICKS THE SOURCE WITH THE MOST WORDS FOR ARTIST
# THE TITLES NEED TO BE THE SAME

# 3RD APPROACH
# CHECKS IF ALL THE INFO IN THE TAGS ARE CONTAINED IN THE FILENAME (OR VICE-VERSA)
# IF SO, THE SOURCE WITH THE MOST INFO IS PICKED (TAG OR FILENAME)

# 4RD APPROACH
# THIS MIGHT BE THE BEST APPROACH TO COMPARE
# dict = {"base": base_len, "comp": comp_len, "common": common_len, "max": max_len, "ratio": ratio, "match": Hit}

def file_tag_comp(track):
    # FROM TAGS
    Arq = track.location
    tag_Art = Simple_stdz(track.Artist)
    tag_Title = Simple_stdz(track.Name)
    tag_song = tag_Art + " " + tag_Title
    tag_Art_set = set(tag_Art.split(" "))
    tag_set = set(tag_song.split(" "))
    # FROM FILENAME
    file_dict = Files.file_to_art_title(Arq)
    dict = {}
    dict["match"] = False
    dict["best"] = None
    dict["method"] = None
    if file_dict["Ok"]:
       file_Art = Simple_stdz(file_dict["Art"])
       file_Title = Simple_stdz(file_dict["Title"])
       file_song = file_Art + " " + file_Title
       file_Art_set = set(file_Art.split(" "))
       file_set = set(file_song.split(" "))
       
       # 1ST APPROACH (THE FILENAME AND TAGS ARE ALREADY IN SYNC, INCLUDING ORDER)
       tag_Title2 = track.Name
       tag_Title2 = tag_Title2.replace(" / ",", ")
       tag_Title2 = tag_Title2.replace(" \\ ",", ")
       tag_song2 = Files.Replace_spec_chars(track.Artist + " - " + tag_Title2)
       file_no_nbr_no_ext = Files.File_no_nbr_no_ext(Arq)
       dict["match"] = tag_song2.lower() == file_no_nbr_no_ext.lower()
       if dict["match"]:
          dict["method"] = 1
          dict["best"] = "both"
        
       # 2ND APPROACH (eq_title_diff_art) THIS INCLUDES A PERFECT MATCH (BUT WO/ THE ORDER)
       if not dict["match"] and tag_Title==file_Title and (tag_Art_set.issubset(file_Art_set) or file_Art_set.issubset(tag_Art_set)):
          dict["match"] = True 
          dict["method"] = 2
          if len(tag_Art_set)>=len(file_Art_set):
             dict["best"] = "tags"
          else:
             dict["best"] = "file"
       
       # 3RD APPROACH (SUPERSET)
       if not dict["match"] and (tag_set.issubset(file_set) or file_set.issubset(tag_set)):
          dict["match"] = True 
          dict["method"] = 3
          if len(tag_set)>=len(file_set):
             dict["best"] = "tags"
          else:
             dict["best"] = "file"      
       
       # 4RD APPROACH (SIMILARITY RATIO)
       if not dict['match']:
          comp = similar_ratio(tag_song, file_song, thres = 0.97)
          print("\tSimilarity ratio is",comp["ratio"])
          if comp["match"]:
             dict['match'] = True
             dict["method"] = 4
             if len(tag_set)>=len(file_set):
                dict["best"] = "tags"
             else:
                dict["best"] = "file"
       
       if dict["match"]:
          if dict["best"] == "file": 
             dict["Art"] = Proper(file_dict["Art"])
             dict["Title"] = Proper(file_dict["Title"])
    
    # FINAL
    return dict


# REWRITE TAGS 
# HERE WE CHECK IF THE TAGS MATCH CASE INSENSITIVELY SINCE IT REQUIRES USER INPUT
# INSTEAD OF UPDATING THEM TO PROPER CASE IF THEY'RE NOT PROPER CASE
def Rewrite_tags(track,New_art,New_title):
    updt = False
    if exists(track.location):
       Arq = Files.file_wo_ext(track.location)
       Art = track.Artist
       Title = track.Name
       art_aux = Proper(New_art)
       title_aux = Proper(New_title)
       if art_aux.lower() != Art.lower():
          print("\nChanging Artist tag // Arq:",Arq)
          print("From",Art,"->",art_aux,"\n")
          inp = input("Press Enter to write Artist tag: ")
          if inp == "":
             track.Artist = art_aux
             updt = True
       if title_aux.lower() != Title.lower():
          print("\nChanging Title tag // Arq:",Arq)
          print("From",Title,"->",title_aux,"\n")
          inp = input("Press Enter to write Title tag: ")
          if inp == "":
             track.Name = title_aux
             updt = True
    return updt    

# USES THE TAGS TO RENAME THE FILE IF THEY'RE NOT IN SYNC
# REMEMBER STRINGS ARE NOT MUTABLE
def tag_2_file(track):
    Arq = Files.file_wo_ext(track.location)
    Art = track.Artist
    Title = track.Name
    subdir = Files.Folder(track.location)
    Title = Title.replace(" / ",", ")
    Title = Title.replace(" \ ",", ")
    tags_no_sp_chars = Files.Replace_spec_chars(Art + " - " + Title,"_")
    tags_no_sp_chars = re.sub(' +', ' ',tags_no_sp_chars)
    tags_no_sp_chars = tags_no_sp_chars.strip()
    tag_no_sp_chars_ext = tags_no_sp_chars + ".mp3" 
    # MAYBE FIND VALID FILE AS WELL? (THAT DOESN'T OVERWRITE)
    full_filename = Files.finds_valid_file(subdir,tag_no_sp_chars_ext)
    subdir = Files.Folder(full_filename)
    tag_no_sp_chars_ext = Files.file_w_ext(full_filename)
    dict = {"Subdir" : subdir , "Filename" : tag_no_sp_chars_ext}
    return dict


# GIVEN AN AA-ALBUM AND A DELIMITER, RETURNS EACH ONE SEPARATELY
def Split_AA_Album(Art,Title,AA_Album,delim=" - "):
    dict = {}
    dict['AA'] = ""
    dict['Album'] = ""
    if type(AA_Album)==str:
       if AA_Album.find(delim)==-1:
          delim = "-" 
       if AA_Album.find(delim)>=0:
          AA_Album_aux = AA_Album.split(delim)
          AA = AA_Album_aux[0].strip()
          Album = AA_Album_aux[1].strip()
          dict['AA'] = AA
          dict['Album'] = Album
          dict['quality'] = "accurate"
       else:
            dict['AA'] = Art
            dict['Album'] = AA_Album
            dict['quality'] = "unsure"
            Title_stdz = Simple_stdz(Title)
            Album_stdz = Simple_stdz(AA_Album)
            if Title_stdz.find(Album_stdz)>=0 or Album_stdz.find(Title_stdz)>=0:
               dict['quality'] = "unsure/overriden"
            #print("\tAlbum name missing dash")      
    return dict


# THIS CALCULATES A SCORE THAT TELLS ME WHICH COVER IS BETTER
# BELOW IS REALLY OUTDATED
def Album_score(Art,Title,AA,Album,Genre,Has_cover,Wid,Hei,Year_updt):
    Alb_not_miss = AA != '' and Album != ''
    Alb_by_art_aux = Alb_by_art(Art,AA,Title)
    Nice_cover_aux = Nice_cover(Album,Genre)
    Alb_not_great = not Greatest_Hits(Album)
    Yr_updt = Year_updt and Alb_by_art_aux
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
       Ratio = min(Wid,Hei)/(max(Wid,Hei)+0.1)>=.95 and Dim500
    Is_Now = Album.lower().find("now that's what")>-1
    Is_novela = False
    if Album[0:4].isnumeric():
        Is_novela = 1960<= int(Album[0:4]) <=2010
          
    # CREATES LIST WITH FACTORS TO BE CONSIDERED IN THE ORDER OF THEIR PRIORITY    
    Priority = [Alb_not_miss, Alb_by_art_aux, Has_cover, Nice_cover_aux, Alb_not_great, Is_novela, Is_Now, Ratio, Dim600, Dim550, Dim500, Dim450, Dim400]
    score_aux = 0.0
    for i in range(0,len(Priority)):
        power = len(Priority)-i-1
        score_aux = score_aux + (10**power)*Priority[i]
    # Score2 is a dictionary that'll be returned    
    score2 = {}    
    score2['score'] = score_aux
    score2['ratio'] = Ratio
    score2['alb_not_miss'] = Alb_not_miss
    score2['alb_by_art'] = Alb_by_art_aux
    return score2

# ARTISTS THAT CAN'T NOT HAVE THEIR TAGS CHANGED
def forbid_art(art):
    Achou = False
    if art.lower().find("roberto carlos")>=0:
        Achou = True
    if art.lower().find("raul seixas")>=0:
        Achou = True
    return Achou

# COALESCE FUNCTION
def coalesce(*args):
    pick = ""
    for arg in reversed(args):
        if arg != "":
           pick = arg
    return pick

def compress(input):
    #name = "Hello, 123! This is a sample phrase with symbols."
    input = unidecode(input)
    comp_name = re.sub(r'[^a-zA-Z0-9\s]', '', input)
    return comp_name
