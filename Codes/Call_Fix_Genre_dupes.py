# FIXES DUPE ENTRIES IN THE GENRE TAG
# FOR EXAMPLE, IF GENRE=Rap/Rap -> GENRE=Rap

from os import rename
from os.path import exists
#import Move
import Read_PL
import Tags
import Files

def Count(Genre):
    lst = Genre.split("\\")
    new_lst = [x for x in lst if x.strip() != ""]
    count = len(new_lst)
    return count

def Fix_genre(PL_name=None,PL_nbr=None,Do_lib=False):
    # CALLS FUNCTION
    col_names =  ["Arq","Genre","ID"]
    dict = Read_PL.Read_PL(col_names,PL_name=PL_name,PL_nbr=PL_nbr,Do_lib=Do_lib)
    App = dict['App']
    playlists = dict['PLs']
    df = dict['DF']

    # TEST LIST CREATION (list comprehension) 
    Arq = [x for x in df['Arq']]
    Genre = [x for x in df['Genre']]
    ID = [x for x in df['ID']]
    nbr_files = len(Arq)

    # CHAMA A FUNCAO QUE CRIA A PL
    # CRIA PLAYLIST APENAS SE HOUVER ARQUIVOS 
    Created_PL_name = "Fix_Genre"
    if len(Arq)>0:
        Move_PL = Read_PL.Cria_PL(Created_PL_name,recria="n")

    # BREAK LINE
    print()

    cnt = 0
    for i in range(nbr_files):
        m = ID[i]
        track = App.GetITObjectByID(*m)
        file_exists = exists(Arq[i])
        if Files.Is_DMP3(Arq[i]) and file_exists and Arq[i]==track.Location:
           init_count = Count(Genre[i])
           print("Checking file:",i+1,"of",nbr_files,":",Files.file_wo_ext(Arq[i])," -- GENRE:",Genre[i])
           New_Genre = Tags.Add_to_tag(track,"",Tag="Genre")
           # THE LOGIC HERE IS THAT IF THE GENRE CHANGES, THEN A DUPE WORD WAS REMOVED
           # SINCE ONLY A BLANK WAS BEING ADDED TO THE GENRE
           # WE STILL CHECK THE COUNTS, BECAUSE MAYBE JUST A "/" WAS ADDED (OR THE ODER CHANGED)
           if New_Genre != "":
              fin_count = Count(New_Genre)
              if init_count>fin_count:
                 cnt = cnt+1
                 Read_PL.Add_track_to_PL(playlists,Created_PL_name,track) 
    # THE END
    print("\nAdded",cnt,"files to the playlist\n")           

# CALLS FUNC
Fix_genre(PL_name="Playlist 3")