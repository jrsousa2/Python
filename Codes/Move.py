# SUBROUTINE CALLED BY OTHER CODES
# MOVE MP3 FILES TO THEIR PROPER FOLDER BASED ON THE TAGS
from os.path import exists
from re import sub #For regular expressions
import Proper
import Tags
import Files

# FINDS THE FIRST VALID LETTER IN AN ARTIST
def Acha_letra(Str):

    Str=Str.lower()
    Str=Str.strip()
    trans1 = Str.maketrans("ßçñÿùúûü", "bcnyuuuu")
    trans2 = Str.maketrans("àáâãäåæ", "aaaaaaa")
    trans3 = Str.maketrans("èéêëíîï", "eeeeiii")
    trans4 = Str.maketrans("ðòóôõöø", "ooooooo")
    trans = {**trans1, **trans2, **trans3, **trans4}
    Str = Str.translate(trans)

    Dir_Letra = ""
    Achou=False
    words = Str.split()
    i=0
    while (i<len(words) and not Achou):
        word = words[i].strip()
        word = word.lower()
        for j in range (0,len(word)):
            if not Achou and "a"<= word[j] <="z" and \
               word not in ("a","o","as","os","the","dj","feat","feat.","ft."):
               Dir_Letra = word[j].upper()
               Achou = True
        i=i+1

    if not ("A"<=Dir_Letra<="Z"):
        Dir_Letra = ""
    return Dir_Letra    

# FUNCAO QUE MOVE UM ARQUIVO
def Move(Location,Art,Genre):
    #pos = Location.rfind("\\")+1
    #subdir = Location[0:pos].upper()
    #subdir = Stdz.Folder_proper(subdir)
    subdir = Files.Folder(Location)
    subdir = Files.Folder_proper(subdir)
    file = Files.file_w_ext(Location)
    #file = Location[pos:]

    # RIGHT FOLDER
    if Tags.Is_Brasil(Genre):
       Right_folder = "Brasil"
       Fave_folder = "Favorites_Brasil"
    else:
        Right_folder = "Intl"
        Fave_folder = "Favorites"
    
    # ACTUAL FOLDER
    if "brasil" in subdir.lower():
        Actual_folder = "Brasil"
    else:
        Actual_folder = "Intl" 

    # IS FAVE?
    if "favorite" in Genre.lower():
        Is_fave = True
    else:
        Is_fave = False

    # IN FAVE FOLDER?
    if Fave_folder.lower() in subdir.lower():
       In_fave = True
    else:
       In_fave = False

    # LETRA EM QUE ESTA ATUALMENTE
    pos = subdir.rfind("\\")-1
    if pos>=0:
       Actual_Dir_Letra = subdir[pos].upper()
    else:
        Actual_Dir_Letra = ""

    if "\\"+Actual_Dir_Letra.lower()+"\\" not in subdir.lower():
        Actual_Dir_Letra=""

    #file_letra = file[0].upper()
    # 1a LETRA VALIDA DO ArtA */
    Target_Dir_Letra = Acha_letra(Art)

    # EXCEPTIONS
    if Art.lower()=="the the":
       Target_Dir_Letra = "T"
    
    Dir_is_right = False
    if not Is_fave and In_fave and Right_folder=="Brasil": # Not Fave but Fave folder */
       Dest_Dir = "D:\\MP3\\Brasil\\" + Target_Dir_Letra
    elif not Is_fave and In_fave and Right_folder=="Intl":
        Dest_Dir = "D:\\MP3\\" + Target_Dir_Letra
    elif Is_fave and not In_fave and Right_folder=="Brasil": # Fave but not Fave folder */
        Dest_Dir = "D:\\MP3\\Favorites_Brasil"
    elif Is_fave and not In_fave and Right_folder=="Intl":
        Dest_Dir = "D:\\MP3\\Favorites"
    elif not Is_fave and Right_folder=="Brasil" and Right_folder != Actual_folder:
        Dest_Dir = "D:\\MP3\\Brasil\\" + Target_Dir_Letra
    elif not Is_fave and Right_folder=="Brasil" and Target_Dir_Letra != Actual_Dir_Letra:
        Dest_Dir = "D:\\MP3\\Brasil\\" + Target_Dir_Letra
    elif not Is_fave and Right_folder=="Intl" and Right_folder != Actual_folder:
        Dest_Dir = "D:\\MP3\\" + Target_Dir_Letra
    elif not Is_fave and Right_folder=="Intl" and Target_Dir_Letra != Actual_Dir_Letra:
        Dest_Dir = "D:\\MP3\\" + Target_Dir_Letra
    else:
        Dest_Dir = subdir
        Dir_is_right = True

    # Adiciona backslash
    if not Dir_is_right:
       Dest_Dir = Dest_Dir + "\\"

    # Fazer se: diretorio mudou OU nome do arquivo mudou:

    # FINDS FILE NAME THAT DOESN'T EXIST
    # REGULAR EXPRESSION (qq numero entre parenteses) 
    # SUBSTITUI d+ POR d{1,3} (PARA NAO BATER SE FOR UM ANO DENTRO DOS PARENTESES)
    aux = sub(" \(\d{1,3}\)\.[mM][pP]3", ".mp3", file) 
    no = -1
    if aux != file:
       pos1 = file.rfind("(")
       pos2 = file.rfind(")")
       no = int(file[pos1+1:pos2])
    pos = aux.lower().rfind(".mp3")
    file_no_ext = aux[0:pos]
    file_no_ext = Proper.Proper(file_no_ext,"file")
    New_file = file_no_ext + ".mp3"
    New_location = Dest_Dir + New_file
    i=0
    # Procuro arquivo que nao exista ate achar, exceto no caso do diretorio estar correto
    # Neste ultimo caso eu paro quando o numero chegar no atual
    while exists(New_location) and (i<=no-1 or not Dir_is_right or (no==-1 and New_location.lower() != Location.lower())):
        i=i+1
        New_file = file_no_ext + " ("+ str(i) + ")"+ ".mp3"
        New_location = Dest_Dir + New_file

    # AQUI TEM QUE SER CASE-SENSITIVE JA QUE QUERO ARRUMAR O FILE NAME
    if Dir_is_right and Location==New_location:
       New_location = Location

    return New_location
