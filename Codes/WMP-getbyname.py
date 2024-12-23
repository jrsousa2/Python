import win32com.client
import pandas as pd

# Connect to Windows Media Player
wmp = win32com.client.Dispatch("WMPlayer.OCX")

# get the playlist collection
playlists = wmp.playlistCollection.getAll()

PL = wmp.mediaCollection.getByAttribute("SourceURL", "D:\\MP3\\Favorites_Brasil\\Agnaldo Timóteo - Quem É.mp3")

PL2 = wmp.mediaCollection.getByAttribute("SourceURL", "D:\\MP3\\Favorites_Brasil\\Baby Consuelo - Todo Dia Era Dia De Índio.mp3")

# Get the media library object
#library = wmp.mediaCollection

PL = wmp.mediaCollection.getByName("XXX")

item = PL.Item(0)

PL_test = wmp.playlistCollection.getByName("XXX")
item2 = PL_test.Item(0)

print("Reading PLs...")
for i in range(len(playlists)):
    print("Pos",i,"name:",playlists[i].name)

item3 = item2
for i in range(item3.attributeCount):
    k = item3.getAttributeName(i)
    print("Attrib:",k,"Value:",item3.getItemInfo(k))

try:
    wmp.mediaCollection.remove(item, True)
except:
    print("Didn't work")    

# Get the playlist collection object
#PL_collection = wmp.playlistCollection.getAll()

# Get the playlist object by name
#PL = wmp.playlistCollection.getByname("Brasil Fave")

# Do something with the playlist, for example print its name
#print(PL.name)

# Loop through all playlists and print their names and IDs
data = []
# x = Print(PL_collection,"Favorites")
# PLs = [PL.name for PL in PL_collection]
# PL = Find(PL_collection,"Favorites")
#PL = PL_collection[5]
#PL = PL_collection[0]
#for PL in PL_collection:
PL_name = PL.name
nbr_files = PL.count
# LOOPS THRY ITEMS IN PL
for i in range(nbr_files):
    track = PL.Item(i)
    Art = track.getItemInfo("Artist")
    Arq = track.sourceURL
    list = [PL_name,i,Arq]
    if (i+1) % 100==0:
        print("Row. no: ",i+1,"of",nbr_files)
    # ADD ROW TO LIST, BEFORE CREATING DF
    data.append(list)
# ORDER THE LIST OF COLUMNS TO MATCH THE ABOVE ORDER
# SO COLUMN HEADERS ALWAYS MATCH THEIR VALUES
#col_names = order_list(col_names)
col_names = ["PL","Pos","Arq"]
df = pd.DataFrame(data, columns=col_names)

    #y = playlist.getAttribute("PlaylistID")
    #print(f"Playlist Name: {playlist.name}\nPlaylist ID: {playlist.getAttribute("PlaylistID")}\n")
# SAVES DUPES TO AN EXCEL FILE
file_nm = "D:\\iTunes\\Excel\\WMP.xlsx"
#df.to_excel(file_nm, index=False)

# ADD COUNT COL. AND SELECT
group_list = ["PL","Arq"]
df.loc[:,'Count'] = df.groupby(group_list)['Pos'].transform('count')
# SELECT ONLY RELEVANT ROWS
df = df[df['Count'] > 1]

# DF INFORMATION
print("\nThe PL has:",df.shape[0],"dupe tracks")

# SORTS 
df = df.sort_values(["Count","PL","Arq"])

# Group by columns A and B and assign a unique number to each row within the group
df['N'] = df.groupby(group_list).cumcount() + 1

# TAKES THE MAX OF THE ADDED DATE
df.loc[:,'max_N'] = df.groupby(group_list)['N'].transform('max')

# REFRESHES LISTS 
Pos = [x for x in df['Pos']]
Arq = [x for x in df['Arq']]
N = [x for x in df['N']]
max_N = [x for x in df['max_N']]
nbr_files = len(Arq)

# COUNTS HOW MANY TRACKS WILL BE REMOVED
#Plays_l = [i if (Plays[i] != Max['Plays'][i]) else None for i in range(nbr_files)]
Remove_l = [i for i in range(nbr_files) if N[i]<max_N[i]]
nbr_dupes = len(Remove_l)

print("\nDupe files that may be removed:",nbr_dupes,"of",nbr_files)
print(df['Arq'].nunique(),"unique files\n")

removed = 0
for j in range(nbr_dupes):
    i = Remove_l[j]
    m = Pos[i]
    print("Checking file:",Arq[i])
    try:
        track = PL.Item(m)
    except:
        pass
    else:    
        try:
            print("Removing file:",track.sourceURL)
            PL.mediaCollection.remove(track, True)
            PL.removeItem(track)
        except:
            track.removeItem()
            pass
        else:
            removed = removed+1
            print("Removed",removed,"dupe files of",nbr_dupes,"\n")
                    
# FINAL
print("Removed:",removed,"dupes of",nbr_dupes,"files\n")
# print("Different dir:",len(Diff_dir),"\n")

# Find the track you want to delete by its file path
# Find the track you want to delete
#track = library.getByAttribute("Title", "What Time Is Love (LP Mix)")
#filepath = "D:\\MP3\\Favorites\\The KLF - What Time Is Love (LP Mix).mp3"
#track = library.getByAttribute("SourceURL", filepath)
#track = library.getByPath(filepath)

# Delete the track from the library
# if track is not None:
#     library.remove(track)
#     print("Track deleted successfully.")
# else:
#     print("Track not found in library.")
