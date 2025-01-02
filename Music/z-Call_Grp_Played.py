# IDENTIFIES WHICH TRACKS HAVE PLAYED IN THE GROUPING BUT NO PLAYS
# SETS PLAYS=1 FOR THOSE
# THIS IS NOT NEEDED ANYMORE, SINCE I CAN SYNC THE TAGS (WMP VS ITUNES)

from os import rename
from os.path import exists
import Move
import Read_PL
import Tags

Log_file = "D:\\iTunes\\Move_files_log.txt"

def Call_plays(PL_name=None,PL_nbr=None):
    if PL_name != "":
       dict = Read_PL.Get_PL_no(PL_name)
       if dict["res"]:
          PL_nbr = dict["PL_nbr"]
    # CALLS FUNCTION
    col_names =  ["Arq","Plays","Group"]
    dict = Read_PL.Read_PL(col_names,PL_nbr=PL_nbr)
    playlists = dict['PLs']
    tracks = dict['tracks']
    df = dict['DF']

    # TEST LIST CREATION (list comprehension) 
    PL_list = [x for x in df['PL']]
    Pos = [x for x in df['Pos']]
    Arq = [x for x in df['Arq']]
    Plays = [x for x in df['Plays']]
    Group = [x for x in df['Group']]
    nbr_files = len(Arq)

    #nbr_files_to_updt = count_list.count(True)
    do_list = [i for i in range(nbr_files) if Plays[i]==0 and Group[i].find("Played")>=0]
    nbr_files_to_updt = len(do_list)

    print("\nFiles to be updated:",nbr_files_to_updt,"\n")

    # CHAMA A FUNCAO QUE CRIA A PL
    # CRIA PLAYLIST APENAS SE HOUVER ARQUIVOS 
    if nbr_files_to_updt>0:
       Out_PL_nm = "Plays"
       Move_PL = Read_PL.Cria_PL(Out_PL_nm,recria="y")

    #Stdz.Print_to_file(Log_file,"\n\nTIME: {}\n\n", Stdz.track_time())
    fixed = 0 
    miss = 0
    for j in range(nbr_files_to_updt):
        i = do_list[j]
        file_exists = exists(Arq[i])
        if not file_exists:
           miss = miss+1
        read_PL = playlists.ItemByName(PL_list[i])
        tracks = read_PL.Tracks
        m = Pos[i]
        track = tracks.Item(m)
        if file_exists and Arq[i]==track.Location:
           fixed = fixed+1
           print(fixed,") Updating file:",j+1,"of",nbr_files_to_updt,":",Arq[i])
           track.PlayedCount = 1
           Read_PL.Add_track_to_PL(playlists,Out_PL_nm,track)

    print("\nFinal:",fixed,"tags updated,",miss,"files missing","\n")
    #Stdz.Print_to_file(Log_file,"\nFinal: {} files moved, {} files missing\n", fixed, miss)
    
# CALLS FUNC
Call_plays(PL_name="AAA")