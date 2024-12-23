# MOVES FILES TO A TEMPORARY FOLDER (D:\MP3\Z_temp\)
# 1o ADICIONA TRACKS NA PLAYLIST
# ESSE MODULO TB CORRIGE O CASE DOS FILENAMES

from os import rename
from os.path import exists
import Read_PL
import Tags

def Call_move(PL=None):

    # CALLS FUNCTION
    col_names =  ["Pos","Arq","Art","Genre"]
    dic = Read_PL.Read_PL(col_names,PL_nbr=PL)
    #dic = Read_PL.Read_PL(col_names,PL_nbr=37)
    playlists = dic['PLs']
    tracks = dic['tracks']
    result = dic['PL_nbr']
    df = dic['DF']
    numtracks = tracks.Count

    # TEST LIST CREATION (list comprehension) 
    Pos = [x for x in df['Pos']]
    Arq = [x for x in df['Arq']]
    Art = [x for x in df['Art']]
    #Title = [x for x in df['Title']]
    Genre = [x for x in df['Genre']]

    # CHAMA A FUNCAO QUE CRIA A PL
    # CRIA PLAYLIST APENAS SE HOUVER ARQUIVOS 
    PL_name = "Moved"
    Move_PL = Read_PL.Cria_PL(PL_name,recria="y")

    # REASSIGNS PLAYLIST
    read_PL = playlists.Item(result)
    playlistName = read_PL.Name
    print("Doublecheck playlist:",read_PL.Name,"\n")
    # BLOCO QUE SCANEIA A PL
    tracks = read_PL.Tracks

    To_fix_list = []
    # SUBDIR NEEDS TO END WITH \\
    subdir = "D:\\ZZZ2\\"
    for i in range(0,len(Arq)):
        if exists(Arq[i]) and Arq[i].lower().rfind("d:\\mp3")>=0 and Arq[i].lower().rfind(subdir.lower())==-1:
            #New_location = Move.Move(Arq[i],Art[i],Genre[i])
            #subdir = Stdz.Folder(Arq[i])
            # OS ARQUIVOS SERAO MOVIDOS PARA A PASTA ABAIXO
            tag_no_sp_chars_ext = Tags.file_w_ext(Arq[i])
            New_location = Tags.finds_valid_file(subdir,tag_no_sp_chars_ext)
            m = Pos[i]
            track = tracks.Item(m)
            if Arq[i]==track.Location:
               print(i+1,"Moving/renaming file:",Arq[i],"->",New_location,"\n")
               rename(Arq[i], New_location)
               track.Location = New_location
               Read_PL.Add_file_to_PL(playlists,PL_name,New_location)

    #print("\n")
    #print("Files moved:",len(To_fix_list),"\n")

# CALLS FUNC
Call_move()