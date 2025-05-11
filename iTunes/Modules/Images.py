# SUBROUTINE CALLED BY OTHER CODES.
# Search Apple's db
from requests import get
from PIL import Image
from urllib import request
from sys import exit
# Below is for the dims function
#import stagger #traceback
from stagger import id3, read_tag
from io import BytesIO 
from os.path import exists
from os import remove
# BELOW IS TO DETECT COVER SIZE
from mutagen.id3 import ID3
from unidecode import unidecode
#from os import rename, remove
import Files
import Tags

import imagehash

import cv2
#import numpy as np

# VARIABLE USED IN THE iTunes FUNCTIONS
ExtArray = [".unk",".jpg",".png",".bmp"]

base_url = "https://itunes.apple.com/search/"


# MEDIA TYPE: music: entity
# musicArtist, musicTrack, album, musicVideo, mix, song.
# Please note that “musicTrack” can include both songs and music videos in the results.

# MEDIA TYPE: music: attributes
# mixTerm, genreIndex, artistTerm, composerTerm, albumTerm, ratingIndex, songTerm

# THIS IS THE QUCIK VERSION OF THE APPLE QUICK SEARCH
def get_Apple_cover_url(srch_term, srch_limit=1, srch_by="Album"):
    # Get a pmts using the base_url. General purpose GET interface
    pmts = {}
    # THE KEYWORD THAT IS USED FOR THE SEACH (E.G. AA+ALBUM)
    pmts["term"] = srch_term
    # NUMBER OF SEARCHES? 1 IS BEING USED IN THE OTHER CODE
    pmts["limit"] = srch_limit
    # TYPE OF MEDIA
    pmts["media"] = "music"
    
    # Search type
    if srch_by.lower()=="title":
       pmts["entity"] = "musicArtist,musicTrack,song"
    else:
        pmts["entity"] = "musicArtist,album"

    # SEARCHES
    data = get(base_url, params = pmts)
    srch_url = data.url

    dict = []
    nbr_res = 0
    # Apparently only 200 means no error
    if data.status_code == 200:
       try:
          parsed = data.json()
       except Exception:
           print("Json exception")
       else:  
         nbr_res = parsed["resultCount"]
         dict = [parsed["results"][i] for i in range(nbr_res)]
         
    # REPLACES THE URL WITH A BETTER RESOLUTION
    # dict is a LIST of dictionaries
    list = []
    Found = False
    j = 0
    while (j<min(nbr_res,10)):
           URL = dict[j].get("artworkUrl100", "")
           j = j+1
           if URL != "":
              Found = True
              size = 600
              URL = URL.replace("100x100bb", "%sx%s" % (size, size))  
              list.append(URL)  
    # A URL DA IMAGEM
    return list

# PERFORMS A SEARCH ON DISCOGS
def get_discogs_cover_url(disco,srch_type,AA,Album):
    list = []
    # READS THE INPUT PMTS
    params = {"type": srch_type, "artist": AA, "title": Album}

    # REMOVES EMPTY PARAMETERS
    params = {k: v for k, v in params.items() if v}

    # CALLS THE FUNCTION WITH THE PARAMETERS
    results = disco.search(**params)
    
    # UPDATES LIST
    # ERROS APARECERAM NESSA PARTE
    try:    
        nbr_res = results.count
    except Exception:
        nbr_res = 0 
    # CHECK 
    if nbr_res>0 and results is not None:
       nbr_pages = results.pages
       nbr_matches = min(nbr_res,10)
       # LIST OF MATCHES
       j = 0
       while(j<nbr_matches):
             try:
                Obj = results[j]
                ID = Obj.id
                if srch_type=="master":
                   img = disco.master(ID).images[0]
                else:
                   img = disco.release(ID).images[0]
             except Exception:
                Obj = None
                Obj_exists = False
             else:
                ratio = max(img["width"],img["height"])/min(img["width"],img["height"])
                if ratio<=1.01 and min(img["width"],img["height"])>=500:
                   URL = img["uri"]
                   list.append(URL)    
             j = j+1   
    return list 

# CALL EXAMPLE
# get_Apple_cover_url("The Beatles Abbey Road",1)

