# WILL TRY TO SEARCH ARTWORK FOR ALBUMS ON THE APPLE MUSIC STORE
# THIS WAS THE METHOD THAT WORKED PREVIOUSLY TO DOWNLOAD ARTWORK
# FIRST ADD TRACKS TO PLAYLIST

import itunespy
import requests
import Read_PL

def Call_art(PL_name="",PL=None):
    # CHECKS PL NAME
    if PL_name != "":
       dict = Read_PL.Get_PL_no(PL_name)
       if dict["res"]:
          PL = dict["PL_nbr"]
    # CALLS FUNCTION
    col_names =  ["Arq","Art","Title","AA"]
    dic = Read_PL.Read_PL(col_names,PL_nbr=PL)
    #dic = Read_PL.Read_PL(col_names,PL_nbr=37)
    playlists = dic['PLs']
    PL_name = dic['PL_Name']
    PL_nbr = dic['PL_nbr']
    tracks = dic['tracks']
    numtracks = tracks.Count
    df = dic['DF']

    # TEST LIST CREATION (list comprehension) 
    Pos = [x for x in df['Pos']]
    Arq = [x for x in df['Arq']]
    #Art = [x for x in df['Art']]
    #Title = [x for x in df['Title']]
    #AA = [x for x in df['AA']]
    nbr_files = len(Arq)
    #Album = [x for x in df['Album']]
    #Genre = [x for x in df['Genre']]

    # CHAMA A FUNCAO QUE CRIA A PL
    # CRIA PLAYLIST APENAS SE HOUVER ARQUIVOS 

    # Search for an album by name and artist
    results = itunespy.search_album("Abbey Road","The Beatles")

    # Retrieve the URL for the 600x600 album cover image
    cover_url = results[0].artwork_url_600

    # Download the cover image
    response = requests.get(cover_url)
    if response.status_code == 200:
       print("Valid response")
       # Save the image to a file
       with open("D:\\iTunes\\AbbeyRoad.jpg", "wb") as f:
            f.write(response.content)
    else:
        print("Invalid response")

    # REASSIGNS PLAYLIST
    List = []
    for i in range(nbr_files):
        read_PL = playlists.Item(PL_nbr)
        tracks = read_PL.Tracks
        m = Pos[i]
        track = tracks.Item(m)
        url = track.ArtworkUrl
        List.append(url)
        #file_exists = exists(Arq[i])
        # Stdz.Is_DMP3(Arq[i]) and 
        # if file_exists:
        #    Alb_by_art_vl = Stdz.Alb_by_art(Art[i],AA[i],Title[i])
        #    if (i+1) % 100==0:
        #       print("Adding file:",i+1,"of",len(Arq),":",Arq[i])
        #    if Alb_by_art_vl:
        #       Create_PL.Add_file_to_PL(playlists,Created_PL_name,Arq[i])

# CALLS FUNC
Call_art(PL_name="Playlist 4")