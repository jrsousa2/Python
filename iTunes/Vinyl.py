# FINDS OUT WHAT COVERS ARE VINYL IMAGES
#from mutagen.id3 import ID3

from os.path import exists
from os import remove
import Read_PL
import Images
import Tags

iTu_detach_folder = "D:\\Z-Covers\\Vinyl2\\"

def Vinyl(PL_name=None,PL_nbr=None):
    # CALLS FUNCTION "Art","Title","AA","Album"
    col_names =  ["Arq","Covers","Group","ID"] 
    dict = Read_PL.Read_PL(col_names,PL_name=PL_name,PL_nbr=PL_nbr) 
    App = dict['App']
    playlists = dict['PLs']
    df = dict['DF']
    
    # TEST LIST CREATION (list comprehension) 
    Arq = [x for x in df['Arq']]
    ID = [x for x in df['ID']]
    Covers = [x for x in df['Covers']]
    Group = [x for x in df['Group']]
    nbr_files = len(Arq)
    # LIST THE COVERS
    Has_cover = [i for i in range(nbr_files) if exists(Arq[i]) and Covers[i]>0 and Group[i].lower().find("vinylcover")==-1]
    nbr_files_check = len(Has_cover)

    # CHAMA A FUNCAO QUE CRIA A PL
    # CRIA PLAYLIST APENAS SE HOUVER ARQUIVOS 
    Created_PL_name = "Vinyl"
    Move_PL = Read_PL.Create_PL(Created_PL_name,recreate="n")
    
    # STATS
    print("\nProcessing",nbr_files_check,"files\n")

    # READS PLAYLISTS
    tagged = 0
    for j in range(nbr_files_check):
        print("Checking file",j+1,"of",nbr_files_check,"files")
        i = Has_cover[j]
        m = ID[i]
        track = App.GetITObjectByID(*m)
        cover_img = Images.Save_cover_iTu(track,iTu_detach_folder,tag="old",order="file",Remove_accent=True)
        cover_resized = Images.Read_and_resize(cover_img)
        vinyl_resized = Images.Read_and_resize("D:\\Z-Covers\\Vinyl\\template.jpg")
        match_dict = Images.Compare_imgs(cover_resized, vinyl_resized, threshold=0.37, color=False)
        # NOW REPLACE IF OLD COVER MATCHES NEW   
        print("Match strenght:",match_dict.get("metric",-1))
        if match_dict["match"]:
           tagged = tagged+1
           print("Vinyl covers:",tagged)
           New_group = Tags.Add_to_tag(track,"VinylCover",Tag="Group")
           Read_PL.Add_track_to_PL(playlists,Created_PL_name,track)
        else:
            remove(cover_img)   

# CALLS FUNC Updt_AA_Album zzzz-Not Vinyl
Vinyl(PL_name="Updt_AA_Album")


