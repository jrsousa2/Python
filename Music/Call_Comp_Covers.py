# COMPARA COVERS DE ARQUIVOS COM O MESMO ALBUM
# SO COMPARA SE ATRIBUTOS FOREM DIFERENTES (DIMENSOES E TAMANHO DO ARQUIVO)
import pandas as pd
from os.path import exists
from os.path import getsize
from unidecode import unidecode
from re import sub
import Read_PL
import Images
import Files


# DISABLE PANDAS WARNINGS
pd.options.mode.chained_assignment = None  # default='warn'

# This program will receive a DF and check which files can have tags or art transferred

Log_file = "D:\\iTunes\\Transfer_tags_log.txt"

work_folder = "D:\\Z-Covers\\Compare art\\"
done_folder = "D:\\Z-Covers\\Upgrade_Done\\"
mismat_folder = "D:\\Z-Covers\\Upgrade_Mismatch\\"

resize_pmt = (600, 600)
threshold_vl = 0.60

Priority_lst = ['Alb_not_miss', 'Alb_by_art_vl', 'Has_cover', 'Nice_cover_vl', 'Alb_not_great', \
                'Is_novela', 'One_hit_wonders', 'Is_Now', 'Ratio', 'Dim600', 'Dim550', 'Dim500', 'Dim450', 'Dim400']

digits = len(Priority_lst)


