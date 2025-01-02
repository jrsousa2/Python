import win32com.client
import pandas as pd

# Connect to Windows Media Player
wmp = win32com.client.Dispatch("WMPlayer.OCX")

# Get the media library object
library = wmp.mediaCollection

# get the playlist collection
PL_collection = wmp.playlistCollection

def Print(PL_collection,srch_PL):
    nbr = len(PL_collection)
    count = 0
    print("Number of PL's:",nbr)
    for PL in PL_collection:
        count = count+1
        PL_name = PL.name
        print("PL",count,"of",nbr,":",PL_name)
        if PL_name == srch_PL:
           break
    return 1

def Find(PL_collection,srch_PL):
    PLs = PL_collection.getAll()
    for PL in PL_collection.getAll():
        PL_name = PL.name
        if PL_name == srch_PL:
           break
    return PL     

# CREATE A NEW PLAYLIST
new_PL_name = "Favorites"

# Get the playlist collection object
PL_col = wmp.playlistCollection.getByname(new_PL_name)
cnt = PL_col.count
N = len(PL_col)
if N==1:
   new_PL = PL_col.Item(0)
   #new_PL_name = new_PL.name
   print("Playlist",new_PL_name,"exists, with",new_PL.count,"tracks. Will be deleted!\n")
   PL_collection.remove(new_PL)
   #new_PL.removeItem() 
elif (N>1):
   print("Error creating new playlist",new_PL_name,"\n")

# RECREATES THE PLAYLIST AFTER DELETION
try:
    # THIS ONE IS RIGHT
    new_PL = PL_collection.newPlaylist(new_PL_name)
    #test = new_PL.getItemInfo("URL")
    #PL_path = new_PL.sourceURL
except:
    print("Error creating new playlist",new_PL_name,"\n")   

# PLAYLIST TO FIND DUPES IN
read_PL_name = "Favorites-Easy"
# Get the playlist collection object
PL_col = wmp.playlistCollection.getByname(read_PL_name)
cnt = PL_col.count
N = len(PL_col)
if cnt==1:
   read_PL = PL_col.Item(0)
   cnt = read_PL.count
   nbr_files = len(read_PL)
else:
    print("Error finding playlist to read\n")   
#PL_col1 = PL_read.Item(0)

data = []
# LOOPS THRU ITEMS IN PL
for i in range(nbr_files):
    track = read_PL.Item(i)
    Art = track.getItemInfo("Artist")
    Arq = track.sourceURL
    list = [read_PL_name,i,Arq]
    if (i+1) % 100==0:
        print("Row. no: ",i+1,"of",nbr_files,"(",read_PL_name,")")
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
Keep_l = [i for i in range(nbr_files) if N[i]==max_N[i]]
Remove_l = [i for i in range(nbr_files) if N[i]<max_N[i]]
nbr_dupes = len(Remove_l)

print("\nDupe files that may be removed:",nbr_dupes,"of",nbr_files)
print(df['Arq'].nunique(),"unique files\n")

# TESTA SE EH POSSIVEL ACHAR O ITEM DUPLICADO NA LIBRARY
i = Keep_l[0]
item = library.getByAttribute("SourceURL", Arq[i])

try:
   item.removeItem()
except:
      pass

try:
   item.remove()
except:
      pass

try:
   library.remove(item)
except:
      pass

try:
   library.remove(Arq[i])
except:
      pass
#library.remove(item)

# CREATE NEW PLAYLIST
#new_PL = PL_collection.newPlaylist("New Playlist")
#new_PL = library.newPlaylist("My Playlist")

removed = 0
for j in range(nbr_dupes):
    i = Remove_l[j]
    m = Pos[i]
    print("Checking file:",Arq[i],"(track reference still valid?","yes)" if track.sourceURL==Arq[i] else "no)")
    try:
        track = read_PL.Item(m)
    except:
        pass
    else:    
        try:
            print("Appending file to playlist",new_PL_name)
            new_PL.appendItem(track)
            read_PL.removeItem(track)
            # save playlist
            #new_PL.Save()
            #PL.mediaCollection.remove(track, True)
        except:
            print("Adding the track tp",new_PL_name,"has failed\n")
        else:
            removed = removed+1
            print("Removed",removed,"dupe files of",nbr_dupes,"\n")
                    
# FINAL
print("Removed:",removed,"dupes of",nbr_dupes,"files\n")
# print("Different dir:",len(Diff_dir),"\n")

