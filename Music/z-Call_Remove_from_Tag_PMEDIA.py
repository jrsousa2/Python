# REMOVES ALL TAGS THAT CONTAIN PMEDIA
# IT REMOVES THE VAST MAJORITY (the remaindar of the tags can be removed manually in Mp3Tag)
# IT'S WORKING WELL
from os.path import exists
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

import Files
import Read_PL

tag_descs = {
    'TALB': 'Album',
    'TBPM': 'BPM',
    'TCOM': 'Composer',
    'TCON': 'Genre',
    'TCOP': 'Copyright message',
    'TDAT': 'Date',
    'TDLY': 'Playlist delay',
    'TENC': 'Encoded by',
    'TEXT': 'Lyricist/Text writer',
    'TFLT': 'File type',
    'TIME': 'Time',
    'TIT1': 'Content group description',
    'TIT2': 'Title',
    'TIT3': 'Subtitle/Description refinement',
    'TKEY': 'Initial key',
    'TLAN': 'Language(s)',
    'TLEN': 'Length',
    'TMED': 'Media type',
    'TOAL': 'Original album/movie/show title',
    'TOFN': 'Original filename',
    'TOLY': 'Original lyricist(s)/text writer(s)',
    'TOPE': 'Original artist(s)/performer(s)',
    'TORY': 'Original release year',
    'TOWN': 'File owner/licensee',
    'TPE1': 'Artist',
    'TPE2': 'Album artist',
    'TPE3': 'Conductor/performer refinement',
    'TPE4': 'Interpreted, remixed, or otherwise modified by',
    'TPOS': 'Part of a set',
    'TPUB': 'Publisher',
    'TRCK': 'Track number',
    'TRDA': 'Recording dates',
    'TRSN': 'Internet radio station name',
    'TRSO': 'Internet radio station owner',
    'TSIZ': 'Size',
    'TSRC': 'ISRC (international standard recording code)',
    'TSSE': 'Software/Hardware and settings used for encoding',
    'TYER': 'Year',
    'TXXX:RELEASECOUNTRY': 'Release Country',
    'APIC:': 'Attached picture',
    'GRP1': 'Grouping',
    'TDRC': 'Year'
}

# Get the description of each tag
def tag_desc(tag_name):
    if tag_name in tag_descs:
        desc = tag_descs[tag_name]
    else:
        desc = None
    return desc

# Replace 'your_file.mp3' with the path to your MP3 file
def all_tags(path):
    # Load the MP3 file
    audio = MP3(path, ID3=ID3)
    # Get all the tags
    tag_list = audio.tags.keys()
    #tag_names = [tag.split(":")[-1] for tag in audio.tags.keys()]
    #tag_names = [x for x in tag_names if x != ""]
    return tag_list

def Upgrade(PL_name=None,PL_nbr=None):
    # CALLS FUNCTION "Art","Title","AA","Album"
    col_names =  ["Arq","Group","ID"] 
    dict = Read_PL.Read_PL(col_names,PL_name=PL_name,PL_nbr=PL_nbr) 
    App = dict['App']
    playlists = dict['PLs']
    df = dict['DF']

    print()
    # TEST LIST CREATION (list comprehension) 
    Arq = [x for x in df['Arq']]
    ID = [x for x in df['ID']]
    nbr_files = len(Arq)

    # CRIA PLAYLIST APENAS SE HOUVER ARQUIVOS 
    Created_PL_name = "Remove_PMEDIA"
    Move_PL = Read_PL.Cria_PL(Created_PL_name,recria="n")

    # STATS
    print("\nUpdating",nbr_files,"files\n")

    # READS PLAYLISTS
    deleted = 0
    for i in range(nbr_files):
        m = ID[i]
        track = App.GetITObjectByID(*m)
        path = track.Location
        tag_list = all_tags(path)
        print("\nChecking file",i+1,"of",nbr_files,":",Files.file_wo_ext(path))
        removed = False
        # CREATING EXTERNAL TAGS
        for srch_tag in tag_list:
            try:
               tag_value = ID3(path)[srch_tag].text[0]
            except:
               tag_value = None
               print("\tTag", srch_tag,"has no text[0] attribute")   
            
            # CHECKS VALUES 
            print("\tExternal tag",srch_tag,"(", tag_desc(srch_tag),")",":",tag_value)
            if tag_value in ["PMEDIA", "www.t.me/pmedia_music", "PMEDIA☺"]: 
               removed = True
               deleted = deleted + 1
               print("\tRemoving external tag",srch_tag,":",tag_value)
               Files.remove_tag(path, srch_tag)
        
        # ADD TO PLAYLIST IF CHANGED        
        if removed:
           Read_PL.Add_track_to_PL(playlists,Created_PL_name,track)
    
    print("\nDeleted",deleted,"junk tags")
# CALLS FUNC zzzzz-Albums
Upgrade(PL_name="BBB")