# Tirei mix da busca
def get_Apple_cover(term, limit, dict, srch_by):
    # Get a payload using the base_url. General purpose GET interface
    payload = {}
    payload['term'] = term
    payload['limit'] = limit
    
    # Search type
    if srch_by.lower()=="title":
       payload['entity'] = "musicArtist,musicTrack,song"
    else:
        payload['entity'] = "musicArtist,album"
    payload['media'] = 'music'

    data = get(base_url, params = payload)

    # Apparently only 200 means no error
    if data.status_code == 200:
       try:
          parsed = data.json()
       except Exception as erro1:
           print("Json exception")
           vec = {"N" : 0, "Json exc" : 0, "search" : data.url} 
           dict.append(vec)
       else:    
         for i in range(0,parsed['resultCount']):
             dict.append(parsed['results'][i])
         
         # Handle results    
         if parsed['resultCount']==0:
            vec = {"N" : 0, "Json exc" : 0, "search" : data.url} 
            dict.append(vec)
         else:   
             dict[0]['N'] = parsed['resultCount']
             dict[0]['Json exc'] = 0
             dict[0]['search'] = data.url 
    else:
        vec = {"N" : 0, "Json exc" : 0, "search" : data.url} 
        dict.append(vec)          

# DOWNLOADS AND SAVES THE DISCOGS IMAGE FILE LOCALLY
# AA AND ALBUM ARE THOSE FROM THE COVER THAT WILL BE DOWNLOAD
def Dwld_cover(Arq,AA,Album,URL,path,order="file",tag="New",Remove_accent=False):
    # Logic
    Album_aux = AA +"@"+ Album
    file_no_ext = Files.file_wo_ext(Arq)
    ext = Files.ext(URL)
    # NEEDED TO INDICATE IF DOWNLOAD WORKED 
    filename = ""
    if ext != "":
       if order=="file":
          aux_str = file_no_ext + "@("+ tag +")@" + Album_aux
       else:
           aux_str = Album_aux + "@("+ tag +")@" + file_no_ext
       # TRIMS TO AVOID EXCEDING MAX LENGTH
       tam = min(255-len(path)-len(ext),len(aux_str))
       aux_str = aux_str[0:tam]
       filename = path + aux_str + ext
       if Remove_accent:
                       filename = unidecode(filename)
       # FINDS FILE THAT DOESN'T OVERWRITE
       file_no_dir = Files.file_w_ext(filename)
       to_folder = Files.Folder(filename)
       filename_final = Files.finds_valid_file(to_folder, file_no_dir)
       try:
           dwld = request.urlretrieve(URL, filename_final)
       except Exception as e:
           exit(f"Unable to download cover, error {e}")
           filename_final = ""
    return filename_final


# DOWNLOAS AND SAVES THE APPLE IMAGE FILE LOCALLY
def Dwld_cover_Apple(Arq,busca,path):
    # Logic
    Srch_AA = busca.get('AA','')
    Srch_Album = busca.get('Album','') 
    URL = busca.get('URL','')
    Album_aux = Srch_AA +"@"+ Srch_Album
    file_no_ext = Files.file_wo_ext(Arq) 
    ext = Files.ext(URL) 
    filename = ""
    if ext != '':
        dwld = get(URL, allow_redirects=True)
        aux_str = file_no_ext + "@(new)@" + Album_aux
        tam = min(255-len(path)-len(ext),len(aux_str))
        aux_str = aux_str[0:tam]
        file_no_dir = aux_str + ext
        filename = Files.finds_valid_file(path, file_no_dir)
        open(filename,'wb').write(dwld.content) 
    return filename

