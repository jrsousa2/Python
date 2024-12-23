# MOVES FILES TO THE RIGHT FOLDER 
# ESSE MODULO TB CORRIGE O CASE DOS FILENAMES
# 1o ADICIONA TRACKS NA PLAYLIST

from os import rename
from os.path import exists
#import Move
import Read_PL
import Tags

def Call_Alb_by_art(PL_name=None,PL_nbr=None,Do_lib=False):
    # CALLS FUNCTION
    col_names =  ["Arq","Art","Title","AA","ID"]
    dict = Read_PL.Read_PL(col_names,PL_name=PL_name,PL_nbr=PL_nbr,Do_lib=Do_lib)
    # ASSIGNS
    App = dict['App']
    PLs = dict['PLs']
    df = dict['DF']

    # TEST LIST CREATION (list comprehension) 
    Arq = [x for x in df['Arq']]
    Art = [x for x in df['Art']]
    Title = [x for x in df['Title']]
    AA = [x for x in df['AA']]
    ID = [x for x in df['ID']]
    nbr_files = len(Arq)

    # CHAMA A FUNCAO QUE CRIA A PL
    # CRIA PLAYLIST APENAS SE HOUVER ARQUIVOS 
    Created_PL_name = "Alb_by_Art"
    if nbr_files>0:
       Move_PL = Read_PL.Cria_PL(Created_PL_name,recria="y")

    # REASSIGNS PLAYLIST
    for i in range(nbr_files):
        file_exists = exists(Arq[i])
        # Stdz.Is_DMP3(Arq[i]) and 
        if file_exists:
           Alb_by_art_vl = Tags.Alb_by_art(Art[i],Title[i],AA[i])
           if (i+1) % 100==0:
              print("Checking file",i+1,"of",nbr_files)
           if Alb_by_art_vl:
              track = App.GetITObjectByID(*ID[i])
              Read_PL.Add_track_to_PL(PLs,Created_PL_name,track)

def Call_great_hits(PL_name=None,PL_nbr=None,Do_lib=False,rows=None):
    # CALLS Read_PL FUNCTION
    col_names =  ["Arq","Art","Title","AA","Album"]
    dict = Read_PL.Read_PL(col_names,PL_name=PL_name,PL_nbr=PL_nbr,Do_lib=Do_lib,rows=rows)
    PLs = dict['PLs']
    df = dict['DF']

    # TEST LIST CREATION (list comprehension) 
    Arq = [x for x in df['Arq']]
    Art = [x for x in df['Art']]
    Title = [x for x in df['Title']]
    AA = [x for x in df['AA']]
    Album = [x for x in df['Album']]
    nbr_files = len(Arq)
    #Genre = [x for x in df['Genre']]

    # CHAMA A FUNCAO QUE CRIA A PL
    # CRIA PLAYLIST APENAS SE HOUVER ARQUIVOS 
    Created_PL_name = "Great_hits"
    if nbr_files>0:
       Move_PL = Read_PL.Cria_PL(Created_PL_name,recria="y")

    # REASSIGNS PLAYLIST
    for i in range(nbr_files):
        file_exists = exists(Arq[i])
        if file_exists:
           Alb_by_art_vl = Tags.Alb_by_art(Art[i],Title[i],AA[i])
           Great_hits_vl = Tags.Greatest_Hits(Album[i]) and Alb_by_art_vl and not Tags.forbid_art(Art[i])
           if (i+1) % 100==0:
              print("Checking file",i+1,"of",nbr_files,":",Arq[i])
           if Great_hits_vl:
              Read_PL.Add_file_to_PL(PLs,Created_PL_name,Arq[i])

