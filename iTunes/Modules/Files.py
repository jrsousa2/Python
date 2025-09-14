from os.path import exists
import os
from re import sub
from datetime import datetime
from unidecode import unidecode
# This module obtains the MP3 ID3 tags indirectly
import eyed3
from tinytag import TinyTag
from mutagen.id3 import ID3, TXXX
from mutagen.mp3 import MP3

def Is_DMP3(Arq):
    if Arq.lower().find(":\\mp3\\")>=0:
       res = True
    else:
       res = False
    return res

# print(Alb_by_art("The clash feat. madonna","the madonna & the clash"))
def Folder_proper(Str):
    dirs = ["Brasil","Favorites","Playlists","Youtube","Z_to_move"]
    for i in range(len(dirs)):
        Str=Str.replace(dirs[i].upper(),dirs[i])
    return Str

# Removes speacial characters from the album name
def Replace_spec_chars(Str,Replc="_"):
    Repl_with = 8*Replc
    trans = Str.maketrans("\\/:*?\"<>",Repl_with)
    New_str = Str.translate(trans)
    return New_str

#print(Replace_spec_chars("Sun \\ Sylvia"))

# Gets the name of a file from a full path
def file_wo_ext(path):
    file = path[path.rfind("\\")+1:]
    pos = file.lower().rfind(".")
    if pos>=0:
       file_no_ext = file[0:pos]
       return file_no_ext
    else:
        return "" 

# Gets the name of a file from a full path
def file_w_ext(path):
    pos = path.rfind("\\")+1
    file_w_ext = path[pos:]
    return file_w_ext


# GETS THE EXTENSION OF A FILE NAME
def ext(file):
    #ext = arq[arq.rfind("."):]
    pos = file.rfind(".")
    if pos>=0:
       ext = file[pos:]
       return ext
    else:
        return ""   

# GETS THE FOLDER PART OF A FULL FILE NAME
def Folder(path):
    pos = path.rfind("\\")+1
    subdir = path[0:pos].upper()
    subdir = Folder_proper(subdir)
    return subdir

def File_no_nbr_no_ext(Arq):
    subdir = Folder(Arq)
    file = file_w_ext(Arq)
    file_no_nbr = sub(" \(\d+\)\.[mM][pP]3", ".mp3", file)
    file_no_nbr_no_ext = file_wo_ext(file_no_nbr)
    return file_no_nbr_no_ext

# GIVEN A FULL FILE NAME, RETURNS THE ART AND TITLE
def file_to_art_title(Arq):
    file_no_nbr_no_ext = File_no_nbr_no_ext(Arq)
    Art_Title = file_no_nbr_no_ext.split(" - ")
    dict = {}
    dict['Ok'] = False
    if len(Art_Title)==2:
        Art = Art_Title[0]
        Title = Art_Title[1]    
        dict['Ok'] = True
        dict['Art'] = Art
        dict['Title'] = Title
    return dict

# FINDS THE FIRST FILE NAME THAT WON'T OVERWRITE
# RETURNS FILE WITH PATH
def finds_valid_file(subdir,file_no_dir):
    nbr = 0
    file_no_dir = Replace_spec_chars(file_no_dir)
    file_no_ext = file_wo_ext(file_no_dir)
    ext2 = ext(file_no_dir)
    file_w_ext = subdir + file_no_dir
    while exists(file_w_ext) or len(file_w_ext)>255:
          nbr = nbr+1
          suffix = " ("+ str(nbr) + ")"
          aux_str = file_no_ext
          tam = min(255-len(subdir)-len(suffix)-len(ext2),len(aux_str))
          aux_str = aux_str[0:tam]
          file_w_ext = subdir + aux_str + suffix + ext2
    return file_w_ext

# RECEIVES A FILE AND DIR WHERE TO SEND THE FILE
def Move_covers(cover_file, To_dir):
    file_no_dir = file_w_ext(cover_file)
    new_path = finds_valid_file(To_dir, file_no_dir)
    os.rename(cover_file, new_path)

# Checks if file exists first
def Move_covers1(Srch_cover_file,Cur_cover_file,To_dir):
    # SRCH COVER
    Move_covers(Srch_cover_file,To_dir)
    # CUR COVER
    Move_covers(Cur_cover_file,To_dir)