# AFTER IMG HAS BEEN DOWNLOADED AND SAVED, ATTACHES IT TO THE TRACK
# KW VA IS TO INDICATE THAT A PREVIOUS VA COVER WAS DELETED AND REPLACED
def Attach_cover(Log_file,track,New_AA_vl,New_Album_vl,New_cover_file,fix_Album,VA=False,Del_after_attach=False):
    # INFO FOR THE LOG FILE
    Cur_AA = track.AlbumArtist
    Cur_Album = track.Album
    Cur_AA_Album = Cur_AA + " - " + Cur_Album
    Arq = track.Location
    file_nm = Files.file_wo_ext(Arq)
    # THE NEW ALBUM
    New_AA_Album = New_AA_vl + " - " + New_Album_vl
    # FIRST CHECKS ENSURE IF COVERS EXIST (IF THE COVER CAN BE SAVED FROM iTUNES)
    if VA:
       dict = Has_artwork(track,"D:\\Z-Covers\\Deleted_VA_covers\\")
    else:
        dict = Has_artwork(track)   
    Has_cover = dict['Has_cover'] or dict['Isdownl']
    # Cur_cover_file = dict['image']
    Change_tag = exists(New_cover_file)
    # TRIES TO DELETE COVER
    # ONLY DELETE THE CURRENT COVER IF THE NEW ONE EXISTS
    Tag_updated = False
    Deleted = False
    Delete_exc = False
    Attached = False
    Attach_exc = False
    if Has_cover and Change_tag:
       try:
          itu_Cover = track.Artwork.Item(1) 
          itu_Cover.Delete()
       except:  
          print("\tCover deletion failed")
          Files.Print_to_file(Log_file,"Cover deletion failed\n")
          Change_tag = False
          Delete_exc = True
       else:
          print("\tCover deleted!")
          # Files.Print_to_file(Log_file,"Cover deleted!\n")
          Deleted = True
          #Covers[i] = False
          #AA[i] = ""
          #Album[i] = ""

    # THIS NEEDS TO COME ONLY AFTER COVER DELETION
    if Change_tag:
       track.AlbumArtist = New_AA_vl
       track.Album = New_Album_vl
       fix_Album = fix_Album+1
       Tag_updated = True
       print("\tUpdated Album of",file_nm)
       print("\tFrom",Cur_AA_Album ,"->",New_AA_Album,"(",fix_Album,"updates)")
       Files.Print_to_file(Log_file,"Updated Album of {} ({} updates)\n", file_nm, fix_Album)
       Files.Print_to_file(Log_file,"From @{}@ To @{}@\n", Cur_AA_Album, New_AA_Album)

       # TRY TO MODIFY THE ARTWORK 
       try:
           track.AddArtworkFromFile(New_cover_file)
       except:
            Attach_exc = True
            print("\tAttach exception has occurred")
            Files.Print_to_file(Log_file,"Attach exception has occurred\n")
       else:
           Attached = True
           if Del_after_attach:
              remove(New_cover_file)
    # FINAL    
    dict = {}
    dict['Tag_updt'] = Tag_updated
    dict['Attached'] = Attached
    dict['Deleted'] = Deleted
    dict['Exception'] = Attach_exc

    # ATTACHED? PRINTS RESULT ON THE SCREEN
    attached_res = "Attached" if Attached else "Not attached"
    has_cover_res = "Had cover," if Has_cover else "Had no cover,"
    deleted_res = "cover deleted," if Deleted else "cover not deleted,"
    attach_exc_res = "attach exception" if Attach_exc else "no attach exception"
    # PRINTS
    print("\tResult of cover attachment for",file_nm,":",attached_res)
    print("\t",has_cover_res,deleted_res,attach_exc_res,"\n")
    Files.Print_to_file(Log_file,"Result of cover attachment for {}: {}\n", file_nm, attached_res)
    Files.Print_to_file(Log_file,"{} {} {}\n", has_cover_res, deleted_res, attach_exc_res)
    return dict

# SAVES A FILE FROM ITUNES TO THE LOCAL DISK
# ORDER: FILE FIRST OR ALBUM FIRST
def Save_cover_iTu(track,iTu_detach_folder,tag="old",order="file",Remove_accent=False):
    #track = tracks.Item(m)
    Arq = track.Location
    Cur_AA = track.AlbumArtist
    Cur_Album = track.Album
    Artobj = track.Artwork
    Art_count = Artobj.Count
    Detach_res = False
    Cur_cover_file = ""
    if Art_count>0:
       try:
          itu_Cover = Artobj.Item(1)
          Format = itu_Cover.Format
       except Exception:
          print("iTunes cover can't be saved")
          Art_count = 0 
       if Art_count>0:
          file_no_ext = Files.file_wo_ext(Arq)
          Cur_Album_aux = Cur_AA +"@"+ Cur_Album
          if order=="file":
             Cur_final_file = file_no_ext + "@("+ tag +")@" + Cur_Album_aux + ExtArray[Format]
          else:
              Cur_final_file = Cur_Album_aux + "@("+ tag +")@" + file_no_ext + ExtArray[Format]   
          # Cur_final_file = file_no_ext + ExtArray[Format]
          # SEARCHES A FILE NAME THAT DOESN'T OVERWRITE ANOTHER FILE
          if Remove_accent:
                          Cur_final_file = unidecode(Cur_final_file)
          Cur_cover_file = Files.finds_valid_file(iTu_detach_folder,Cur_final_file)
          try:
             itu_Cover.SaveArtworkToFile(Cur_cover_file)
          except Exception:
             print("iTunes cover save failed")
          else:
             Detach_res = True
    return Cur_cover_file

# CHECKS ITUNES ARTWORK (IT'S NOT JUST HAS ARTWORK, NEED TO CHECK IF IT'S ATTACHED)
def Has_artwork(track,iTu_detach_folder="D:\\Z-Covers\\Check artwork\\"):
    Has_artwork = False
    IsDownlArtw = False
    Artobj = track.Artwork
    Artobj_Count = Artobj.Count
    Cur_cover = ""
    if Artobj_Count>0:
       Cur_cover = Save_cover_iTu(track,iTu_detach_folder,tag="check art",order="file")
       if Cur_cover != "":
          Has_artwork = True 
       error = False
       for i in range(1,Artobj_Count+1):
           Art = Artobj.Item(i)
           try:
               if Art.IsDownloadedArtwork:
                  IsDownlArtw = True
           except Exception:
                  error = True
    # dict = {'Has_artwork': Artwork, 'Not_attached': IsDownlArtw, 'Exception': Except} 
    # AN ITUNES NON ATTACHED COVER IS NOT CONSIDERED A COVER (NOT RELIABLE)  
    Artwork_Ok = Has_artwork and not IsDownlArtw and not error
    dict = {}
    dict['Has_cover'] = Artwork_Ok
    dict['Isdownl'] = IsDownlArtw
    dict['image'] = Cur_cover
    return dict

