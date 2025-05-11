# TO USE THIS CODE, CREATE 3 PLAYLISTS FIRST, AS CREATING THEM FROM SCRATCH FAILS
# COMPARES IF FILENAMES MATCH THE TAGS (SYNCS FILENAMES WITH TAGS)
from os.path import exists
import Read_PL
# import Tags
import Files

# 1o ADICIONA TRACKS NA PLAYLIST
def file_vs_tags(PL_name=None,PL_nbr=None):

    # CALLS FUNCTION
    col_names =  ["Arq"]
    dict = Read_PL.Read_PL(col_names,PL_name=PL_name,PL_nbr=PL_nbr)
    playlists = dict['PLs']
    df = dict['DF']
    
    # TEST LIST CREATION (list comprehension) 
    Arq = [x for x in df['Arq']]
    nbr_files = len(Arq)

    # PLAYLIST NAME
    PL_nm = "A_not_D_MP3"
    # CRIA PLAYLISTS 
    Diff_PL = Read_PL.Create_PL(PL_nm, recreate="y")

    # CHECKS WHICH FILES MEET THE CRITERIA
    # STATS
    print("Building lists of missing/not D:\\MP3 files")
    missing = [i for i in range(nbr_files) if not exists(Arq[i])]
    not_D_MP3 = [i for i in range(nbr_files) if exists(Arq[i]) and not Files.Is_DMP3(Arq[i])]
    nbr_files = len(not_D_MP3)

    # STATS
    print(len(missing),"missing files,",len(not_D_MP3),"not in D:\\MP3")
    
    for j in range(nbr_files):
        i = not_D_MP3[j]
        print("Adding file",j+1,"to playlist")
        if exists(Arq[i]) and not Files.Is_DMP3(Arq[i]):
           Read_PL.Add_file_to_PL(playlists,PL_nm,Arq[i])

# CALLS FUNC
file_vs_tags(PL_name="ALL",rows=4000)