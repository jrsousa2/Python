# O LIXO DO iTUNES FICOU LOUCO
# NAO USAR ESSE PGM PRA ANEXAR, PQ VAI SAIR ERRADO
# EMBEDS THE ARTWORK INTO THE FILE, FOR FILES THAT ALREADY HAVE DOWNLOADED ART FROM APPLE IN ITUNES
# ISSO DAQUI NAO DEVE AFETAR MUITOS ARQUIVOS, JA QUE EU NAO PROCURO MAIS AS CAPAS USANDO O ITUNES
# EU FACO ISSO DIRETAMENTE
import Read_PL
from os.path import exists
import Cover_logic
import Read_PL

#TINYTAG IMAGE DATA
#tag = TinyTag.get('/some/music.mp3', image=True)
#image_data = tag.get_image()

# Pass the filename into the
# Tinytag.get() method and store
# the result in audio variable


# MAIN CODE
def Embed_art():
    col_names =  ["Pos","Arq"]
    dict = Read_PL.Read_PL(col_names,PL_nbr=None)
    playlists = dict['PLs']
    tracks = dict['tracks']
    result = dict['PL_nbr']
    PL_Name = dict['PL_Name']
    numtracks = tracks.Count
    df = dict['DF']

    # TEST LIST CREATION (list comprehension) 
    Pos = [x for x in df['Pos']]
    Arq = [x for x in df['Arq']]
    #Art = [x for x in df['Art']]

    # TRACKS WITH COVERS PL 
    Is_dwld_PL_nm = "Is_dwld"
    Pop = Read_PL.Cria_PL(Is_dwld_PL_nm,recria="Y")

    # 2o SYNC THE TAGS and key !='Cover'
    Is_dwld_attach_PL_nm = "Is_dwld_attached"
    Pop = Read_PL.Cria_PL(Is_dwld_attach_PL_nm,recria="Y")

    # REASSIGNS PLAYLIST
    dict = Read_PL.Reassign_PL(PL_Name)
    tracks = dict['tracks']
    result = dict['PL_nbr']

    # Initializes list
    Dwld_cover = []
    Arq = []
    Pos = []
    # CHECKS IF TRACK HAS ART:
    print("Creating lists of files that will be checked:\n")
    achou = False
    tam = -1
    for m in range(1,numtracks):
        track = tracks.Item(m)
        if track.Kind == 1:
           Arq_nm = track.Location 
           tam = tam+1
           Arq.append(Arq_nm)
           Pos.append(m)
           if m % 100==0:
              print("Processing file",m,"of",numtracks)
           if exists(Arq_nm):
               # If mode override on, do for all tracks in the list 
               Artobj = track.Artwork
               Artobj_Count = Artobj.Count
               if Artobj_Count>0:
                   for c in range(1,Artobj_Count+1):
                       Art = Artobj.Item(c)
                       #desc = Art.Description
                       #IsDownlArtw_value = False
                       try:
                          IsDownlArtw_value = Art.IsDownloadedArtwork
                       except Exception:
                              print("Art error")
                       else:       
                            if IsDownlArtw_value:
                               Dwld_cover.append(tam)
                               Read_PL.Add_file_to_PL(playlists,Is_dwld_PL_nm,Arq_nm)
                               achou = True
                               break
#                       if achou:
#                          break         
#                   if achou:
#                      break   
#               if achou:
#                  break
#           if achou:
#               break
#        if achou:
#               break        

    # SAINDO DO LOOP
    print("\nFiles that have donwloaded cover:",len(Dwld_cover))
    print("")

    # REASSIGNS PLAYLIST
    # REASSIGNS PLAYLIST
    #dict = Read_PL.Reassign_PL(PL_Name)
    #tracks = dict['tracks']
    #result = dict['PL_nbr']

    # Initiliazes issue counts
    fixed = {}
    fixed['iTunes saved'] = 0
    fixed['iTunes save exc'] = 0
    fixed['Attached'] = 0
    fixed['Attach exc'] = 0
    
    # Albs is a set for albums searched
    for i in range(0,len(Dwld_cover)):
        if (i+1) % 100==0:
            print("Processing file",i+1,"of",len(Dwld_cover))
        n = Dwld_cover[i]
        m = Pos[n]
        #m = Pos[n]
        test2= Arq[n]
        if exists(Arq[n]):
            track = tracks.Item(m)
            test = track.Location
            # Saves cover to an external file
            Srch_cover_file = Cover_logic.Save_cover(tracks,m)
            if exists(Srch_cover_file):
                fixed['iTunes saved'] = fixed['iTunes saved'] + 1
                try:
                    track.AddArtworkFromFile(Srch_cover_file)
                except:
                    print("Attach exception has occurred")
                    fixed['Attach exc'] = fixed['Attached exc']+1
                else:
                    Read_PL.Add_file_to_PL(playlists,Is_dwld_attach_PL_nm,Arq[n])
                    fixed['Attached'] = fixed['Attached']+1
            else:
                fixed['iTunes save exc'] = fixed['iTunes save exc']+1        
            
    print("")
    for key in fixed:
        print("Final: ",key,"->",fixed[key])
    print("")

# CALLS THE FUNCTION
Embed_art()