######################################################################################
######################################################################################
# THIS MODULE TRANSFER TAGS SUCH AS YEAR, GENRE AND ALBUM WHEN THE ARTIST-TITLE MATCH
def Comp_covers(PL_name_vl=None,PL_nbr=None,Do_lib=False,rows=None):
    # CALLS Read_PL FUNCTION ,Do_lib=True,rows=10
    # ONLY ADD BASIC ATTRIBUTES HERE
    col_names =  ["Arq","AA","Album","ID"] 
    dict = Read_PL.Read_PL(col_names,PL_name=PL_name_vl,PL_nbr=PL_nbr,Do_lib=Do_lib,rows=rows)
    # ASSIGNS
    App = dict['App']
    playlists = dict['PLs']
    df = dict['DF']

    # LISTS
    Arq = [x for x in df['Arq']]

    print("\nPrior to selection, df has",df.shape[0],"rows\n")

    # SELECT ONLY TRACKS WHERE AT LEAST ONE OF THE DUPES IS NOT MISSING
    
    not_miss = [exists(Arq[i]) for i in range(df.shape[0])]
    # ADDS NOT-MISSING COL. TO DF
    df.loc[:, "not_miss"] = not_miss
    
    # SELECT ONLY RELEVANT ROWS
    df = df[df['not_miss'] == True]

    print("The df has",df.shape[0],"dupes with only non-missing files")

    AA = [x for x in df['AA']]
    Album = [x for x in df['Album']]

    # Cria nova lista baseada nos nomes
    # ANY TRACK IS INCLUDED, INCLUDING THOSE WITH MISSING FILE 
    # HERE THE CHANGE HAS TO BE MINIMAL (ONLY UNICODE CONVERSION)
    print("\nHold on, checking tracks per album...")
    Album_stdz = []
    for i in range(df.shape[0]):
        AA_uni = sub(' +', ' ', unidecode(AA[i])) 
        Album_uni = sub(' +', ' ', unidecode(Album[i]))
        Album_stdz.append(AA_uni.lower()+" & "+Album_uni.lower())

    # CREATES COL. WITH STDZ TRACK NAMES
    df.loc[:, "Album_stdz"] = Album_stdz
    # FLAGS DUPES
    df['Count'] = df.groupby('Album_stdz')['Pos'].transform('count')

    # SELECT ONLY RELEVANT ROWS
    df = df[df['Count'] > 1]

    print("The df has",df.shape[0],"tracks where count of AA-Album>1")

   
    # COVERS
    Arq = [x for x in df['Arq']]
    ID = [x for x in df['ID']]
    print("\nBuilding cover list...\n")
    Covers = []
    Hei_lst = []
    Wid_lst = []
    Size_lst = []
    Img_not_found_cnt = 0
    tam = df.shape[0] // 20
    for i in range(df.shape[0]):
        if (i+1) % tam==0:
            print("Checked",i+1,"covers of",df.shape[0],"// file:",Arq[i])
        m = ID[i]
        track = App.GetITObjectByID(*m)
        Artobj = track.Artwork
        Art_count = Artobj.count
        Has_cover = False
        if Art_count>0:
           try:
              dict = Images.Img_dims(Arq[i])
              Has_cover = dict['Has_cover']
           except:
               pass   
        # POPULATES LISTS
        Hei = 0
        Wid = 0
        Cover_size = 0
        if Has_cover:
           Hei = dict['Hei']
           Wid = dict['Wid']
           Cover_size_dict = Images.Cover_size(Arq[i])
           Cover_size = Cover_size_dict["Size"]
           if Cover_size_dict["Img_not_found"]:
              Img_not_found_cnt = Img_not_found_cnt + 1 
        # ADDS SCORE    
        Covers.append(Art_count)
        Hei_lst.append(Hei)
        Wid_lst.append(Wid)
        Size_lst.append(Cover_size)
    # ADDS TO THE DF    
    df.loc[:, "Covers"] = Covers
    df.loc[:, "Hei"] = Hei_lst
    df.loc[:, "Wid"] = Wid_lst
    df.loc[:, "Art_size"] = Size_lst

    # SELECT ONLY RELEVANT ROWS
    df = df[df['Covers'] > 0]

    print("\nThe df has",df.shape[0],"tracks with covers")
    print("Image not found in",Img_not_found_cnt,"files (cover size not available)")
    
    # NOW SELECT ONLY ROWS WHERE THE DATA MAY CHANGE
    # concatenate columns A and B into a new column C
    # ADDS COVER COL. TO DF 
    df['Key'] = df['Hei'].astype(str) +"@"+ df['Wid'].astype(str) + "@" + df['Art_size'].astype(str)
    
    # COUNTS DISTINCT COVERS PER ALBUM
    df['dist_Key'] = df.groupby('Album_stdz')['Key'].transform('nunique')

    df = df[df['dist_Key'] > 1]

    print("\nThe df has",df.shape[0],"albums (tracks) with different covers")

    # NOW SELECT ONLY ROWS WHERE THE DATA MAY CHANGE
    # ADDS KEY COL. TO DF
    df['bench_track'] = df.groupby('Album_stdz')['Arq'].transform('max')
    # Create column C based on the condition (1 if A == B, else 0)
    df['Flag'] = df.apply(lambda row: 1 if row['Arq'] == row['bench_track'] else 0, axis=1)
    
    # SORTS DF
    # CRIA COL. LOCATION IN LOWER CASE (THE DIRECT SYNTAX IS NOT NICE)
    # df['Arq_lower'] = df['Arq'].str.lower()
    # SORTS THE DF SO THE DUPES APPEAR AT THE TOP
    df = df.sort_values(['Count','Album_stdz','Flag'], ascending=[True, True, False])

    # SAVES DATA TO AN EXCEL FILE
    # df.to_excel("D:\\iTunes\\Excel\\Cover_diferente.xlsx", index=False)

    # REFRESHES TRACK LIST
    Arq = [x for x in df['Arq']]
    ID = [x for x in df['ID']]
    Flag = [x for x in df['Flag']]
    nbr_files = df.shape[0]

    # CREATES A NEW PLAYLIST TO SAVE DUPES IF NEEDED TO RE-RUN MANY TIMES
    # CRIA PLAYLISTS
    if nbr_files>0:
       PL_nm = "Covers_Comparable"
       PL = Read_PL.Create_PL(PL_nm,recreate="n")
       Diff_cover_PL_nm = "Covers_Different"
       Diff_cover_PL = Read_PL.Create_PL(Diff_cover_PL_nm,recreate="y")

    # ADD TRACKS TO NEW PL
    # DOESN'T NEED TO CHECK IF FILE EXISTS, MISSING FILES ARE NOT ADDED 
    if nbr_files>0 and not PL["PL_exists"]:
       print("\nCreating PL with possible different covers...(",nbr_files,"files)")
       for i in range(nbr_files):
           m = ID[i]
           track = App.GetITObjectByID(*m)
           Read_PL.Add_track_to_PL(playlists,PL_nm,track)

    # INICIA A COMPARACAO
    for i in range(nbr_files):
        m = ID[i]
        track = App.GetITObjectByID(*m)
        # SEARCH THE NEW COVER ON THE APPLE SITE
        file = track.Location
        AA = track.AlbumArtist
        Album = track.Album
        AA_Album = AA +" - "+ Album
        print("\nChecking file",i+1,"of",nbr_files,":",Files.file_wo_ext(Arq[i]),"\\\\ Album:",AA_Album)

        # COMPARE LOGIC
        if Flag[i]==1:
           Added_bench = False
           bench_ID = ID[i]
           print("File is the benchmark")
           bench_cover = Images.Save_cover_iTu(track,work_folder,order="AA",Remove_accent=True)
           bench_resized = Images.Read_and_resize(bench_cover, desired_size = resize_pmt) 
        else:
            print("File is to be compared")
            comp_cover = Images.Save_cover_iTu(track,work_folder,order="AA",Remove_accent=True)
            # COMPARE ONLY IF DIFFERENT SIZES
            dict = {}
            comp_resized = Images.Read_and_resize(comp_cover, desired_size = resize_pmt)
            comp = Images.Compare_imgs(comp_resized, bench_resized, show_img=False, threshold = threshold_vl)
            print("Match strenght:",comp.get("metric","N/A"))
            if not comp["match"]:
               # ONLY ADD BENCHMARK IF A HIT OCCURS
               if not Added_bench:
                  track_bench = App.GetITObjectByID(*bench_ID)
                  Read_PL.Add_track_to_PL(playlists,Diff_cover_PL_nm,track_bench) 
                  Added_bench = True
               # ADD THE COVER THAT MISMATCHES   
               Read_PL.Add_track_to_PL(playlists,Diff_cover_PL_nm,track)   

#CALLS FUNC Transfer_Dupes zzzzzz-CoverCheck
Comp_covers(PL_name="AAA3",Do_lib=0)