# THIS CODE WAS CREATED TO TRY TO FIGURE
# THE VERY CONVOLUTED WAY THAT FILES ARE SORTED IN AN ITUNES PL

from os import rename
from os.path import exists
import Read_PL
import Tags

def Call_order(PL=None):

    # CALLS FUNCTION
    col_names =  ["Pos","Arq","Art","Title","Genre"]
    dic = Read_PL.Read_PL(col_names,PL_nbr=PL)
    #dic = Read_PL.Read_PL(col_names,PL_nbr=37)
    playlists = dic['PLs']
    tracks = dic['tracks']
    result = dic['PL_nbr']
    df = dic['DF']
    PL_name = dic['PL_Name']
    numtracks = tracks.Count

    # TEST LIST CREATION (list comprehension) 
    Pos = [x for x in df['Pos']]
    Arq = [x for x in df['Arq']]
    Art = [x for x in df['Art']]
    Title = [x for x in df['Title']]
    #Genre = [x for x in df['Genre']]

    # CHAMA A FUNCAO QUE CRIA A PL
    # CRIA PLAYLIST APENAS SE HOUVER ARQUIVOS 
    Created_PL_name = "Checa_Ordem"
    if len(Arq)>0:
        Move_PL = Read_PL.Cria_PL(Created_PL_name,recria="y")

    # REASSIGNS PLAYLIST
    for i in range(0,len(Arq)):
        file_exists = exists(Arq[i])
        if not Tags.Is_DMP3(Arq[i]) or not file_exists:
           x = 1 
        if Tags.Is_DMP3(Arq[i]) and file_exists:
           if (i+1) % 100==0:
              print("Adding file:",i+1,"of",len(Arq),":",Arq[i])
           Read_PL.Add_file_to_PL(playlists,Created_PL_name,Arq[i])
# CALLS FUNC
Call_order()