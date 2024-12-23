# TRIES TO REPLACE LOW QUALITY COVERS WITH THE SAME COVER
# DOWNLOADED FROM THE APPLE SITE (IF FOUND)
# CHECKS IF THE COVERS MATCH FIRST

import discogs_client
from os.path import exists
from os.path import getsize
from os import remove
from os import rename
from time import sleep
import Tags
import Read_PL
import Images
import Files

Log_file = "D:\\itunes\\Upgrade_cover_dwld.txt"

work_folder = "D:\\Z-Covers\\Upgrade\\"
done_folder = "D:\\Z-Covers\\Upgrade_Done\\"
mismat_folder = "D:\\Z-Covers\\Upgrade_Mismatch\\"

resize_pmt = (300, 300)
threshold_vl = 0.37

  

# DOWNLOADS AND COMPARES
def Dwld_and_comp(track,itunes_resized,itunes_wid,itunes_cover_Kb,urls):
    file = track.Location
    AA = track.AlbumArtist
    Album = track.Album
    nbr_urls = len(urls)
    list = []
    gray_scale = Images.Gray_scale(AA)
    for i in range(nbr_urls):
        URL = urls[i]
        new_cover = Images.Dwld_cover(file,AA,Album,URL,work_folder,order="AA",Remove_accent=True)
        new_cover_Kb = round(getsize(new_cover)/1024, 3)
        new_wid = Images.Wid(new_cover)
        new_hei = Images.Hei(new_cover)
        Eq_imgs = itunes_wid==new_wid and itunes_cover_Kb==new_cover_Kb
        # COMPARE ONLY IF DIFFERENT SIZES
        dict = {}
        dict["equal"] = Eq_imgs
        if new_wid>itunes_wid:
           new_resized = Images.Read_and_resize(new_cover, desired_size = resize_pmt, gray_scale = gray_scale)
           comp = Images.Compare_imgs(new_resized, itunes_resized, show_img=False, threshold = threshold_vl)
           dict["metric"] = round(comp["metric"],6)
           dict["match"] = comp["match"]
           dict["cover"] = new_cover
        # sleep(1)   
        list.append(dict)
    # FINAL
    return list

# TRACKS THAT WILL BE SEARCHED 
def Criteria(Arq,AA,Covers,Group):
    Fazer = exists(Arq) and Covers>0 and Group.lower().find("small")>=0 \
            and Group.lower().find("looked")==-1 \
            and Group.lower().find("upgrade")==-1 \
            and not Tags.Is_VA(AA)
    return Fazer

