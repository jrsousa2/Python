# LISTS ALL THE PROPERTIES FOR AN ITUNES TRACK

from os.path import exists
#from os import listdir 
import Read_PL
import Tags
from Files import get_Win_files


def All_props(PL_name=None,PL_nbr=None,Do_lib=False,rows=None):
    # CALLS FUNCTION
    col_names =  ["Arq", "ID"] 
    dict = Read_PL.Read_PL(col_names,PL_name=PL_name,PL_nbr=PL_nbr,Do_lib=Do_lib,rows=rows) 
    # App = dict['App']
    PLs = dict['PLs']
    df = dict['DF']
    # ASSIGNS VARS
    iTu_App = dict["App"]

    # TEST LIST CREATION (list comprehension) 
    Arq = [x.lower() for x in df["Arq"]]
    ID = [x for x in df["ID"]]

    track = iTu_App.GetITObjectByID(*ID[0])
    PID = iTu_App.GetITObjectPersistentIDs(track)
    
    # Get all attributes and methods of the 'track' object
    attributes = dir(track)
    # Loop through attributes
    for attr in attributes:
        # Filter out methods
        if not callable(getattr(track, attr)):
            # Get the value of the attribute and display it
            value = getattr(track, attr)
            print(f"{attr}: {value}")

    print("The End")
# CALLS FUNC ,rows=500
All_props(PL_name="AAA 1",Do_lib=1, rows=1)