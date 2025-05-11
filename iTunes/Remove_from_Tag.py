# TRY TO RESET ALBUM RATING
from os.path import exists
import Tags
import Files
import Read_PL
import Images

def get_tag_attribs(track, tag):
    tag_assign = {"Genre": track.Genre, "Group": track.Grouping}
    Cur_tag = tag_assign[tag]
    return Cur_tag

def Tag_updt(PL_name=None,PL_nbr=None,updt_tag="Genre",To_rem=None,To_add=[]):
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
    nbr_files = len(Arq)

    # CRIA PLAYLIST APENAS SE HOUVER ARQUIVOS 
    Created_PL_name = "Fix_" + updt_tag + "_"  + "_".join(To_rem)+"_To_"+"_".join(To_add)
    Move_PL = Read_PL.Create_PL(Created_PL_name,recreate="y")

    # STATS
    print("\nUpdating",nbr_files,"of",nbr_files,"files\n")

    # READS PLAYLISTS
    fixed = 0
    for i in range(nbr_files):
        m = ID[i]
        track = App.GetITObjectByID(*m)
        tag_assign = {"Genre": track.Genre, "Group": track.Grouping}
        Cur_tag = tag_assign[updt_tag]
        print("\nUpdating",updt_tag,i+1,"of",nbr_files,":",Files.file_wo_ext(track.Location),"\\",updt_tag,":",Cur_tag)
        if "".join(To_rem) in Cur_tag:
            New_group = Tags.Rem_from_tag(track,To_rem,Tag=updt_tag)
            for value in To_add:
                New_group1 = Tags.Add_to_tag(track,value,Tag=updt_tag)
            fixed = fixed + 1
            print("\tNew tag:",get_tag_attribs(track, updt_tag))
            Read_PL.Add_track_to_PL(playlists,Created_PL_name,track)
    
    print("\nFixed", fixed, "tags\n")
# CALLS FUNC zzzzz-Albums
#Genre_updt(PL_name="B_File_ne_Tags",updt_tag="Group",To_rem=["Tag_file_match"],To_add=[])
Tag_updt(PL_name="AAA",updt_tag="Genre",To_rem=["Indie Rock"],To_add=["Alternative", "Rock"])
#Tag_updt(PL_name="AAA2",updt_tag="Genre",To_rem=["Classic Hard Rock"],To_add=["Rock"])


