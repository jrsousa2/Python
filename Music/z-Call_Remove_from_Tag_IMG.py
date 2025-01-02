# TRY TO RESET ALBUM RATING
from os.path import exists
import Tags
import Files
import Read_PL
import Images

# TRACKS THAT WILL BE SEARCHED 
def Criteria(Arq,Min_dim,Group):
    Fazer = exists(Arq) and Min_dim>=400 and (Group.lower().find("small")>=0 or Group.lower().find("looked")>=0)
    return Fazer

def Upgrade(PL_name=None,PL_nbr=None):
    # CALLS FUNCTION "Art","Title","AA","Album"
    col_names =  ["Arq","Covers","AA","Album","Group","ID"] 
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
    Hei = [Images.Height(Arq[i]) for i in range(nbr_files)]
    Wid = [Images.Width(Arq[i]) for i in range(nbr_files)]
    Min_dim = [min(Hei[i],Wid[i]) for i in range(nbr_files)]
    # LIST THE COVERS
    Do_list = [i for i in range(nbr_files) if Criteria(Arq[i],Min_dim[i],Group[i])]
    nbr_files = len(Arq)
    nbr_files_updt = len(Do_list)

    # CRIA PLAYLIST APENAS SE HOUVER ARQUIVOS 
    Created_PL_name = "Fix_Tag"
    Move_PL = Read_PL.Cria_PL(Created_PL_name,recria="n")

    # STATS
    print("\nUpdating",nbr_files_updt,"of",nbr_files,"files\n")

    # READS PLAYLISTS
    fixed = 0
    for j in range(nbr_files_updt):
        i = Do_list[j]
        m = ID[i]
        track = App.GetITObjectByID(*m)
        print("Fixing tag",j+1,"of",nbr_files_updt,":",Files.file_wo_ext(track.Location),"\\ Tag:",track.Grouping)
        if Min_dim[i]>400:
           New_group = Tags.Rem_from_tag(track,["Small","Looked"],Tag="Group")
           New_group = Tags.Add_to_tag(track,"Upgraded",Tag="Group")
        if New_group != "":
           print("\tNew tag:",New_group)
           Read_PL.Add_track_to_PL(playlists,Created_PL_name,track)
  
# CALLS FUNC zzzzz-Albums
Upgrade(PL_name="Playlist 3")


