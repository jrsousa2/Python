import win32com.client
import pandas as pd

import sys
sys.path.insert(0, "D:\\Python\\iTunes")
from Read_PL import order_list

# ORDER OF THE COLS. IN THE DF (BUT THEY CAN BE SPECIFIED ANY WAY)
# THE BELOW IS JUST SO THE RIGHT HEADERS GO WITH THE RIGHT COLS.
order_list_wmp = ["PL_nbr","PL_name","Pos","ID","Arq","Art","Title","AA","Album","Genre","Year","Group","Bitrate","Len","Plays","Skips","Added"]

tag_dict = {
    "Art" : "Artist",
    "Title" : "Title",
    "AA" : "WM/AlbumArtist",
    "Album" : "WM/AlbumTitle", # OR Album
    "Genre" : "WM/Genre", # OR Genre
    "Year" : "WM/Year", # OR ReleaseDateYear
    "Group" : "WM/ContentGroupDescription",
    "Bitrate" : "Bitrate",
    "Plays": "UserPlayCount",
    "Added": "AcquisitionTime" #AcquisitionTimeYearMonthDay
    }


# OS OBJETOS ABAIXO SAO RECONHECIDOS POR QQ FUNCAO DESSE MODULO
# OBJECT wmp IS THE Player
def Init_wmp():
    global wmp
    global library
    global playlists

    # CHECKS IF WMP EXISTS
    try:
        wmp = win32com.client.Dispatch('WMPlayer.OCX')
        # library = wmp.mediaCollection.getAll()
        library = wmp.mediaCollection.getByAttribute("MediaType", "audio")
        # get the playlist collection
        playlists = wmp.playlistCollection.getAll()
    except:
        success = False    
    else:
        success = True

# create a dictionary to store attribute names
def WMP_tag_dict(item,cols):
    dict = {}
    # PROPERTIES
    for key in cols:
        if key in tag_dict.keys():
           dict[key] = item.getItemInfo(tag_dict[key])
    if "Plays" in cols: 
        dict["Plays"] = int(dict["Plays"]) 
    if "Skips" in cols: 
        dict["Skips"] = 0
    if "Bitrate" in cols: 
        dict["Bitrate"] = int(dict["Bitrate"])/1000   
    if "Added" in cols: 
        dict["Added"] = pd.to_datetime(dict["Added"], format="%d/%b/%Y %I:%M:%S %p")    
    if "Arq" in cols: 
        dict["Arq"] = item.sourceURL
    #if "Title" in cols: 
    #    dict["Title"] = item.name
    if "Len" in cols: 
        dict["Len"] = item.durationString
    if "ID" in cols: 
        dict["ID"] = 0    
    return dict


