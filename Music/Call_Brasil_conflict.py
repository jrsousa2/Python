# CHECA ARTISTAS QUE ESTAO EM BR E INTL AO MESMO BASEADO NO GENRE
from os.path import exists
import Tags
import Cover_logic
import Read_PL

# MAIN CODE
def Brasil_conflict(PL_nbr=None):
    # CALLS FUNCTION
    col_names =  ["Pos","Arq","Art","Genre"]
    # "Title","Genre"
    dic = Read_PL.Read_PL(col_names,PL_nbr=PL_nbr)
    playlists = dic['PLs']
    tracks = dic['tracks']
    result = dic['PL']
    df = dic['DF']

    #override_art=False
    # TEST LIST CREATION (list comprehension) 
    Pos = [x for x in df['Pos']]
    Arq = [x for x in df['Arq']]
    Art = [x for x in df['Art']]
    #Title = [x for x in df['Title']]
    Genre = [x for x in df['Genre']]

    # CHANGE POS TO INTEGER
    df['Pos'] = df['Pos'].astype(int)

    # CRIA BRASIL FLAG COL. SUBDIR
    df.loc[df['Genre'].str.contains("Brasil"), 'Is_Brasil'] = True
    #df.loc[df['Genre'].str.contains("Favorite_Brasil"), 'Is_Brasil'] = True
    df.Is_Brasil = df.Is_Brasil.fillna(False)

    # CREATES COL. 
    df['Art_lc'] = df['Art'].str.lower()
    df['Dist'] = df.groupby('Art_lc')['Is_Brasil'].transform("nunique").astype(int)

    # SORTS DF
    df = df.sort_values(['Dist','Art_lc'], ascending=[False,True])

    # CRIA DISTINCT LISTA
    Dist = [x for x in df['Dist']]
    # RECREATES ALL LISTS
    Pos = [x for x in df['Pos']]
    Arq = [x for x in df['Arq']]
    Art = [x for x in df['Art']]
    Is_Brasil = [x for x in df['Is_Brasil']]

    # MESSAGE
    print("Number of artists in both location:",Dist.count(2),"\n")

    # 2o SYNC THE TAGS and key !='Cover'
    PL_BR = "B_in_Brasil"
    PL_not_BR = "B_not_in_Brasil"
    Pop = Read_PL.Cria_PL(PL_BR,recria="Y")
    Pop = Read_PL.Cria_PL(PL_not_BR,recria="Y")

    for i in range(0,len(Dist)):
        if Dist[i]==2 and exists(Arq[i]) and Tags.Is_DMP3(Arq[i]):
           if Is_Brasil[i]:
              Read_PL.Add_file_to_PL(playlists,PL_BR,Arq[i])  
           else:
               Read_PL.Add_file_to_PL(playlists,PL_not_BR,Arq[i])  

# CHAMA PROGRAM
Brasil_conflict(PL_nbr=12)