# FORMATS IMAGE
def Read_and_resize(path, desired_size = (600, 600), gray_scale=True):
    # Load the template as grayscale
    if gray_scale:
       img = cv2.imread(path, cv2.IMREAD_GRAYSCALE) 
    else:
       img = cv2.imread(path)    
    # Set the desired size for resizing
    img_resized = cv2.resize(img, desired_size)
    return img_resized

# COMPARE IMAGES #cv2.COLOR_BGR2GRAY
def Compare_imgs(img_resized, template_resized, threshold=0.7, show_img=False):
    match = False
    if img_resized is not None and template_resized is not None:
       # Display the masked image and template
       if show_img:
          cv2.imshow("Masked Image", img_resized)
          cv2.imshow("Masked Template", template_resized)
          cv2.waitKey(0)
          cv2.destroyAllWindows() 

       result = cv2.matchTemplate(img_resized, template_resized, cv2.TM_CCOEFF_NORMED)
       min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

       # FINAL
       if max_val >= threshold:
          match = True
    dict = {}      
    dict["match"] = match
    dict["metric"] = round(max_val,6)
    return dict

# RETURNS THE SIZE OF THE COVER IN BYTES
def Cover_size(Arq):
    # Open the MP3 file
    image_size = 0
    Img_not_found = False
    try:
        mp3_file = ID3(Arq)
        # Get the image information
        if "APIC:" in mp3_file:
            image_data = mp3_file.get('APIC:').data
            image_size = len(image_data)
            # print(f"Image size: {image_size} bytes")
        else:
            Img_not_found = True
            # print("No image found in file",Arq)
    except:
        Img_not_found = True
        print("Exception getting the cover size")
    dict = {}
    dict["Img_not_found"] = Img_not_found
    dict["Size"] = image_size
    return dict  

# COVER IMG DIMENSIONS (formerly DIM)
# THIS IS FROM PIL (Pillow). 
# IT'S BETTER THAN THE OTHER FUNCTION BELOW (mutagen.id3)
def Wid(image):
    #filename = os.path.join('path', 'to', 'image', 'file')
    try:
        img = Image.open(image)
    except Exception:
        wid = 0 
    else:
        wid = img.size[0]
        if wid is None:
           wid = 0 
    return wid

# COVER IMG DIMENSIONS
def Hei(image):
    #filename = os.path.join('path', 'to', 'image', 'file')
    try:
        img = Image.open(image)
    except Exception:
        hei = 0 
    else:
        hei = img.size[1]
        if hei is None:
           hei = 0 
    return hei

# GRABS DIMS OF THE COVER WITHOUT DETACHING THE FILE
# THIS IS FROM mutagen.id3 AND IS NOT AS GOOD AS THE ONE FROM PIL ABOVE
def Img_dims(arq):
    dict = {}
    dict['Hei'] = 0
    dict['Wid'] = 0
    try:
        mp3 = read_tag(arq)
        img = Image.open(BytesIO(mp3[id3.APIC][0].data))
        # im.save("cover.jpg") # save cover to file
    except:
        dict['Has_cover'] = False
        print("Exception finding the cover dimensions")
        #print(traceback.format_exc())
    else:
        hei = int(img.size[0])
        wid = int(img.size[1])
        if hei>0 and wid>0:
           dict['Has_cover'] = True
        else:
            dict['Has_cover'] = False   
        dict['Hei'] = hei
        dict['Wid'] = wid
    return dict

def Width(Arq):
    dict = Img_dims(Arq)
    return dict["Wid"]

def Height(Arq):
    dict = Img_dims(Arq)
    return dict["Hei"]

# THIS FUNCTION COMPARES TWO IMAGES AND TELLS IF THEY ARE THE SAME
def Compare(Arq1,Arq2):
    # Load the two images to compare
    img1 = Image.open("image1.jpg")
    img2 = Image.open("image2.jpg")

    # Calculate the hash for each image
    hash1 = imagehash.average_hash(img1)
    hash2 = imagehash.average_hash(img2)

    # Compare the two hashes and print the result
    if hash1 == hash2:
        print("The images are the same!")
    else:
        print("The images are different.")

# DECIDE WHICH SCALE TO USE
def Gray_scale(AA):
    gray_scale = True
    if Tags.Is_VA(AA):
       gray_scale = False
    return gray_scale 