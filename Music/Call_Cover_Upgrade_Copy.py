# UPGRADES COVER THRU COPY FROM ANOTHER FILE
# IF A BETTER COVER EXISTS FOR THE SAME ALBUM
# WILL ONLY UPGRADE IF ONE IS LESS THAN 400 AND THE OTHER MORE THAN 500
# ALSO ATTACHES COVER IF THE TRACK HAS NO COVER BUT ANOTHER HAS IT

from os.path import exists
from os.path import getsize
#from os import remove
#from os import rename
import pandas as pd
import Tags
import Read_PL
import Images
import Files

# DISABLE PANDAS WARNINGS
pd.options.mode.chained_assignment = None  # default='warn'

Log_file = "D:\\itunes\\Upgrade_cover_copy.txt"

work_folder = "D:\\Z-Covers\\Upgrade_Copy\\"
#done_folder = "D:\\Z-Covers\\Upgrade_Done\\"
#mismat_folder = "D:\\Z-Covers\\Upgrade_Mismatch\\"

resize_pmt = (300, 300)
threshold_vl = 0.37

# THE TRACK BELOW IS THE BEST COVER TRACK ACTUALLY
def Comp(track,itunes_resized,itunes_hei,itunes_wid,itunes_cover_Kb):
    file = track.Location
    AA = track.AlbumArtist
    Album = track.Album
    new_cover = Images.Save_cover_iTu(track,work_folder,order="AA",tag="NEW",Remove_accent=True)
    new_cover_Kb = round(getsize(new_cover)/1024, 3)
    new_wid = Images.Wid(new_cover)
    new_hei = Images.Hei(new_cover)
    Eq_imgs = itunes_wid==new_wid and itunes_cover_Kb==new_cover_Kb
    # COMPARE ONLY IF DIFFERENT SIZES
    dict = {}
    dict["equal"] = Eq_imgs
    if min(new_hei,new_wid)>min(itunes_hei,itunes_wid):
       new_resized = Images.Read_and_resize(new_cover, desired_size = resize_pmt)
       comp = Images.Compare_imgs(new_resized, itunes_resized, show_img=False, threshold = threshold_vl)
       dict["metric"] = round(comp["metric"],5)
       dict["match"] = comp["match"]
       dict["cover"] = new_cover
    # FINAL
    return dict

# TRACKS THAT WILL BE SEARCHED 
def Criteria(Arq,Covers,Group):
    Fazer = False
    return Fazer

def Print_df(df):
    cols_to_exclude = ["ID","Arq","AA","Album","PL","AA2","Album2","Pos"]
    df_subset = df.drop(cols_to_exclude, axis=1)
    print(df_subset.head(10).to_string(index=False))

