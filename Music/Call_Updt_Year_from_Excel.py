# THIS IS OUT OF DATE (USED TO TAKE YEAR FROM CHATGPT)
# UPDATES THE YEAR TAG OF TRACKS FROM AN EXCEL FILE
# IT DOESN'T NEED AN INITIAL PLAYLIST, IT CREATES THE PLAYLIST FIRST
# FIRST ADDS TRACKS TO PLAYLIST


# THIS IS A SUBROUTINE CALLED BY MOST CODES
# iTunes MS COM (component object model) (NOT THE SAME AS API)
import win32com.client
#import pandas as pd
#from os.path import exists
import pandas as pd
from os import rename
from os.path import exists
import Move
import Read_PL
import Tags

# OS OBJETOS ABAIXO SAO RECONHECIDOS POR QQ FUNCAO DESSE MODULO
iTunesApp = win32com.client.Dispatch("iTunes.Application.1")
Sources = iTunesApp.Sources

for i in range(1,Sources.Count+1):
        source = Sources.Item(i)
        # ESSA VARIAVEL (playlists) DEVE SER DISPONIVEL PARA TODAS AS FUNCOES
        if source.Kind == 1:
            playlists = source.Playlists

# def Add_PL(PL_name):
#     # CRIA PLAYLIST SEMPRE 
#     Updt_Year_PL = Read_PL.Create_PL(PL_name,recreate="y")
    
#     # ASSIGNS PLAYLIST BY NAME
#     New_PL = playlists.ItemByName(PL_name)
#     # BLOCO QUE SCANEIA A PL
#     tracks = New_PL.Tracks
#     numtracks = tracks.Count
#     print("Check playlist:",New_PL.Name,"tracks: ",numtracks,"\n")

#     # CRIA PLAYLIST APENAS SE HOUVER ARQUIVOS PRA ATUALIZAR
#     if nbr_updt>0:
#        PL_fix_nm = "Updt_Year_fixed"
#        Year_PL = Read_PL.Create_PL(PL_fix_nm,recreate="y") 

def Call_Updt_Year(PL=None):
    # LOADS AN EXCEL FILE INTO A DF
    # read the 'Sheet1' tab of an Excel file named 'data.xlsx'
    Excdf = pd.read_excel('D:\\iTunes\\Excel\\Fix_Year.xlsx', sheet_name='Sheet3')

    # TEST LIST CREATION (list comprehension) 
    #Pos = [x for x in Excdf['Pos']]
    Arq = [x for x in Excdf['Arq']]
    Year = [x for x in Excdf['Year']]
    New_Year = [x for x in Excdf['New_Year']]

    # CRIA PLAYLIST SEMPRE 
    PL_name = "Updt_Year_Files"
    Updt_Year_PL = Read_PL.Create_PL(PL_name,recreate="y")
    
    # ADDS FILES IN THE EXCEL SHEET TO THE PLAYLIST
    # TAMBEM CONSTROI A LISTA DE ARQUIVOS QUE TERAO O YEAR ATUALIZADOS
    To_fix_list = []
    print("\n")
    i = 0
    while (i<len(Arq)):
          file_exists = exists(Arq[i])
          comp1 = Year[i]+1 == New_Year[i]
          comp2 = New_Year[i] < Year[i]
          if file_exists and Tags.Is_DMP3(Arq[i]) and comp1:
             print("Adding file",i+1,":",Arq[i])
             Read_PL.Add_file_to_PL(playlists,PL_name,Arq[i])
             # ADICIONA AQUIVO A LISTA DE YEAR TAG UPPDATES
             To_fix_list.append(i)
             print("Year update: From",Year[i],"->",New_Year[i],"\n")
             i=i+1   
          else:
              del Arq[i]      
              del Year[i]
              del New_Year[i]

    # NUMERO DE ARQUIVOS A SEREM ATUALIZADOS
    nbr_updt = len(To_fix_list)
    print("\nFiles to have year tag updated:",nbr_updt,"\n")

    # ASSIGNS PLAYLIST BY NAME
    New_PL = playlists.ItemByName(PL_name)
    # BLOCO QUE SCANEIA A PL
    tracks = New_PL.Tracks
    numtracks = tracks.Count
    print("Check playlist:",New_PL.Name,"tracks: ",numtracks,"\n")

    # CRIA PLAYLIST APENAS SE HOUVER ARQUIVOS PRA ATUALIZAR
    if nbr_updt>0:
       PL_fix_nm = "Updt_Year_fixed"
       Year_PL = Read_PL.Create_PL(PL_fix_nm,recreate="y") 

    # START FIXING THE FILES HERE:
    fixed = 0 
    miss = 0
    for i in range(nbr_updt):
        # THE RANGE FOR ITEMS IN A PL IS NOT 0 TO N-1, IT'S 1 TO N
        n = To_fix_list[i]+1
        track = tracks.Item(n)
        if track.Kind == 1:
           Curr_loc = track.Location
           Curr_Yr = track.Year
           file_exists = exists(Curr_loc)
           if not file_exists:
              miss=miss+1
           if Tags.Is_DMP3(Curr_loc) and file_exists and Arq[i]==Curr_loc:
              if comp1:
                 print("Fixing year of",i+1,":",Curr_loc," || From",Curr_Yr,"->",New_Year[i])
                 track.Year = New_Year[i]
                 fixed=fixed+1
                 Read_PL.Add_file_to_PL(playlists,PL_fix_nm,Curr_loc)

    print("\nFinal:",fixed,"year tags updated,",miss,"files missing","\n")
    
# CALLS FUNC
Call_Updt_Year()