def Upgrade(PL_name=None,PL_nbr=None):
    # CALLS FUNCTION "Art","Title","AA","Album"
    col_names =  ["Arq","AA","Album","Covers","Group","ID"] 
    dict = Read_PL.Read_PL(col_names,PL_name=PL_name,PL_nbr=PL_nbr) 
    App = dict['App']
    playlists = dict['PLs']
    df = dict['DF']

    # PRINT MESSAGE
    print("\nDF has",df.shape[0],"rows\n")

    # SELECT SINGLE TRACK FOR EACH ALBUM
    group_list = ["AA","Album"]
    df.loc[:,"Max_arq"] = df.groupby(group_list)["Arq"].transform("max")

    # SELECT ONLY RELEVANT ROWS
    df = df[df["Arq"]==df["Max_arq"]]

    # PRINT MESSAGE
    print("DF has",df.shape[0],"distinct albums\n")
    
    # TEST LIST CREATION (list comprehension) 
    Arq = [x for x in df['Arq']]
    AA = [x for x in df['AA']]
    ID = [x for x in df['ID']]
    Covers = [x for x in df['Covers']]
    Group = [x for x in df['Group']]
    nbr_files = len(Arq)
    # LIST THE COVERS
    Has_cover = [i for i in range(nbr_files) if Criteria(Arq[i],AA[i],Covers[i],Group[i])]
    nbr_files_check = len(Has_cover)

    # CHAMA A FUNCAO QUE CRIA A PL
    # CRIA PLAYLIST APENAS SE HOUVER ARQUIVOS 
    Created_PL_name = "Upgrade_Dwld"
    Move_PL = Read_PL.Cria_PL(Created_PL_name,recria="n")
    
    # STATS
    print("\nProcessing",nbr_files_check,"files\n")

    # CALLS THE DISCOGS OBJECT (NEEDS USER TOKEN)
    my_user_token = "docQjZEPqWxycqKxScnAQVTKsvQKwjqFkjrmEGWA"
    disco = discogs_client.Client("ExampleApplication/0.1", user_token=my_user_token)
    
    fixed = 0
    for j in range(nbr_files_check):
        i = Has_cover[j]
        m = ID[i]
        track = App.GetITObjectByID(*m)
        # SEARCH THE NEW COVER ON THE APPLE SITE
        file = track.Location
        AA = track.AlbumArtist
        Album = track.Album
        AA_Album = AA +" - "+ Album
        print("\nChecking file",j+1,"of",nbr_files_check,":",Files.file_wo_ext(Arq[i]))
        print("Album:",AA_Album)
        itunes_cover = Images.Save_cover_iTu(track,work_folder,order="AA",Remove_accent=True)
        itunes_cover_Kb = round(getsize(itunes_cover)/1024, 3)
        itunes_wid = Images.Wid(itunes_cover)
        itunes_hei = Images.Hei(itunes_cover)
        itunes_resized = Images.Read_and_resize(itunes_cover, desired_size = resize_pmt, gray_scale = Images.Gray_scale(AA))
        # START THE COMPARISON HERE
        if min(itunes_wid,itunes_hei)<400:
           # APPLE
           list_Apple = Images.get_Apple_cover_url(AA_Album)
           # DISCOGS MASTER
           list_master = Images.get_discogs_cover_url(disco, "master", AA, Album)
           # DISCOGS RELEASE
           list_rel = Images.get_discogs_cover_url(disco, "release", AA, Album)
           list_all = list_Apple + list_master + list_rel
           res = Dwld_and_comp(track,itunes_resized,itunes_wid,itunes_cover_Kb,list_all)
        else:
            New_group = Tags.Rem_from_tag(track,["Small"],Tag="Group")   
        nbr_res = len(res)
        # THE CHOSEN ALBUM    
        # OBTAIN THE BEST MATCH dict_busca.get('Attempt',0)
        try:
            Scores = [res[i].get("metric",-1) for i in range(nbr_res)]
            max_score = max(Scores)
            indice = Scores.index(max_score)
            best_match = res[indice]
        except:
            best_match = {}
        Upgraded = False     
        print("Match strenght:",best_match.get("metric","N/A"),"\\ Results:",nbr_res)
        if best_match.get("match",False):
           new_cover = best_match["cover"]
           attachf = Images.Attach_cover(Log_file,track,AA,Album,new_cover,fixed,VA=True)
           fixed = fixed+1
           Read_PL.Add_track_to_PL(playlists,Created_PL_name,track)
           # Files.Move_covers(itunes_cover, done_folder)
           # Files.Move_covers(new_cover, done_folder)
           New_group = Tags.Add_to_tag(track,"Upgraded",Tag="Group")
           New_group = Tags.Rem_from_tag(track,["Small"],Tag="Group")
           Upgraded = True
        # MOVE OLD COVER TO MISMATCH FOLDER ONLY IF THERE ARE RESULTS
        if nbr_res==0 or min(itunes_wid,itunes_hei)>=400:
           remove(itunes_cover)
        elif best_match.get("metric",0)<threshold_vl:   
             Files.Move_covers(itunes_cover, mismat_folder)
        else:
            Files.Move_covers(itunes_cover, done_folder)   
        # MOVE NEW COVERS
        for k in range(nbr_res):
            if res[k].get("cover","") != "":
               if Upgraded:
                  if res[k].get("match",False):
                     Files.Move_covers(res[k]["cover"], done_folder)
                  else:
                      remove(res[k]["cover"])   
               else:
                   Files.Move_covers(res[k]["cover"], mismat_folder)  
        # REASSIGNS THE TRACK
        if not best_match.get("match",False):
           track = App.GetITObjectByID(*ID[i])
           New_group = Tags.Add_to_tag(track,"Looked",Tag="Group")
        sleep(3)
        #if best_match["metric"]==-1:
        #   sleep(3)

# CALLS FUNC Updt_AA_Album zzzz-Small
Upgrade(PL_name="Playlist")


