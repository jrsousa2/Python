# REMOVES COUNTRY, LABEL OR FORMAT FROM GROUPING TAG
# SO IT CAN'T BE DONE BY THE OTHER CODE
# IT'S MORE CONVOLUTED THAN REMOVING A SINGLE VALUE
from os.path import exists
import Tags
import Files
import Read_PL

# RETURNS THE VALUE OF AN ELEMENT (COUNTRY/LABEL/FORMAT)
def find_elem_in_list(lst, target):
    for element in lst:
        if target in element:
           values = element.split("=")
           return values[1]
    return None  # Return None if no element contains the target string

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
    Group = [x for x in df['Group']]
    nbr_files = len(Arq)

    # CRIA PLAYLIST APENAS SE HOUVER ARQUIVOS 
    Created_PL_name = "Fix_Tag"
    Move_PL = Read_PL.Create_PL(Created_PL_name,recreate="n")

    # STATS
    print("\nUpdating",nbr_files,"files\n")

    # READS PLAYLISTS
    fixed = 0
    Rem_list = ["Country=", "Format=", "Label="]
    for i in range(nbr_files):
        m = ID[i]
        track = App.GetITObjectByID(*m)
        path = track.Location
        print("\nFixing tag",i+1,"of",nbr_files,":",Files.file_wo_ext(path))
        print("Grouping:",track.Grouping)
        removed = False
        # CREATING EXTERNAL TAGS
        for srch_tag in Rem_list:
            srch_tag = srch_tag.replace("=", "")
            tag_split_list = Group[i].split("\\")
            tag_value = find_elem_in_list(tag_split_list, srch_tag)
            if tag_value is not None and not Files.ext_tag_exist(path, srch_tag.upper()):
               removed = True
               print("\tWriting external tag",srch_tag,":",tag_value)
               writ_tag = Files.write_tag(path, srch_tag.upper(), tag_value)
               New_group = Tags.Rem_from_tag(track, srch_tag+"=" ,Tag="Group",Full_match=False)
               if New_group != "":
                  print("\tNew tag:",New_group)
            elif tag_value is None:
                 print("\tTag",srch_tag,"not found") 
        
        # ADD TO PLAYLIST IF CHANGED        
        if removed:
           Read_PL.Add_track_to_PL(playlists,Created_PL_name,track)
  
# CALLS FUNC zzzzz-Albums
Upgrade(PL_name="BBB")


