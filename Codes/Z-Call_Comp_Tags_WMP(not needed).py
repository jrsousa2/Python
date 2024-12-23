# DOES A COMPARISON BETWEEN WMP AND iTUNES TAGS

from os.path import exists
import pandas as pd
from timeit import default_timer
import Read_PL
import WMP_Read_PL as WMP
import Files

def time_msg(start_time):
    end_time = default_timer()
    elapsed_time = end_time - start_time
    print("\nElapsed time",round(elapsed_time/60,2),"minutes (",round(elapsed_time,2),"seconds)")

def freq(df,vars = ['iTunes', 'WMP']):
    freq = df.groupby(vars).size().reset_index(name='count')
    print("\n",freq)

# MAIN CODE
def Comp_tags(PL_name=None,PL_nbr=None,Do_lib=False,rows=None,Do_wmp=1):
    # CALLS Read_PL FUNCTION ,Do_lib=True,rows=10
    col_names =  ["Arq","Art","Title","AA","Album","Genre","Year"]
    col_names_itu = col_names.copy()
    col_names_itu.append("ID")
    
    # ITUNES
    start_time = default_timer()
    dict1 = Read_PL.Read_PL(col_names_itu,PL_name=PL_name,PL_nbr=PL_nbr,Do_lib=Do_lib,rows=rows,Modify_cols=False)
    time_msg(start_time)
    
    df_itu = dict1["DF"]
    # KEEP ONLY SELECTED COLS.
    df_itu = df_itu.loc[:, col_names_itu]
    # LOWER CASE
    df_itu['Arq'] = df_itu['Arq'].str.lower()
    nbr_rows = df_itu.shape[0]
    # Eliminate duplicate records based on "Arq" column
    df_itu = df_itu.drop_duplicates(subset="Arq", keep="first")
    df_itu = df_itu[df_itu['Arq'] != ""]
    # Create flags for presence in df1 and df2
    df_itu['iTunes'] = 1

    print("\nThe iTunes df has",df_itu.shape[0],"rows (",nbr_rows,"with dupes)")

    # PLAYLIST
    iTunesApp = dict1['App']
    playlists = dict1['PLs']

    # WMP
    if Do_wmp:
        start_time = default_timer()
        if PL_name is None:
           dict2 = WMP.Read_WMP_PL(col_names,PL_name=PL_name,PL_nbr=PL_nbr,Do_lib=Do_lib,rows=rows,Modify_cols=False)
        else:
            Arq = [x for x in df_itu['Arq']]
            print("\nReading the tracks from the iTunes playlist in WMP")  
            dict2 = WMP.Read_WMP_MC(col_names,Arq,Modify_cols=True)   
        
        time_msg(start_time)
        
        df_wmp = dict2["DF"]

        # SAVE TO EXCEL FILE:
        # df_wmp.to_excel("D:\\iTunes\\Excel\\WMP_test.xlsx", index=False)
        
        print("\nThe WMP df has",df_wmp.shape[0],"rows")
        col_names_wmp = col_names.copy()
        col_names_wmp.append("Pos")
        # KEEP ONLY SELECTED COLS.
        df_wmp = df_wmp.loc[:, col_names_wmp]
        # LOWER CASE
        df_wmp['Arq'] = df_wmp['Arq'].str.lower()
        # Rename columns
        df_wmp = df_wmp.rename(columns={"Art": "Art_wmp","Title": "Title_wmp","AA": "AA_wmp","Album": "Album_wmp", \
                                        "Genre": "Genre_wmp","Year": "Year_wmp"})
        nbr_rows = df_wmp.shape[0]
        # Eliminate duplicate records based on "Arq" column
        df_wmp = df_wmp.drop_duplicates(subset="Arq", keep="first")
        # print STATS
        print("\nThe WMP df has",df_wmp.shape[0],"rows (",nbr_rows,"with dupes)")
        # CREATES WMP FLAG
        df_wmp['WMP'] = 1

        # WMP LIBRARY ITEMS
        wmp = dict2["WMP"]
        library = dict2["Lib"]
        wmp_PL = dict2["PL"]
    else:
         print("\nThe WMP df has 0 rows (not doing WMP)")
         # Create an empty DataFrame with the same columns as the original DataFrame
         # df_wmp = pd.DataFrame(columns=df_itu.columns)

    # JOIN THE DATAFRAMES
    if Do_wmp:
       df = df_itu.merge(df_wmp, on="Arq", how="outer") # outer
    else:
        df = df_itu 
        df_wmp['WMP'] = 0

    print("\nThe full joined df has",df.shape[0],"rows")

    # Fill missing values in the flags columns with False
    df['iTunes'] = df['iTunes'].fillna(0)
    df['WMP'] = df['WMP'].fillna(0)

    df['iTunes'] = df['iTunes'].astype(int)
    df['WMP'] = df['WMP'].astype(int)


    # FREQS
    print("\nFreq prior to selection")
    freq(df)

    # DIFFERENCES:
    Tags = ['Art', 'Title', 'AA', 'Album', 'Genre', 'Year']

    
    # USANDO TINYTAG: read_tag
    if Do_wmp:
       # COMPARE ITUNES X WMP
       for tag in Tags:
           df[f'{tag}_eq'] = df.apply(lambda row: int(row[tag]==row[f'{tag}_wmp']) if (row['iTunes'] == row['WMP'] == 1) else 1, axis=1)
    else:    
        print("\nReading tags...this may take a while")
        start_time = default_timer()
        for tag in Tags:
            df[f'{tag}_tiny'] = df.apply(lambda row: Files.read_tinytag(row["Arq"], tag), axis=1)
        time_msg(start_time)

        # CONVERTS YEAR TO NUMERIC
        df['Year_tiny'] = pd.to_numeric(df['Year_tiny'], errors="coerce")
        df['Year_tiny'] = df['Year_tiny'].fillna(0)

        # ITUNES DIFFERENCES WITH TINY
        for tag in Tags:
            df[f'{tag}_eq'] = df.apply(lambda row: int(row[tag] == row[f'{tag}_tiny']), axis=1)

    # CHECKS FREQS
    for tag in Tags:
        freq(df,vars = [f"{tag}_eq"])  

    # SAVES ALL FILES
    Miss = [arq for arq, itunes in zip(df['Arq'], df['iTunes']) if itunes == 0]

    print("\nThe df has",len(Miss),"rows where the file is in WMP but not iTunes")

    # FLAG FOR RECORDS THAT WILL BE SELECTED
    df["Sel"] = df.apply(lambda row: int(row['iTunes']==row['WMP']==1) if Do_wmp else 1, axis=1)

    # FREQS
    print("\nThe selection")
    freq(df,vars = ["Sel"]) 

    # DIFFERENT (df['iTunes'] ==1) |
    df = df[(df['Sel']==1) & ((df['Art_eq'] == 0) | (df['Title_eq'] == 0) | (df['AA_eq'] == 0) |
             (df['Album_eq'] == 0) | (df['Genre_eq'] == 0) | (df['Year_eq'] == 0))]

    # COUNT DIFFERENT TAGS
    tags_mismatch = ((df['Art_eq'] == 0) | (df['Title_eq'] == 0) | (df['AA_eq'] == 0) |
                     (df['Album_eq'] == 0) | (df['Genre_eq'] == 0) | (df['Year_eq'] == 0)).sum()

    print("\nThe df has",tags_mismatch,"rows where itunes and","wmp" if Do_wmp else "tiny","tags don't match")

    # FREQS
    print("\nFreq after selection")
    freq(df)


