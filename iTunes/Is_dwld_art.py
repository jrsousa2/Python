# CREATES PLAYLIST WITH FILES WHOSE COVER IS ITUNES DOWNLOADED (NOT ATTACHED)
# THESE ARE USUALLY WRONG AND NEED TO BE DELETED
# WITH THIS I DON'T HAVE A NEED TO CHECK IF ART IS DOWNLOAD IN ANY CODES
# THIS RARELY NEEDS TO BE RUN
from os import rename
from os.path import exists
#import Move
import Read_PL
import Tags

def Is_dwld(PL_name=None,PL_nbr=None,Do_lib=False):
    # CALLS FUNCTION
    col_names =  ["Arq","ID"]
    dict = Read_PL.Read_PL(col_names,PL_name=PL_name,PL_nbr=PL_nbr,Do_lib=Do_lib)
    # ASSIGNS
    App = dict['App']
    playlists = dict['PLs']
    df = dict['DF']

    # TEST LIST CREATION (list comprehension) 
    Arq = [x for x in df['Arq']]
    ID = [x for x in df['ID']]
    nbr_files = len(Arq)

    # CHAMA A FUNCAO QUE CRIA A PL
    # CRIA PLAYLIST APENAS SE HOUVER ARQUIVOS 
    print()
    PL_name = "Dwld_art"
    if nbr_files>0:
       Art_PL = Read_PL.Create_PL(PL_name,recreate="y")

    # REASSIGNS PLAYLIST
    for i in range(df.shape[0]):
        print("Checking",i+1,"of",df.shape[0],"covers // file:",Arq[i])
        m = ID[i]
        track = App.GetITObjectByID(*m)
        Artobj = track.Artwork
        Art_count = Artobj.count
        Is_dwld = False
        if Art_count>0:
           try:
              Art = Artobj.Item(1)
              Is_dwld = Art.IsDownloadedArtwork
           except:
              print("Exception")   
        if Is_dwld:
           Read_PL.Add_track_to_PL(playlists,PL_name,track)

# CALLS FUNC
Is_dwld(PL_name="AAA2")