# SRCH Move_covers2(Srch_cover_file,Cur_cover_file,VA2Art_new_folder)
def Move_covers2(Arq,To_dir,dic):
    Srch_AA = dic['AA1']
    Srch_Album = dic['Album1']
    Srch_cover_file = dic['cover1']
    Srch_Album_aux = Srch_AA + "@" + Srch_Album
    Srch_file_no_ext = file_wo_ext(Arq)
    Srch_ext = ext(Srch_cover_file) 
    Srch_file_no_dir = Srch_Album_aux + "@(new)@" + Srch_file_no_ext + Srch_ext
    Srch_final_file = finds_valid_file(To_dir,Srch_file_no_dir)
    os.rename(Srch_cover_file, Srch_final_file)
    # CURRENT
    Cur_AA = dic['AA2']
    Cur_Album = dic['Album2']
    Cur_cover_file = dic['cover2']
    Cur_Album_aux = Cur_AA + "@" + Cur_Album
    Cur_file_no_ext = Srch_file_no_ext
    Cur_ext = ext(Cur_cover_file)
    Cur_file_no_dir = Cur_Album_aux + "@(old)@" + Cur_file_no_ext + Cur_ext
    Cur_final_file = finds_valid_file(To_dir,Cur_file_no_dir)
    os.rename(Cur_cover_file, Cur_final_file)

def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

# CONVERTS TIME STRING TO SECONDS (INT)
def time_to_sec(time_str):
    min, sec = map(int, time_str.split(":"))
    return 60*min + sec


# PRINT ON SCREEN AND IN THE FILE
# args NEEDS TO BE A TUPLE
def Print_to_file(Arq, txt, *args):
    with open(Arq, "a", encoding="utf-8") as file:
         file.write(txt.format(*args))

def track_time():
    # Get the current time
    now = datetime.now()

    # Extract the hour and minute components from the current time
    hour = now.hour
    minute = now.minute
    day_of_week = now.strftime('%A %D')

    # Determine if it's morning or afternoon
    if hour < 12:
        period = "AM"
    else:
        period = "PM"

    # Convert hour to 12-hour format
    if hour == 0:
        hour = 12
    elif hour > 12:
        hour = hour - 12

    # Format the time string
    time_string = f"{day_of_week} {hour}:{minute:02d} {period}"

    # Display the time
    return time_string

# THIS ONE IS NOT VERY RELIABLE / TINYTAG IS BEST (MAYBE THIS STATEMENT IS NOT TRUE)
def read_eyed3(File, tag): #MP3_tag
    eyed3.log.setLevel("ERROR")
    value = ""
    if exists(File):
       audio = eyed3.load(File)

       # RESETS SOME ATTRIBUTE NAMES
       if tag.lower()=="art":
          tag = "artist"
       elif tag.lower()=="aa":
            tag = "album_artist"

        # GETS ATTRIBUTES
       if tag.lower()=="year":
          try:
              value = audio.tag.getBestDate().year
          except:
              value = 0    
       elif tag.lower()=="genre":
          try:
             obj = getattr(audio.tag, tag.lower())
             value= obj.name 
          except:
             tag = ""
       else: 
           value = getattr(audio.tag, tag.lower())
        
    if value == None:
       value = ""
    return value

# Pass the filename into the
# Tinytag.get() method and store
# the result in audio variable
def read_tinytag(File, tag):
    res = ""
    if exists(File):    
       audio = TinyTag.get(File)
       # REFORMATS SOME TAG NAMES              
       if tag.lower()=="art":
          tag = "artist"
       elif tag.lower()=="aa":
            tag = "albumartist"
       # GETS ATTRIBUTE
       res = getattr(audio, tag.lower())     
    else:
        print("Tag read error")

    if res == None:
       res = ""     
    return res

# OBTAIN ALL PROPERTIES OF TRACK AT A TIME (REQUESTED ONES IN COLS)
def tinytag_tags_dict(File,cols):
    dict = {}
    # PROPERTIES
    for key in cols:
        dict[key] = read_tinytag(File, key)
    return dict