# USANDO TINYTAG: read_tag
    if Do_wmp:
       Pos = [x for x in df['Pos']]

    # CREATES LISTS
    Arq = [x for x in df['Arq']]
    Art_eq = [x for x in df['Art_eq']]
    Title_eq = [x for x in df['Title_eq']]
    AA_eq = [x for x in df['AA_eq']]
    Album_eq = [x for x in df['Album_eq']]
    Genre_eq = [x for x in df['Genre_eq']]
    Year_eq = [x for x in df['Year_eq']]
    iTunes = [x for x in df['iTunes']]
    ID = [x for x in df['ID']]
    dict = {"Art": Art_eq,"Title": Title_eq,"AA": AA_eq,"Album": Album_eq,"Genre": Genre_eq,"Year": Year_eq}
    nbr_files = len(Arq)

    # tinytag = Files.read_tag(Arq[0] , "title")
    # tag = iTunesApp.GetITObjectByID(*ID[0]).name

    # CREATES MISMATCH PLAYLISTS
    # PL = Read_PL.Cria_PL("Tag_mism_Only_WMP", recria="n")
    # PL = Read_PL.Cria_PL("Tag_mism_All", recria="n")
    for key in dict:
        PL = Read_PL.Cria_PL("Tag_mism_" + key, recria="n")

    # ADDS MISMATCHING FILES TO PL
    for i in range(nbr_files):
        for key in dict:
            if dict[key][i]==0:  
               Read_PL.Add_file_to_PL(playlists,"Tag_mism_" + key,Arq[i])
        
        # ALL files with differences
        if False and Do_wmp and rows==None:
           Read_PL.Add_file_to_PL(playlists,"Tag_mism_All",Arq[i]) 
        
    
    # ADDS MISMATCHING FILES TO PL
    if Do_wmp and (rows==None or PL_name != ""):
       for i in range(len(Miss)):
           if Files.Is_DMP3(Miss[i]):  
              Read_PL.Add_file_to_PL(playlists,"Tag_mism_Only_WMP",Miss[i])
   
    if False and df.shape[0]>0:
       # SAVE TO EXCEL FILE:
       file_nm = "D:\\iTunes\\Excel\\Tag_comp.xlsx"

       print("\nSaving data to Excel file...")
       # save the dataframe to an Excel file
       df.to_excel(file_nm, sheet_name="Compare", index=False)

    # FIX WMP ISSUES
    wmp_updt = 0
    itu_updt = 0
    if Do_wmp:
       for i in range(nbr_files):
           m = Pos[i]
           if Do_lib:
              track_wmp = library[m]
           elif PL_name is not None:
                PL = wmp.mediaCollection.getByAttribute("SourceURL", Arq[i])
                track_wmp = PL.Item(0)   
           else:
               track_wmp = wmp_PL.Item(m)
           wmp_tags = WMP.tag_dict_wmp(track_wmp,col_names)
           # ASSIGNS TRACK WITH TUPLE
           m = ID[i]
           track_itu = iTunesApp.GetITObjectByID(*m)
           for tag in Tags:
               itu_tag = getattr(track_itu, Read_PL.iTu_tag_dict[tag])
               wmp_tag = wmp_tags[tag]
               if tag == "Year":
                  try:
                     wmp_tag = int(wmp_tag) 
                  except:
                     wmp_tag = 0    
               # WMP   
               if itu_tag != wmp_tag and tag not in ["Title"]:
                  wmp_updt = wmp_updt + 1
                  if tag == "Year":
                     tag_nm = "WM/Year" # "ReleaseDateYear"
                  else:
                     tag_nm = WMP.tag_dict[tag]   
                     print("\nUpdating WMP",tag,"tag. From",wmp_tag,"->",itu_tag)
                     track_wmp.setItemInfo(tag_nm, itu_tag if type(itu_tag) is str else str(itu_tag)) # if type(itu_tag) is str else str(itu_tag)
                     new_value = track_wmp.getItemInfo(tag_nm)
                     print(tag,"after update:", new_value)
               # ITUNES  
               if itu_tag != wmp_tag:
                  itu_updt = itu_updt + 1
                  if tag != "Year":
                     print("\nRewriting iTunes",tag,"tag...")
                     # update the iTunes track object dynamically
                     setattr(track_itu, Read_PL.iTu_tag_dict[tag], itu_tag + " ")
                     setattr(track_itu, Read_PL.iTu_tag_dict[tag], itu_tag.strip())
                  else:
                      setattr(track_itu, Read_PL.iTu_tag_dict[tag], itu_tag + 1)
                      setattr(track_itu, Read_PL.iTu_tag_dict[tag], itu_tag)
                  

    print("\nUpdated",wmp_updt,"WMP tags")
    print("\nUpdated",itu_updt,"iTunes tags")
    # Clean up and release resources
    wmp.close()

# CHAMA PROGRAM PL_name="ALL",Fave-iPhone
Comp_tags(PL_name="AAA",Do_lib=0,rows=None,Do_wmp=1)

