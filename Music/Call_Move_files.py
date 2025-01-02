# MOVES FILES TO THE RIGHT FOLDER 
# ESSE MODULO TB CORRIGE O CASE DOS FILENAMES
# 1o ADICIONA TRACKS NA PLAYLIST

from os import rename
from os.path import exists
import Move
import Read_PL
import Files

Log_file = "D:\\iTunes\\Move_files_log.txt"

def Call_move(PL_name=None,PL_nbr=None,Check_dir=True,Do_lib=False):
    # CALLS FUNCTION
    col_names =  ["Arq","Art","Genre","ID"]
    dict = Read_PL.Read_PL(col_names,PL_name=PL_name,PL_nbr=PL_nbr,Do_lib=Do_lib)
    App = dict['App']
    playlists = dict['PLs']
    df = dict['DF']

    # TEST LIST CREATION (list comprehension) 
    Arq = [x for x in df['Arq']]
    Art = [x for x in df['Art']]
    Genre = [x for x in df['Genre']]
    ID = [x for x in df['ID']]

    To_fix_list = []
    miss = 0 
    print("Building list of files that will move...")
    for i in range(0,len(Arq)):
        if Check_dir:
           Fazer = Files.Is_DMP3(Arq[i])
        else:
           Fazer = True
        if Fazer:
            file_exists = exists(Arq[i])
            if file_exists:
               New_location = Move.Move(Arq[i],Art[i],Genre[i])
               # Note que aqui a comparacao eh case-sensitive
               if New_location != Arq[i]:
                  To_fix_list.append(i)
                  # print(i+1,Arq[i],"->",New_location)
            else:
                miss=miss+1      

    print("\nFiles to be moved:",len(To_fix_list),", missing",miss,"\n")

    # CHAMA A FUNCAO QUE CRIA A PL
    # CRIA PLAYLIST APENAS SE HOUVER ARQUIVOS 
    if len(To_fix_list)>0:
       Move_PL = Read_PL.Cria_PL("Moved",recria="y")

    Files.Print_to_file(Log_file,"\n\nTIME: {}\n\n", Files.track_time())
    fixed = 0 
    files_to_move = len(To_fix_list)
    for i in range(files_to_move):
        n = To_fix_list[i]
        #Arq_aux = track.Location
        New_location = Move.Move(Arq[n],Art[n],Genre[n])
        file_exists = exists(Arq[n])
        m = ID[n]
        track = App.GetITObjectByID(*m)
        if Check_dir:
           Fazer = Files.Is_DMP3(Arq[n])
        else:
           Fazer = True    
        if Fazer:
           if Arq[n] != New_location and file_exists and Arq[n]==track.Location:
              fixed = fixed+1
              print("Moving",fixed,"of",files_to_move,":",Arq[n],"->",New_location,"\n")
              # ADD ENTRY TO LOG FILE
              Files.Print_to_file(Log_file,"Moving/renaming file {} of {}: {}->{}\n", i+1, files_to_move, Arq[n], New_location)
              rename(Arq[n], New_location)
              track.Location = New_location
              Read_PL.Add_track_to_PL(playlists,"Moved",track)

    print("\nFinal:",fixed,"files moved,",miss,"files missing","\n")
    Files.Print_to_file(Log_file,"\nFinal: {} files moved, {} files missing\n", fixed, miss)
    
# CALLS FUNC
Call_move(PL_name="AAA2",Check_dir=False,Do_lib=1)