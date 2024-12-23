# CREATED TO FIX GENRES THAT I MESSED UP
# THIS IS A ONE-OFF
import iTunesCOM
import pandas as pd
from os import rename
from os.path import exists
import Move
import Read_PL
import Tags

def Call_Updt_Genre(PL=None):

    # LOADS AN EXCEL FILE INTO A DF
    # read the 'Sheet1' tab of an Excel file named 'data.xlsx'
    Excdf = pd.read_excel("D:\\iTunes\\Excel\\Fix_Genre.xlsx", sheet_name="FINAL")

    # TEST LIST CREATION (list comprehension) 
    #Pos = [x for x in Excdf['Pos']]
    Arq = [x for x in Excdf['Location']]
    #Art = [x for x in Excdf['Art']]
    #Title = [x for x in Excdf['Title']]
    Genre = [x for x in Excdf['Genre']]
    New_Genre = [x for x in Excdf['New_Genre']]

    # CRIA PLAYLIST SEMPRE 
    PL_name = "Updt_Genre_Files"
    Updt_Genre_PL = Read_PL.Cria_PL(PL_name,recria="y")

    
    # ADDS FILES IN THE EXCEL SHEET TO THE PLAYLIST
    # TAMBEM CONSTROI A LISTA DE ARQUIVOS QUE TERAO O Genre ATUALIZADOS
    To_fix_list = []
    print("\n")
    for i in range(0,len(Arq)):
        file_exists = exists(Arq[i])
        if file_exists:
           print("Adding file",i+1,":",Arq[i])
           To_fix_list.append(i)
           # ADICIONA AQUIVO A LISTA DE Genre TAG UPPDATES
           Read_PL.Add_file_to_PL(iTunesCOM.playlists,PL_name,Arq[i])
           
    # NUMERO DE ARQUIVOS A SEREM ATUALIZADOS
    print("\nFiles to have Genre tag updated:",len(To_fix_list),"\n")

    # ASSIGNS PLAYLIST BY NAME
    New_PL = iTunesCOM.playlists.ItemByName(PL_name)
    # BLOCO QUE SCANEIA A PL
    tracks = New_PL.Tracks
    numtracks = tracks.Count
    print("Check playlist:",New_PL.Name,"tracks: ",numtracks,"\n")

    # CRIA PLAYLIST APENAS SE HOUVER ARQUIVOS PRA ATUALIZAR
    if len(To_fix_list)>0:
       PL_fix_nm = "Updt_Genre_fixed"
       Genre_PL = Read_PL.Cria_PL(PL_fix_nm,recria="y") 

    # START FIXING THE FILES HERE:
    fixed = 0 
    miss = 0
    for i in range(len(To_fix_list)):
        # THE RANGE FOR ITEMS IN A PL IS NOT 0 TO N-1, IT'S 1 TO N
        n = To_fix_list[i]+1
        track = tracks.Item(n)
        if track.Kind == 1:
           Curr_loc = track.Location
           Curr_Genre = track.Genre
           file_exists = exists(Curr_loc)
           if not file_exists:
              miss=miss+1
           if file_exists and Arq[i]==Curr_loc:
              print("Doing file",i+1,"of",len(Arq))
              # track.Genre = New_Genre[i]
              # fixed=fixed+1
              # print("Fixed Genre of",i+1,":",Curr_loc," || From",Curr_Genre,"->",New_Genre[i])
              try:
                  itu_Cover = track.Artwork.Item(1) 
                  itu_Cover.Delete()
              except:  
                  print("Cover deletion failed")
              else:
                  fixed=fixed+1    
                  Read_PL.Add_file_to_PL(iTunesCOM.playlists,PL_fix_nm,Curr_loc)

    print("\nFinal:",fixed,"Genre tags updated,",miss,"files missing","\n")
    
# CALLS FUNC
Call_Updt_Genre()