def Call_Alb_by_art(PL_name=None,PL_nbr=None):
    # CALLS FUNCTION
    col_names =  ["Pos","Arq","Art","Title","AA","Album","ID"] 
    dict = Read_PL.Read_PL(col_names,PL_name=PL_name,PL_nbr=PL_nbr) 
    App = dict['App']
    PLs = dict['PLs']
    tracks = dict['tracks']
    df = dict['DF']
    
    # TEST LIST CREATION (list comprehension) 
    Arq = [x for x in df['Arq']]
    Art = [x for x in df['Art']]
    Title = [x for x in df['Title']]
    AA = [x for x in df['AA']]
    ID = [x for x in df['ID']]
    Album = [x for x in df['Album']]
    nbr_files = len(Arq)
    #Genre = [x for x in df['Genre']]

    # CHAMA A FUNCAO QUE CRIA A PL
    # CRIA PLAYLIST APENAS SE HOUVER ARQUIVOS 
    Created_PL_name = "Greatest_Hits"
    if len(Arq)>0:
        Move_PL = Read_PL.Cria_PL(Created_PL_name,recria="y")
    
    # LISTA DE GREATEST HITS
    print("Building lists of greatest hits")
    Greatest_hits = [i for i in range(nbr_files) if exists(Arq[i]) and Tags.Greatest_Hits(Album[i])]

    # STATS
    print(nbr_files,"files,",len(Greatest_hits),"greatest hits")

    # READS PLAYLISTS
    for i in range(nbr_files):
        if (i+1) % 100==0:
           print("Added",m,"of",nbr_files,"files to playlist")
        m = ID[i]   
        track = App.GetITObjectByID(*m)
        if track.Kind == 1:
            Read_PL.Add_track_to_PL(PLs,Created_PL_name,track)

# IDENTIFIES FILES WITH CONFLICT BETWEEN ARTIST AND AA TAGS
# ESSE DAQUI AINDA NAO ESTA ACABADO
from os.path import exists
#import requests #Used by function Salva
import Tags
import time
import Busca
from os import rename
from re import sub
import Read_PL

# MAIN CODE
def AA_check(PL=None):
    #override_art=False
    # CALLS FUNCTION
    col_names =  ["Pos","Arq","Art","Title","AA","Album","Genre","Year"]
    dic = Read_PL.Read_PL(col_names,PL_nbr=PL)
    #dic = Read_PL.Read_PL(col_names,PL_nbr=37)
    PLs = dic['PLs']
    tracks = dic['tracks']
    result = dic['PL']
    df = dic['DF']

    # TEST LIST CREATION (list comprehension) 
    Pos = [x for x in df['Pos']]
    Arq = [x for x in df['Arq']]
    Art = [x for x in df['Art']]
    Title = [x for x in df['Title']]
    AA = [x for x in df['AA']]
    Album = [x for x in df['Album']]
    Genre = [x for x in df['Genre']]
    Year = [x for x in df['Year']]
    #Year = [x if x.lower() !='empty' else '' for x in df['Year']]

    # dictionary of lists
    main_dic = {}
    main_dic['Arq'] = Arq
    main_dic['Art'] = Art
    main_dic['Title'] = Title
    main_dic['AA'] = AA
    main_dic['Album'] = Album
    main_dic['Genre'] = Genre
    main_dic['Year'] = Year

   # CREATES THE PLAYLISTS
    AA_nm = "AA_check"
    AA_nm_PL = Read_PL.Cria_PL(AA_nm,recria="y")

    # REASSIGNS PLAYLIST
    read_PL = PLs.Item(result)
    # playlistName = read_PL.Name
    print("Doublecheck playlist:",read_PL.Name,"\n")
    # tracks = read_PL.Tracks

    # Initializes list
    to_fix_dic = []
    # CHECKS IF TRACK HAS ART:
    print("Creating list of files with wrong AA\n")
    for i in range(0,len(Arq)):
        if exists(Arq[i]):
           m = Pos[i]
           Alb_is_ok = Genre[i].lower().find("iscorrect")>=0
           #track = tracks.Item(m)
           # CREATES VARS TO USE
           if not Alb_is_ok:
              if AA[i] != '' and Album[i] != '' and not Tags.Is_VA(AA[i]) and not Tags.Alb_by_art(Art[i],AA[i]):
                 Read_PL.Add_file_to_PL(PLs,AA_nm,Arq[i]) 
                 to_fix_dic.append(i)

    print("Files with wrong AA:",len(to_fix_dic))
    print("")

# CALLS FUNC
AA_check(PL=12)

# CALLS FUNC
Call_Alb_by_art()

# CALLS FUNC
Call_great_hits(PL_name="ALL")

# CALLS FUNC
Call_Alb_by_art(PL_name="ALL")