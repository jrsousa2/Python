# iTunes API
import win32com.client
import pandas as pd
import Cria_PL

# CRIA UMA PLAYLIST
New_PL = Cria_PL.Cria_PL("Move_files")

New_PL.AddFile("D:\MP3\Favorites\2 Brothers On The 4Th Floor - Can't Help Myself.mp3")


New_PL = None