# FIXES THE CASE OF THE TAGS OF ALL MP3 FILES IN THE LIBRARY 
# ACCORDING TO A GIVEN LOGIC FOUND IN MODULE PROPER
# IT'S NOW RELYING ON THE XML, INSTEAD OF READING THE LIBRARY, WHICH IS MUCH MORE TIME CONSUMING
# THE XML IS ALWAYS IN SYNC WITH THE LIBRARY

import Call_Proper
from os.path import exists
import Read_PL
#import Files

# INITIALIZE DICTS
def Proper_dict(main_dict):
    # populates the dicts
    proper_dict = {}
    for key in main_dict:
        proper_dict[key] = Call_Proper.Call_Proper(main_dict[key],key)
    return proper_dict

# CHECK IF A VALUE IS THIS PESKY NAN VALUE
def nan_to_blank(value):
    if value != value:
       res = ""
    else:
       res = value   
    return res

# 1o ADICIONA TRACKS NA PLAYLIST
def Call_proper(rows=None):
    # START
    dict = Read_PL.Init_iTunes()
    App = dict['App']
    PLs = dict['PLs']

    # READS XML
    col_names = ["Arq","Art","Title","AA","Album","PID"]
    dict = Read_PL.Read_xml(col_names,rows=rows)
    df = dict['DF']

    # TEST LIST CREATION (list comprehension) 
    Arq = [x for x in df['Arq']]
    Art = [x for x in df['Art']]
    Title = [x for x in df['Title']]
    AA = [x for x in df['AA']]
    Album = [x for x in df['Album']]
    PID = [x for x in df['PID']]
    nbr_files = len(Arq)

    # CREATES LIST OF DICTIONARIES 
    main_dic = []
    for i in range(nbr_files):
        dic = {'Art': nan_to_blank(Art[i]),'Title': nan_to_blank(Title[i]),'AA': nan_to_blank(AA[i]),'Album': nan_to_blank(Album[i])}
        main_dic.append(dic)

    to_fix_dic = {}
    to_fix_dic['All'] = []
    for key in main_dic[0]:
        to_fix_dic[key] = []

    # 1st CHECK
    print("\nChecking files to have case fixed...\n")
    for i in range(nbr_files):
        if exists(Arq[i]): # and Files.Is_DMP3(Arq[i])
           #proper_dic = {}
           proper_dic = Proper_dict(main_dic[i])

           if main_dic[i] != proper_dic:
              to_fix_dic['All'].append(i)
              for key in proper_dic:
                  if main_dic[i][key] != proper_dic[key] and proper_dic[key] != '':
                     to_fix_dic[key].append(i)
           if (i+1) % 1000==0:
               print("Checked",i+1,"of",nbr_files) 

    # SAINDO DO LOOP
    # Stats das tags que serao arrumadas
    print("")
    for key in to_fix_dic:
        if key=="All":
           print("Files to have case fixed:",len(to_fix_dic[key]),"\n")
        else:
            print(key,"tags to be fixed:",len(to_fix_dic[key]))

    print()
    
    # 2o FIX THE TAGS
    if len(to_fix_dic["All"])>0:
       # CHAMA A FUNCAO QUE CRIA A PL
       PL_nm = "Fix_case"
       Tag_PL = Read_PL.Create_PL(PL_nm)
       
       # INITIALIZE FIXED COUNT VECTOR
       fixed = {}
       for key in main_dic[0]:
           fixed[key] = 0

       for i in range(len(to_fix_dic['All'])):
           n = to_fix_dic['All'][i]
           #m = ID[n]
           #track = App.GetITObjectByID(*m)

           m = Read_PL.unpack('!ii', Read_PL.a2b_hex(PID[n]))
           track = App.LibraryPlaylist.Tracks.ItemByPersistentID(*m)

           if Arq[n]==track.Location:
              # ADDS FIXED FILE TO PL
              Read_PL.Add_track_to_PL(PLs,PL_nm,track)    
              #main_dic = {}
              proper_dic = Proper_dict(main_dic[n])
            
              for key in main_dic[0]:
                  if main_dic[n][key] != proper_dic[key]:
                     fixed[key] = fixed[key]+1
                     print(i+1,"Fixing",key,":",main_dic[n][key],"->",proper_dic[key])
                     # MAPPING
                     attr_name = Read_PL.iTunes_all_tags_dict[key]    
                     # SET PROPERTY TO TRACK
                     setattr(track, attr_name, proper_dic[key])
              print()            

       print("\nFinal:",len(to_fix_dic['All']),"files fixed")
       for key in fixed:
           print("\nFixed:",fixed[key],key,"tags")
       print()

# CALLS FUNC PL=12
Call_proper(rows=None)