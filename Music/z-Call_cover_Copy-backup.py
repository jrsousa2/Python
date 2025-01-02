# COPIES COVER FROM ONE FILE OVER TO ANOTHER, IF THE ALBUM NAMES MATCH
# USE TRANSFER TAGS FIRST TO POPULATE ALBUM TAGS
import Read_PL
from os.path import exists
import Tags
import Cover_logic
import Read_PL

# iTu_detach_folder = "D:\\Z-Covers\\Rz_Copy_covers\\"

iTu_detach_folder = "D:\\Videos\\Novelas\\Copy\\"

# MAIN CODE
def Copy_covers(PL_nbr=None):
    # CALLS FUNCTION
    #col_names =  ["Pos","Arq","Art","Title","AA","Album","Genre","Year"]
    dict = Read_PL.Init_iTunes()
    App = dict['App']
    PLs = dict['PLs']

    col_names =  ["Arq","AA","Album", "PID", "Covers"]
    df = Read_PL.Read_xml(col_names,rows=None)
    #dict = Read_PL.Read_PL(col_names,PL_nbr=PL_nbr)
    #dic = Read_PL.Read_PL(col_names,PL_nbr=37)
    PLs = dict['PLs']
    tracks = dict['tracks']
    result = dict['PL_nbr']
    PL_Name = dict['PL_Name']
    df = dict['DF']
    numtracks = tracks.Count

    #override_art=False
    # TEST LIST CREATION (list comprehension) 
    Pos = [x for x in df['Pos']]
    Arq = [x for x in df['Arq']]
    AA = [x for x in df['AA']]
    Album = [x for x in df['Album']]

    # CHANGE POS TO INTEGER
    df['Pos'] = df['Pos'].astype(int)

    # CRIA COL. AA-Album
    df['AA_Album'] = df['AA'].str.lower() + "@" + df['Album'].str.lower()
    # CRIA COUNTS
    df['Count'] = df.groupby('AA_Album')['Pos'].transform('count')
    df.loc[(df['AA']=='') | (df['Album']==''), 'Count'] = 0
    Count = [x for x in df['Count']]

    # 2o SYNC THE TAGS and key !='Cover'
    No_cover_PL_nm = "Cover_attached"
    Pop = Read_PL.Cria_PL(No_cover_PL_nm,recria="Y")

    # TRACKS WITH COVERS PL 
    Cover_PL_nm = "Cover_albums"
    Pop = Read_PL.Cria_PL(Cover_PL_nm,recria="Y")

    # REASSIGNS PLAYLIST (criar as 2 PLs acima daqui)
    # REASSIGNS PLAYLIST
    dict = Read_PL.Reassign_PL(PL_Name)
    tracks = dict['tracks']
    result = dict['PL_nbr']

    # I don't need to check art for all files, only those that match
    print("Checking files artwork:\n") 
    Covers = []
    for i in range(0,len(Arq)):
        if (i+1) % 100==0:
           print("Checking art",i+1,"of",len(Arq))
        Alb_not_blk = AA[i] != '' and Album[i] != ''
        if Count[i]>1 and Alb_not_blk and exists(Arq[i]):
           m = Pos[i]
           # If mode override on, do for all tracks in the list 
           Artobj_Count = tracks.Item(m).Artwork.count
           Artobj_Count = min(Artobj_Count,1)
        else:
            Artobj_Count = 0
        Covers.append(Artobj_Count)

    # ADD COVERS COL
    df['Covers'] = Covers

    # ALBUMS WHERE SOME FILES HAVE COVER AND OTHERS DON'T
    df['Flag'] = df.groupby('AA_Album')['Covers'].transform("nunique")
    # TEST FLAG
    Flag = [x for x in df['Flag']]

    # DETERMINES WHICH TO PICK AMONG THOSE WITH COVER
    df.loc[(df['Count'] > 1) & (df['Covers'] == 1) & (df['Flag']==2), 'Has_art'] = df['Pos']
    df.Has_art = df.Has_art.fillna(0)
    df['Has_art'] = df['Has_art'].astype(int)
    # TEST LIST
    Has_art = [x for x in df['Has_art']]

    # Pick only one file with cover for each AA-Album
    df['Max_Has_art'] = df.groupby('AA_Album')['Has_art'].transform('max')
    df['Max_Has_art'] = df['Max_Has_art'].astype(int)
    # TEST LIST
    Max_Has_art = [x for x in df['Max_Has_art']]
    

    # Initializes list
    No_cover = []
    Cover_files = []
    # CHECKS IF TRACK HAS ART:
    print("\nCreating lists of files that will be checked:\n")
    for i in range(0,len(Arq)):
        if (i+1) % 100==0:
           print("Processing",i+1,"of",len(Arq))
        if Flag[i]==2 and exists(Arq[i]):
           if Covers[i]==0:
              No_cover.append(i)
           else:
               if Has_art[i]==Max_Has_art[i]:
                  Cover_files.append(i)
                  Read_PL.Add_file_to_PL(PLs,Cover_PL_nm,Arq[i])

    # SAINDO DO LOOP
    print("\nFiles that don't have cover:",len(No_cover))
    print("Distinct albums with cover:",len(Cover_files),"\n")
    #print("")

    # Initiliazes issue counts
    fixed = {}
    fixed['iTunes saved'] = 0
    fixed['iTunes save exc'] = 0
    fixed['Attached'] = 0
    fixed['Attach exc'] = 0

    # Albs is a set for albums searched
    for i in range(0,len(No_cover)):
        n = No_cover[i]
        m = Pos[n]

        # Prints file being worked on
        print("Trying to attach cover",i+1,"of",len(No_cover),":",Tags.file_wo_ext(Arq[n]))

        if exists(Arq[n]) and Tags.Is_DMP3(Arq[n]):
            track = tracks.Item(m)
            Loc = track.location
            File_w_cover_pos = Max_Has_art[n]
            Srch_cover_file = Cover_logic.Save_cover_iTu(tracks.Item(File_w_cover_pos),iTu_detach_folder)
            if exists(Srch_cover_file):
                fixed['iTunes saved'] = fixed['iTunes saved'] + 1
                try:
                    track.AddArtworkFromFile(Srch_cover_file)
                except:
                    print("Attach exception has occurred")
                    fixed['Attach exc'] = fixed['Attached exc']+1
                else:
                    Read_PL.Add_file_to_PL(PLs,No_cover_PL_nm,Arq[n])
                    fixed['Attached'] = fixed['Attached']+1
            else:
                fixed['iTunes save exc'] = fixed['iTunes save exc']+1        
            
    print("")
    for key in fixed:
        if fixed[key] != 0:
           print("Final: ",key,"->",fixed[key])
    print("")

# CHAMA PROGRAM PL=12
Copy_covers()