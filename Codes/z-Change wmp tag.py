# THIS IS WORKING
import win32com.client
import WMP_Read_PL as WMP

#track_wmp.getItemInfoByType("WM/Genre","",0)

wmp = win32com.client.Dispatch('WMPlayer.OCX')
library = wmp.mediaCollection.getAll()
PLs = wmp.playlistCollection.getAll()

col_names =  ["Art","Title","AA","Album","Genre","Year"]

# BELOW WORKS
# paths = [library[x].sourceURL for x in range(len(library))]

# Path = track_wmp.sourceURL

source = "D:\MP3\Favorites\ABBA - The Winner Takes It All.mp3"
# source = source.replace("\\","\\\\")
# Find the track by source URL
PL = wmp.mediaCollection.getByAttribute("SourceURL", source)
track_wmp = PL.Item(0)

track_wmp2 = library[608]

# MediaCollection.getMediaAtom

dict1 = WMP.tag_dict_wmp(track_wmp,col_names)

# track_wmp = library.getByAttribute("SourceURL", source)
print("Year",track_wmp.getItemInfo("ReleaseDateYear"))
print("Genre",track_wmp.getItemInfo("Genre"))

item = track_wmp
for i in range(item.attributeCount):
    k = item.getAttributeName(i)
    print("Attrib:",k,"Value:",item.getItemInfo(k))

tag = "WM/Year"
tag = "ReleaseDateYear"
value = track_wmp.getItemInfo(tag)
print("Before tag:", value)

# track_wmp.setItemInfo("WM/Genre", "Brasil\\Novela\\")
track_wmp.setItemInfo(tag, "1980")

value = track_wmp.getItemInfo(tag)
print("After tag:", value)

# Clean up and release resources
wmp.close()

