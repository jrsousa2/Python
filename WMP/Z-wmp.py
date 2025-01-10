# try:
#     wmp.mediaCollection.add("D:\\MP3\\Playlists\\NewPlaylist (2).wpl")
# except:    
#     pass

#url2 = PL_col1.getItemInfo("sourceURL")
#url = PL_col1.sourceURL
# for PL in PL_col:
#     test = PL.getItemInfo("URL")
#     Arq = PL.sourceULR
# Art = track.getItemInfo("Artist")
# Arq = track.sourceURL


# try:
#     new_PL = library.newPlaylist("My Playlist")
# except:
#     pass    

# add some tracks to the playlist
#track1 = mc.getByPath("D:\\MP3\Favorites\\The Maxx - Cocaine.mp3")
#playlist.appendItem(track1)

#path = "D:\\MP3\\Playlists\\Testa.wpl"
#new_PL.Save(path)

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

# WMPLib.IWMPPlaylistCollection.getByname method. 
# This method returns the WMPLib.IWMPPlaylist

# Get the playlist object
# playlist = wmp.mediaCollection.getByAttribute("PlaylistID", playlist_id)

# # Get the name of the playlist
# name = playlist.name
# No, the getByAttribute method of the WMPLib.IWMPMediaCollection object only supports the following attributes:

# "MediaType"
# "Author"
# "Title"
# "Album"
# "Year"
# "Genre"
# "Duration"
# "Bitrate"
# "FileSize"
# "FileCreateDate"
# "FileModifyDate"
# "FileAccessDate"
# "Rating"
# "DateAdded"
# "AlbumArtist"
# "ContributingArtist"
# "Composer"
# "OriginalArtist"
# "Lyrics"
# "CDTrackNumber"
# "CDTrackCount"
# "IsProtected"
# "IsAvailable"
# There is no attribute for playlist name. 
# However, once you have a reference to a WMPLib.IWMPPlaylist object, 
# you can get its name using the name property, as I showed in my previous answer.