# WRITES A CUSTOMIZED TAG WITH TINY TAG
def write_tag(path, tag, value):
    # Create a TinyTag object
    written = False
    if exists(path):
       # Load the MP3 file
       audio = ID3(path)

       # Add a custom tag (IF IT ALREADY EXISTS IT WILL BE OVERWRITTEN)
       try:
          audio["TXXX:"+ tag] = TXXX(encoding=3, desc=tag, text= value)
          audio.save(v2_version=3)
       except:
          print("Write tag failed")
       else:
           written = False   
    return written

# READS A CUSTOMIZED/EXTENDED TAG
def ext_tag_exist(path, tag):
    tag_exists = False
    if exists(path):
       # Load the audio file
       audio = ID3(path)

       # Check if the custom tag exists
       tag_exists = "TXXX:"+tag in audio
       
    return tag_exists

# READS A CUSTOMIZED TAG
def read_tag_mutag(path, tag):
    custom_value = False
    if exists(path):
       # Load the audio file
       audio = ID3(path)

       # Check if the custom tag exists
       if "TXXX:"+tag in audio:
           custom_value = audio["TXXX:"+tag].text[0]
       
    return custom_value

# USER TAGS USUALLY HAVE "TXXX:"
def remove_tag(path, tag):
    # Load the MP3 file
    audio = MP3(path, ID3=ID3)

    # Get all the tags
    tags_list = audio.tags

    # Check if the "COUNTRY" tag exists
    if tag in audio:
       del tags_list[tag]
       audio.save()
    else:
        print("Tag",tag,"not found in the file.")

# COMPARES TWO SETS OR LISTS CASE-INSENTITIVE
# ELEMENTS THAT ARE IN orig_set_lower BUT NOT IN comp_set_lower.
def Set_diff(orig, comp):
    # CREATES SETS
    orig_set_lower = {item.lower() for item in orig}
    comp_set_lower = {item.lower() for item in comp}

    # TAKES THE DIFFERENCE OF THE 2 SETS    
    diff_lower = orig_set_lower.difference(comp_set_lower)
    
    # FOR EACH ELEMENT IN THE DIFFERENT OF THE 2 SETS, FINDS ORIGINAL VALUE (NON LOWERCASE)
    diff = [item for item in orig if item.lower() in diff_lower]
    # TURNS LIST TO SET
    diff = set(diff)
    
    return diff

# INTERSECTION BT TWO LISTS OR SETS
def Set_common(orig, comp):
    # Create lowercase sets
    orig_set_lower = {item.lower() for item in orig}
    comp_set_lower = {item.lower() for item in comp}

    # Take the intersection
    common_lower = orig_set_lower.intersection(comp_set_lower)
    
    # Map back to original-case items from orig_set
    common = [item for item in orig if item.lower() in common_lower]
    
    # Convert to set
    common = set(common)
    
    return common

# SCANS A WINDOWS FOLDER FOR FILES 
# CLEANS-UP THE RESULTS FOR OPTIMAL SEARCH AND RETURNS A LIST OF TUPLES
# THE SECOND ELEMENT IN THE TUPLE IS THE FILE LOWER CASE, UNIDECODED AND WO/ EXTENSION
def get_Win_files(dir, exts, Progress=False, Ref_total=None):

    if Progress:
        print("Reading files in", dir,"\n")
        # total_files = sum(len(files) for _, _, files in os.walk(dir))
        # total_files = 65000
        process = 0

    file_list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            # ADDS FILE TO LIST ONLY IF MP3 (OR EXTS PROVIDED)
            # TURNS EXTS INTO TUPLE TO SUPPLY TO FUNCTION ENDSWITH
            if file.lower().endswith(tuple(ext.lower() for ext in exts)):
                # PRINT PROGRESS EVERY 100 FILES
                if Progress:
                    process += 1
                    if process % 1000 == 0 or process == Ref_total:
                        print(f"File {process} of {Ref_total}", end="\r")
                        if process == Ref_total:
                            print("\n")
                file_list.append(os.path.join(root, file))        
    
    # NORMALIZE FILE LIST FOR SEARCHES IGNORING CASE AND ACCENTS
    normal_filelist = [(file, unidecode(file_wo_ext(file.lower()))) for file in file_list]           
    return normal_filelist