def Upgrade_copy(PL_name=None,PL_nbr=None):
    # CALLS FUNCTION "Art","Title",
    col_names =  ["Arq","Covers","AA","Album","ID"] 
    dict = Read_PL.Read_PL(col_names,PL_name=PL_name,PL_nbr=PL_nbr) 
    App = dict["App"]
    playlists = dict["PLs"]
    df = dict["DF"]

    # PRINT MESSAGE
    print("\nDF has",df.shape[0],"rows\n")

    # SELECT ONLY RELEVANT ROWS (df["Covers"]==1) & 
    df = df[(df["AA"] != "") & (df["Album"] != "")]

    # PRINT MESSAGE
    print("DF has",df.shape[0],"tracks with cover and album not missing\n")

    # FILE LIST
    # Arq = [x for x in df["Arq"]]
    # Wid = [Images.Img_dims(Arq[i]) for x in df["Arq"]]

    # ADDING COLS.
    df["AA2"] = df["AA"].str.lower()
    df["Album2"] = df["Album"].str.lower()
    # SELECT ONLY DUPE RECORDS
    group_list = ["AA2","Album2"]
    print("Calculating album pairs\n")
    df.loc[:,"Count"] = df.groupby(group_list)["Pos"].transform("count")

    # SELECT ONLY RELEVANT ROWS
    df = df[df["Count"]>1]

    # PRINT MESSAGE
    print("DF has",df.shape[0],"albums with more than one track\n")

    # CALCULATING COVER DIMS
    print("Calculating cover dimensions\n")
    # Conditionally create "Hei" column
    df.loc[:, "Hei"] = df.apply(lambda row: Images.Height(row["Arq"]) if row["Covers"] > 0 else 0, axis=1)
    df.loc[:, "Wid"] = df.apply(lambda row: Images.Width(row["Arq"]) if row["Covers"] > 0 else 0, axis=1)
    #df.loc[:, "Hei"] = df["Arq"].apply(Height)
    #df.loc[:, "Wid"] = df["Arq"].apply(Width)
    df.loc[:, "Min_dim"] = df[["Hei", "Wid"]].min(axis=1)
    df.loc[:, "Need_upgd"] = [1 if x < 400 else 0 for x in df["Min_dim"]]

    # SELECT ONLY DUPE RECORDS
    print("Calculating albums that need upgrade\n")
    df.loc[:,"Upg_flag"] = df.groupby(group_list)["Need_upgd"].transform("nunique")

    # SELECT ONLY RELEVANT ROWS
    df = df[df["Upg_flag"]==2]

    # PRINT MESSAGE
    print("DF has",df.shape[0],"albums that need upgrade\n")

    # ADDS COL. TO SELECT BEST COVER
    df.loc[:, "Best"] = abs(df["Hei"] - 600) + abs(df["Wid"] - 600)
    df.loc[:,"Min_best"] = df.groupby(group_list)["Best"].transform("min")
    df.loc[(df["Best"] == df["Min_best"]), "Best_candidate"] = df["Arq"]
    df.loc[(df["Best"] > df["Min_best"]), "Best_candidate"] = ""
    # NOW, FINALLY SELECT BEST COVER FILE
    df.loc[:,"Best_cover"] = df.groupby(group_list)["Best_candidate"].transform("max")

    # PRINTS
    # Print_df(df)

    # TEST LIST CREATION (list comprehension) 
    Arq = [x for x in df["Arq"]]
    ID = [x for x in df["ID"]]
    Need_upgd = [x for x in df["Need_upgd"]]
    Best_cover = [x for x in df["Best_cover"]]
    Covers = [x for x in df["Covers"]]
    nbr_files = len(Arq)
    # LIST THE COVERS
    Upg_list = [i for i in range(nbr_files) if Need_upgd[i]==1 and exists(Arq[i])]
    nbr_files_upg = len(Upg_list)

    # SALVA PL COM FILES QUE SERAO CHECADOS
    All_PL_name = "Upgrade_files"
    PL_dict = Read_PL.Create_PL(All_PL_name,recreate="n")
    File_list = PL_dict["Files"]
    for i in range(nbr_files):
        m = ID[i]
        track = App.GetITObjectByID(*m)
        Read_PL.Add_track_to_PL(playlists,All_PL_name,track,File_list=File_list)

    # CHAMA A FUNCAO QUE CRIA A PL
    # CRIA PLAYLIST APENAS SE HOUVER ARQUIVOS 
    Created_PL_name = "Upgrade_copied"
    if nbr_files_upg>0:
       PL_dict = Read_PL.Create_PL(Created_PL_name,recreate="n")
       # File_list = PL_dict["Files"]
    
    # STATS
    print("\nProcessing",nbr_files_upg,"files\n")
    
    fixed = 0
    for j in range(nbr_files_upg):
        i = Upg_list[j]
        m = ID[i]
        track = App.GetITObjectByID(*m)
        # PID = App.GetITObjectPersistentIDs(track)
        # SEARCH THE NEW COVER ON THE APPLE SITE
        file = track.Location
        AA = track.AlbumArtist
        Album = track.Album
        AA_Album = AA +" - "+ Album
        print("\nChecking file",j+1,"of",nbr_files_upg,":",Files.file_wo_ext(Arq[i]))
        print("Album:",AA_Album)
        # THE BEST COVER TRACK
        best_cover_vl = Best_cover[i]
        indice = Arq.index(best_cover_vl)
        m = ID[indice]
        best_track = App.GetITObjectByID(*m)
        # ITUNES
        if Covers[i]>0:
           itunes_cover = Images.Save_cover_iTu(track,work_folder,order="AA",Remove_accent=True)
           itunes_cover_Kb = round(getsize(itunes_cover)/1024, 3)
           itunes_wid = Images.Wid(itunes_cover)
           itunes_hei = Images.Hei(itunes_cover)
           itunes_resized = Images.Read_and_resize(itunes_cover, desired_size = resize_pmt)
           # START THE COMPARISON HERE
           if min(itunes_wid,itunes_hei)<400:
              best_match = Comp(best_track,itunes_resized,itunes_hei,itunes_wid,itunes_cover_Kb)
        else:
            itunes_best_cover = Images.Save_cover_iTu(best_track,work_folder,order="AA",tag="NEW",Remove_accent=True)
            best_match = {}
            best_match["match"] = True
            best_match["metric"] = -2
            best_match["cover"] = itunes_best_cover
        # NOW REPLACE IF OLD COVER MATCHES NEW   
        print("Match strenght:",best_match.get("metric",-1))
        if best_match.get("match",False):
           new_cover = best_match["cover"]
           attachf = Images.Attach_cover(Log_file,track,AA,Album,new_cover,fixed,VA=True)
           fixed = fixed+1
           Read_PL.Add_track_to_PL(playlists,Created_PL_name,track)
           if Covers[i]>0:
              New_group = Tags.Add_to_tag(track,"Upgraded",Tag="Group")

# CALLS FUNC Updt_AA_Album zzzz-Small
Upgrade_copy(PL_name="Playlist")


