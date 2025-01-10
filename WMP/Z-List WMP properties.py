# UPCASES THE NAMES OF THE FILES IN WMP
# SO THAT THEY ARE NOT MISSED WHEN SEARCHED FROM AN ITUNES PL

from os.path import exists
#import Read_PL
import WMP_Read_PL as WMP
import pandas as pd
import Proper
import Files
from datetime import datetime

col_names =  ["Arq"]


# MAIN CODE
# SRCH_MISS IS USED FOR DEAD TRACKS (NEEDS TO SCAN WHOLE LIBRARY TO BE ABLE TO DELETE TRACKS)
def Lists(PL_name=None,PL_nbr=None,Do_lib=False,rows=None):
    # WMP
    # CALLS Read_PL FUNCTION 
    #print("\nReading the WMP playlist")
    dict = WMP.Read_WMP_PL(col_names,PL_name=PL_name,PL_nbr=PL_nbr,Do_lib=Do_lib,rows=rows,Modify_cols=False) 
    
    # WMP ASSIGNING
    df = dict["DF"]
    # USED IF INPUT IS THE WHOLE LIBRARY
    WMP_lib = dict["Lib"]
    # USED IF INPUT IS A PLAYLIST (BASED ON iTunes)
    WMP_player = dict["WMP"]
    Read_PL = dict["PL"]

    # POPULATES LISTS
    Arq = [x for x in df["Arq"]]
    Pos = [x for x in df["Pos"]]
    nbr_files = len(Arq)

    print("\nThe WMP library df has",df.shape[0],"tracks")

    res = {}
    res["Attrib"] = []
    res["Value"] = []
    res["ReadOnly"] = []
    if Do_lib:
       track = WMP_lib.Item(0)
       # track2 = WMP_lib[Pos[0]]
    else:
        track = Read_PL.Item(0)
    
    # READS FOR LIBRARY
    for i in range(track.attributeCount):
        k = track.getAttributeName(i)
        print("Attrib:",k,"Value:",track.getItemInfo(k),"ReadOnly",track.isReadOnlyItem(k))
        res["Attrib"].append(k)
        res["Value"].append(track.getItemInfo(k))
        res["ReadOnly"].append(track.isReadOnlyItem(k))

    # TRANSPOSES INFO FOR A PL
    # for i in range(track.attributeCount):
    #     k = track.getAttributeName(i)
    #     print("Attrib:",k,"Value:",track.getItemInfo(k),"ReadOnly",track.isReadOnlyItem(k))
    #     res["Attrib"].append(k)
    #     res["Value"].append(track.getItemInfo(k))
    #     res["ReadOnly"].append(track.isReadOnlyItem(k))

    # Convert the list to a DataFrame
    df_res = pd.DataFrame(res)
    
    # save the dataframe to an Excel file
    df_res.to_excel("D:\\iTunes\\Excel\\WMP_Properties2.xlsx", index=False)
    # print("Hello, " + file_nm + "!")

# CALLS PROGRAM 
Lists(PL_name="Favorites-Easy",Do_lib=0, rows=10)