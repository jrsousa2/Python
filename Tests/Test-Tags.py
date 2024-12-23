# This module obtains the MP3 ID3 tags indirectly
import eyed3

def Tag(File,read_tag):
    eyed3.log.setLevel("ERROR")
    audio = eyed3.load(File)
    #print("Title:",audio.tag.title)

    #mp3_file = "The_File_Path"
    #year = audio.tag.getBestDate()

    if read_tag.lower()=="art":
        res = audio.tag.artist
    elif read_tag.lower()=="title":
        res = audio.tag.title
    elif read_tag.lower()=="aa":
        res = audio.tag.album_artist
    elif read_tag.lower()=="album":
        res = audio.tag.album
    elif read_tag.lower()=="genre":
        res = audio.tag.genre
    elif read_tag.lower()=="year":
        res = audio.tag.getBestDate()
    else: 
        res = ""
    
    return res

""" L = ["Art","title","AA","Album","Genre","Year"]
for i in range(0,len(L)):
    myt = L[i]
    print(myt+" is",Tag("D:\\MP3\\favorites\\Abba - mamma mia.mp3",myt))
 """

#audio = eyed3.load("D:\\MP3\\favorites\\Abba - Fernando.mp3")
#print("Title:",audio.tag.title)

#print(Tag("D:\\MP3\\favorite\\Abba - Fernando.mp3","artist"))