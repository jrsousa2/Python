import win32com.client

# Create a WMP object
player = win32com.client.Dispatch("WMPlayer.OCX")

# Get the media library object
library = player.mediaCollection

# Filter for songs only
#library.mediaType = "audio"

# Iterate over all the songs in the library
for i in range(library.count):
    media = library.get_Item(i)
    if media is not None:
        print(media.name)
