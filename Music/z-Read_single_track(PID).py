# SAVES THE TRACKS FROM A PLAYLIST OR THE WHOLE LIBRARY INTO AN EXCEL FILE
# MORE THAN ONE PLAYLIST CAN BE SELECTED
# WHEN CREATING AN EXCEL OUTPUT FOR THE LIBRARY, A NUMBER OF TRACKS CAN BE SPECIFIED.
# IF NOT SPECIFIED, IT'S ALL THE TRACKS.
from os.path import exists
import pandas as pd
import struct
import binascii
import Read_PL

# PID = App.GetITObjectPersistentIDs(track)
        # SEARCH THE NEW COVER ON THE APPLE SITE
# track = App.ItemByPersistentID(PID)

# MAIN CODE
def Read_track(PL_name=None,PL_nbr=None,Do_lib=False,rows=None,iTunes=True,col_names = ["Arq","Art","Title"]):
    # EXCLUDE INVALID TAGS 
    col_names = [x for x in col_names if x in Read_PL.order_list_itunes]
    dict = Read_PL.Read_PL(col_names,PL_name=PL_name,PL_nbr=PL_nbr,Do_lib=Do_lib,rows=rows)

    # ASSIGNS
    App = dict["App"]
    Sources = dict["Sources"]
    Lib = dict["Lib"]
    PLs = dict["PLs"]
    df = dict["DF"]

    Arq = [x for x in df['Arq']]
    ID = [x for x in df['ID']]

    m = ID[0]
    track = App.GetITObjectByID(*m)

    for key in Read_PL.iTu_tag_dict.keys():
        value = Read_PL.Get_track_attrib(track, key, Len_type="char")
        print("Key:",key,"--Is Tag:",Read_PL.iTu_tag_dict[key],"--Value:",value)
    
    PID = App.GetITObjectPersistentIDs(track)
    print()

    hex = "AE533B6A86544EC5"
    tupla = struct.unpack('!ii', binascii.a2b_hex(hex))

    track3 = App.LibraryPlaylist.Tracks.ItemByPersistentID(-1370277014, -2041295163)
    # track2 = Lib.ItemByPersistentID(-1370277014, -2041295163)
    for key in Read_PL.iTu_tag_dict.keys():
        value = Read_PL.Get_track_attrib(track3, key, Len_type="char")
        print("Key:",key,"--Is Tag:",Read_PL.iTu_tag_dict[key],"--Value:",value)


# CHAMA PROGRAM PL_name="ALL",Fave-iPhone ["Arq","Art","Title","Len"]
Read_track(PL_name="BBB",Do_lib=0,rows=None,iTunes=1,col_names = ["Arq", "Art" , "Title", "ID"])