# I THINK THIS CODE IS TO REPLACE NEW VA COVERS WITH THEIR ORIGINAL VA COVER
# PARECE QUE ELE TB SUBSTITUI AS CAPAS POR SUAS MELHORES VERSOES
# ESTE PGM NAO DEVE DE PRECISAR SER USADO FREQUENTEMENTE
import pandas as pd
from os.path import exists
import Tags
import Read_PL
from Cover_logic import Save_cover_iTu
from Images import Img_dims

ExtArray = [".unk",".jpg",".png",".bmp"]

# DIRECTORY
VA_transf_dir = "D:\\Z-Covers\\Rz_VA_cover_transfer\\"

# This program will receive a DF and check which files can have tags or art transferred

def Transfer(PL=None):

    # CALLS FUNCTION
    col_names =  ["Pos","Arq","Art","Title","AA","Album","Genre","Len"]
    dic = Read_PL.Read_PL(col_names,PL_nbr=PL)
    #dic = Read_PL.Read_PL(col_names,PL_nbr=37)
    playlists = dic['PLs']
    tracks = dic['tracks']
    result = dic['PL']
    df = dic['DF']

    #override_art=False
    # POPS LISTS
    Arq = [x for x in df['Arq']]
    Art = [x for x in df['Art']]
    Title = [x for x in df['Title']]
    AA = [x for x in df['AA']]
    Album = [x for x in df['Album']]
    Len = [x for x in df['Len']]
    Genre = [x for x in df['Genre']]

    # PLAYLISTS
    PL_transf_albs = "VA_transfer_albs"
    PL_transf_albs_res = Read_PL.Create_PL(PL_transf_albs,recreate="y")
    PL_del_cover = "VA_transfer_del_cover"
    PL_del_cover_res = Read_PL.Create_PL(PL_del_cover,recreate="y")
    PL_del_AA_tags = "VA_transfer_del_tags"
    PL_del_AA_tags_res = Read_PL.Create_PL(PL_del_AA_tags,recreate="y")

    # REASSIGNS PLAYLIST
    read_PL = playlists.Item(result)
    playlistName = read_PL.Name
    print("Doublecheck playlist:",read_PL.Name,"\n")
    tracks = read_PL.Tracks

    # Cria nova lista baseada nos nomes
    track_stdz = []
    #Nice_cover = []
    for i in range(0,len(Arq)):
        track_stdz.append(Tags.Stdz(Art[i]+" - "+Title[i]))

    # CREATES COL.
    df["track_stdz"] = track_stdz

    # WHAT I REALLY NEED IS TO FLAG TRACK'S WHOSE ALBUMS THAT HAVE DIFFERENT SCORES
    df['Count'] = df.groupby('track_stdz')['Pos'].transform('count')
    
    # CONCATENATE AA+ALBUM
    df['AA_Album_aux'] = df['AA'] +"@" + df['Album']
    # ALBUMS WHERE SOME FILES HAVE ALB BY ART AND OTHERS DON'T
    #df['Dist2'] = df.groupby('track_stdz')['AA_Album_aux'].transform("nunique").astype(int)

    # SORTS 
    # CRIA COL. Location Lower case
    df['Arq_lower'] = df['Arq'].str.lower()
    df = df.sort_values(['Count','track_stdz','Arq_lower'], ascending=[False, True, True])
    
    # RE-POPULATES LISTS
    Pos = [x for x in df['Pos']]
    Arq = [x for x in df['Arq']]
    Art = [x for x in df['Art']]
    Title = [x for x in df['Title']]
    AA = [x for x in df['AA']]
    Album = [x for x in df['Album']]
    Genre = [x for x in df['Genre']]
    Len = [x for x in df['Len']]
    track_stdz = [x for x in df['track_stdz']]
    Count = [x for x in df['Count']]
    
    # NAO VOU CONSIDERAR ARQS REPETIDOS POR ENQTO
    # df['Count'] = df.groupby('Arq_lower')['Pos'].transform('count')

    ##########################################################
    # ARTWORK 
    # Initializes list
    Covers = []
    Wid = []
    Hei = []
    # CHECKS IF TRACK HAS ART:
    print("Creating lists of files that have cover\n")
    for i in range(0,len(Arq)):
        if i+1 % 100==0:
           print("Checking art",i+1)
        # Intilializes   
        Artobj_count = 0
        wid = 0
        hei = 0
        if Count[i]>1 and exists(Arq[i]):
           m = Pos[i]
           track = tracks.Item(m)
           # If mode override on, do for all tracks in the list 
           Artobj = track.Artwork
           Artobj_count = Artobj.Count
           if Artobj_count>0:
              dic = Img_dims(Arq[i]) 
              if dic['ok']:
                 wid = dic['wid']
                 hei = dic['hei']

        # Populates the whole lists
        Covers.append(Artobj_count)
        Wid.append(wid)
        Hei.append(hei)

    # ADD COVERS TO DF 
    df["Covers"] = Covers
    df["Covers"] = df["Covers"].astype(int)        

    # CREATES SCORES LIST
    Score = []
    for i in range(0,len(Arq)):
        score_aux = 0
        if Count[i]>1 and exists(Arq[i]):
           Alb_not_blk = AA[i] != '' and Album[i] != ''
           Alb_by_art_aux = Tags.Alb_by_art(Art[i],AA[i],Title[i])
           Has_cover = Covers[i]>0
           Nice_cover_aux = Tags.Nice_cover(Album[i],Genre[i])
           # Stdz.Is_DMP3(Arq[i])
           Prev_cover = Len[i]=='0:05' 
           Dim_not_Big = Wid[i]<=650 and Hei[i]<=650
           Dim600 = Wid[i]>=598 and Hei[i]>=598 and Dim_not_Big
           Dim500 = Wid[i]>=500 and Hei[i]>=500 and Dim_not_Big
           Dim450 = Wid[i]>=450 and Hei[i]>=450 and Dim_not_Big
           Dim400 = Wid[i]>=400 and Hei[i]>=400 and Dim_not_Big
           Is_Now = Album[i].lower().find("now that's what")>-1
           if Album[i][0:4].isnumeric():
              Is_novela = 1960<= int(Album[i][0:4]) <=2010
           else:
              Is_novela = False   
           Ratio = min(Wid[i],Hei[i])/(max(Wid[i],Hei[i])+0.1)>=.96
           Priority = [Alb_not_blk, Alb_by_art_aux, Has_cover, Nice_cover_aux, Is_novela, Is_Now, Ratio, Dim600, Prev_cover, Dim500, Dim450, Dim400]
           score_aux = 0.0
           for i in range(0,len(Priority)):
               power = len(Priority)-i-1
               score_aux = score_aux + (10**power)*Priority[i]
        
        Score.append(score_aux)

    # ADDS COL. TO DF
    df['Score'] = Score
    # MAX SCORE PER TRACK
    df['max_Score'] = df.groupby('track_stdz')['Score'].transform("max")
    # CREATES LIST 
    max_Score = [x for x in df['max_Score']]

    # POPULATES ALBUMS WHOSE SCORE IS MAX
    df.loc[(df['Score']==df['max_Score']) & (df['AA'] != '') & (df['Album'] != ''), 'AA_Album'] = df['AA_Album_aux']
    df.AA_Album = df.AA_Album.fillna("")

    # PICK ONLY ONE OUT OF THE FILES WHOSE SCORE IS MAX (THIS ALBUM WILL SHOW IN ALL LINES)
    df['max_AA_Album'] = df.groupby('track_stdz')['AA_Album'].transform('max')
    
    # SET THE ALBUM TO AN ALBUM WITH MAX SCORE, IF ITS SCORE IS LESS THAN THE MAX
    df.loc[df['Score'] != df['max_Score'], 'pick_AA_Album'] = df['max_AA_Album']
    df.pick_AA_Album = df.pick_AA_Album.fillna("")
    #df.loc[df['Covers']>0, 'pick_AA_Album'] = ""

    # TRACK WITH THE BEST COVER
    df.loc[(df['Score']==df['max_Score']) & (df['AA'] != '') & (df['Album'] != ''), 'max_Score_tracks'] = df['Pos']
    df.max_Score_tracks = df.max_Score_tracks.fillna(0)
    # PICK ONLY ONE OUT OF THE FILES WHOSE SCORE IS MAX (THIS ALBUM WILL SHOW IN ALL LINES)
    df['max_Score_track'] = df.groupby('track_stdz')['max_Score_tracks'].transform('max')

    # TEST LIST CREATION (list comprehension) 
    pick_AA_Album = [x for x in df['pick_AA_Album']]
    # TRACK WITH THE BEST COVER
    max_Score_track = [x for x in df['max_Score_track']]
    
    # CHANGES TAGS AND/OR DELETES ARTWORK THAT DOESN'T HAVE THE BEST SCORE
    print("Changing album tags and/or deleting art\n")
    for i in range(0,len(Arq)):
        # THE ALBUMS BELOW NEED TO MATCH EXACTLY OR THE COVER WON'T BE TRANSFERABLE
        # DO NOT USE STDZ
        Albs_eq = (AA[i] +"@"+ Album[i]).strip() == pick_AA_Album[i].strip()
        if Count[i]>1 and Tags.Is_DMP3(Arq[i]) and not Albs_eq and exists(Arq[i]):
           Alb_not_blk = AA[i] != '' and Album[i] != ''
           # CHANGES TAGS/DELETE ART
           if Score[i] != max_Score[i] and Alb_not_blk and not Tags.Nice_cover(Album[i],Genre[i]) and not Tags.Is_live(Genre[i]):
              m = Pos[i]
              track = tracks.Item(m)
              # DELETES ART
              Cur_cover_file = Save_cover_iTu(track,VA_transf_dir)
              if exists(Cur_cover_file):
                 # add track to PL 
                 Read_PL.Add_file_to_PL(playlists,PL_del_cover,Arq[i]) 
                 itu_Cover = track.Artwork.Item(1) 
                 itu_Cover.Delete()
                 Artobj_count = 0
              # CHANGES TAGS
              pos = max_Score_track[i] 
              # SAVES NEW COVER FOR COMPARISON
              New_cover_file = Save_cover_iTu(tracks.Item(pos),VA_transf_dir,tag="new")

              AA[i] = ""
              Album[i] = ""
              if not exists(Cur_cover_file):
                 # add track to PL
                 Read_PL.Add_file_to_PL(playlists,PL_del_AA_tags,Arq[i])
              track.AlbumArtist = ""
              track.Album = ""
    
    # UPDATE COLS. THAT CHANGED
    df['AA'] = AA
    df['Album'] = Album

    ############################################################
    # COVER LOGIC
    print("") # A conta abaixo esta errada!
    print("\nAlbums to fix",len(pick_AA_Album)-pick_AA_Album.count(""),"\n")

    # CREATES LIST OF TRACKS WHOSE YEAR IS NOT THE MIN YEAR
    fix_AA = []
    for i in range(0,len(Arq)):
        Albs_eq = (AA[i] +"@"+ Album[i]).strip() == pick_AA_Album[i].strip()
        if Score[i] != max_Score[i] and Tags.Is_DMP3(Arq[i]) and not Albs_eq and not Tags.Is_live(Genre[i]):
           if exists(Arq[i]): 
              m = Pos[i]
              track = tracks.Item(m)
              AA_Album_l = pick_AA_Album[i].split("@")
              if len(AA_Album_l)==2:
                  AA_aux = AA_Album_l[0]
                  Album_aux = AA_Album_l[1]
                  print("Needs AA/Album updated:",Arq[i])
                  # add track to PL 
                  Read_PL.Add_file_to_PL(playlists,PL_transf_albs,Arq[i]) 
                  Artobj_count = track.Artwork.Count
                  if Artobj_count==0:
                     track.AlbumArtist = AA_aux
                     track.Album = Album_aux
                  fix_AA.append(i)

    print("\nAlbums fixed",len(fix_AA),"\n")

    ############################################################

#CALLS FUNC   
Transfer(PL=12)