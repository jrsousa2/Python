import Cria_PL
import Proper
from os.path import exists
from tinytag import TinyTag

# Pass the filename into the
# Tinytag.get() method and store
# the result in audio variable
def Tag(File,read_tag):
    audio = TinyTag.get(File)

    if read_tag.lower()=="art":
        res = audio.artist
    elif read_tag.lower()=="title":
        res = audio.title
    elif read_tag.lower()=="aa":
        res = audio.albumartist
    elif read_tag.lower()=="album":
        res = audio.album
    elif read_tag.lower()=="genre":
        res = audio.genre
    elif read_tag.lower()=="year":
        res = audio.year
    else: 
        res = ""
    
    return res

# MATCHES ITUNES TAGS TO WINDOWS TAGS
Tags = ["Art","title","AA","Album","Genre","Year"]
for i in range(0,len(Tags)):
    myt = Tags[i]
    print(myt+" is",Tag("D:\\MP3\\favorites\\Abba - mamma mia.mp3",myt))
