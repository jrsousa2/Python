# COPIES COVER FROM ONE FILE OVER TO ANOTHER, IF THE ALBUM NAMES MATCH
# USE TRANSFER TAGS FIRST TO POPULATE ALBUM TAGS
from os.path import exists
from struct import unpack
from binascii import a2b_hex
from Files import file_wo_ext
import Read_PL
import Tags
import Images
import Read_PL

# iTu_detach_folder = "D:\\Z-Covers\\Rz_Copy_covers\\"

iTu_detach_folder = "D:\\Videos\\Novelas\\Copy\\"

# MAIN CODE
def Copy_covers():
    # CALLS FUNCTION
    dict = Read_PL.Init_iTunes()
    App = dict['App']
    PLs = dict['PLs']

    col_names =  ["Arq","AA","Album", "PID", "Covers"]
    dict = Read_PL.Read_xml(col_names,rows=None)
    df = dict['DF']
    
    # ADDS BINARY COVER COL. (0 or 1)
    df['Covers_bin'] = df['Covers'].apply(lambda x: 1 if x > 0 else 0)
    # ADD POS COLUMN
    df['Pos'] = range(1, len(df) + 1)
    
    # TEST FILES THAT EXIST
    File_found = [exists(x) for x in df['Arq']]

    start_rows = df.shape[0]
    df['File_found'] = File_found
    # SELECT ONLY TRACKS THAT MATTER
    df = df[(df['File_found']==True) & (df['Album'] != '')]
    mid_rows = df.shape[0]

    # CRIA COL. AA-Album
    df['AA_Album'] = df['AA'].str.lower() + "@" + df['Album'].str.lower()

    # ALBUMS WHERE SOME FILES HAVE COVER AND OTHERS DON'T
    df['Flag'] = df.groupby('AA_Album')['Covers_bin'].transform("nunique")
    # SELECT ONLY TRACKS THAT MATTER
    df = df[(df["Flag"] == 2)]
    end_rows = df.shape[0]

    # SORTS THE DF SO THE DUPES APPEAR AT THE TOP
    df = df.sort_values(["AA_Album","Covers"], ascending=[True, True])

    # ISSUES INFO ABOUT THE DF
    print("\nThe df has",start_rows,"tracks before selection (end rows:",end_rows,", mid rows:",mid_rows,")")

    # DETERMINES WHICH TO PICK AMONG THOSE WITH COVER
    df.loc[(df['Covers_bin'] == 1), 'Has_art'] = df['Pos']
    df.Has_art = df.Has_art.fillna(0)
    df['Has_art'] = df['Has_art'].astype(int)

    # Pick only one file with cover for each AA-Album
    df['Max_Has_art'] = df.groupby('AA_Album')['Has_art'].transform('max')
    df['Max_Has_art'] = df['Max_Has_art'].astype(int)
    
    # TEST LIST
    Pos = [x for x in df['Pos']]
    Arq = [x for x in df['Arq']]
    PID = [x for x in df['PID']]
    Covers = [x for x in df['Covers_bin']]
    Has_art = [x for x in df['Has_art']]
    Max_Has_art = [x for x in df['Max_Has_art']]

    # PLAYLIST NAMES
    No_cover_PL_nm = "Cover_attached"
    Pop = Read_PL.Create_PL(No_cover_PL_nm,recreate="N")
    # TRACKS WITH COVERS PL 
    Cover_PL_nm = "Cover_albums"
    Pop = Read_PL.Create_PL(Cover_PL_nm,recreate="N")

    # Initializes list
    No_cover = []
    Cover_files = []
    # CHECKS IF TRACK HAS ART:
    print("\nCreating lists of files that will be checked:\n")
    for i in range(len(Arq)):
        if (i+1) % 100==0:
           print("Processing",i+1,"of",len(Arq))
        if Covers[i]==0:
              No_cover.append(i)
        else:
            if Has_art[i]==Max_Has_art[i]:
               Cover_files.append(i)
               Read_PL.Add_file_to_PL(PLs,Cover_PL_nm,Arq[i])

    nbr_no_cover = len(No_cover)
    # SAINDO DO LOOP
    print("\nFiles that don't have cover:",nbr_no_cover)
    print("Distinct albums with cover:",len(Cover_files),"\n")
    #print("")

    # Initiliazes issue counts
    fixed = {}
    fixed['iTunes saved'] = 0
    fixed['iTunes save exc'] = 0
    fixed['Attached'] = 0
    fixed['Attach exc'] = 0

    file_nm = "D:\\iTunes\\Excel\\Test.xlsx"
    # save the dataframe to an Excel file
    #df.to_excel(file_nm, index=False)

    # Albs is a set for albums searched
    for i in range(nbr_no_cover):
        n = No_cover[i]
        # Prints file being worked on
        print("Trying to attach cover",i+1,"of",nbr_no_cover,":",file_wo_ext(Arq[n]))
        m = unpack('!ii', a2b_hex(PID[n]))
        track = App.LibraryPlaylist.Tracks.ItemByPersistentID(*m)
        # TRACK THAT HAS THE COVER
        File_w_cover_pos = Pos.index(Max_Has_art[n])
        #File_w_cover_pos = Max_Has_art[n]
        m = unpack('!ii', a2b_hex(PID[File_w_cover_pos]))
        track_w_cover = App.LibraryPlaylist.Tracks.ItemByPersistentID(*m)
        # PRINT CONFIRMATION
        print("\tAlbum:",track.Album,"//",file_wo_ext(track_w_cover.location),"\n")
        Srch_cover_file = Images.Save_cover_iTu(track_w_cover,iTu_detach_folder)
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