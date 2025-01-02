# THIS CODE POPULATES ARTWORK USING APPLE SEARCHES
import Read_PL
from os.path import exists
from time import sleep
import Tags
import Cover_logic
import Busca

# MAIN CODE
def Call_artwork(recheck_files=True,override_art=True,PL_nbr=None):
    
    # CALLS FUNCTION
    col_names =  ["Pos","Arq","Art","Title","AA","Album","Genre","Year"]
    dic = Read_PL.Read_PL(col_names,PL_nbr=PL_nbr)
    playlists = dic['PLs']
    tracks = dic['tracks']
    result = dic['PL_nbr']
    df = dic['DF']
    PL_Name = dic['PL_Name']
    numtracks = tracks.Count

    #override_art=False
    # TEST LIST CREATION (list comprehension) 
    Pos = [x for x in df['Pos']]
    Arq = [x for x in df['Arq']]
    Art = [x for x in df['Art']]
    Title = [x for x in df['Title']]
    AA = [x for x in df['AA']]
    Album = [x for x in df['Album']]
    Genre = [x for x in df['Genre']]
    Year = [x for x in df['Year']]
    #Year = [x if x.lower() !='empty' else '' for x in df['Year']]

    # List of dictionaries
    main_dic = []
    for i in range(0,len(Arq)):
        dic = {'Arq': Arq[i],'Art': Art[i],'Title': Title[i],'AA': AA[i],'Album': Album[i],'Genre': Genre[i],'Year': Year[i]}
        main_dic.append(dic)

    # Cria sets para nao adicionar dupes
    PL_files = {}
    PL_files["Looked"] = set([])
    
    # Cria lista de arqs a serem ignorados
    if not recheck_files:
       print("\nCreating lists of files to be skipped")
       Read_PL.Cria_skip_list(playlists,"Looked",PL_files)
    
    # CREATES PL's (doesn't recreate any, unless they don't exis)
    PL = Read_PL.Read_PL("Hits")
    PL = Read_PL.Read_PL("Looked")
    PL = Read_PL.Read_PL("Found_Year") 
    PL = Read_PL.Read_PL("Found_Genre") 
    PL = Read_PL.Read_PL("Found_Cover") 

    # REASSIGNS PLAYLIST
    dict = Read_PL.Reassign_PL(PL_Name)
    tracks = dict['tracks']
    result = dict['PL_nbr']

    # Initializes list
    to_fix_dic = {}
    to_fix_dic['Cover'] = []
    to_fix_dic['Year'] = []
    to_fix_dic['Genre'] = []
    
    # CHECKS IF TRACK HAS ART:
    print("Creating lists of files that will be checked: Cover, Year and Genre\n")
    for i in range(0,len(Arq)):
        if exists(Arq[i]) and Arq[i].lower() not in PL_files["Looked"]:
           m = Pos[i]
           track = tracks.Item(m)

           # If mode override on, do for all tracks in the list 
           # IF NOT OVERRIDE ARTWORK, STILL DOES IF FILE HAS NO COVER
           cover_list = False
           if override_art: 
              to_fix_dic['Cover'].append(i)
              cover_list = True
           else:
                if not Cover_logic.Has_artwork(track):
                   to_fix_dic['Cover'].append(i)
                   cover_list = True

           #test = track.Year
           year_list = False
           if not cover_list:
              Year_upd = track.Year
              if Year_upd == 0:
                  to_fix_dic['Year'].append(i)
                  year_list = True

           # don't include values from the Year list in the genre list
           if not cover_list and not year_list:
              Genre_upd = track.Genre
              if Genre_upd == '':
                 to_fix_dic['Genre'].append(i)
   
    # SAINDO DO LOOP
    for key in to_fix_dic:
        print("Files that don't have",key,":",len(to_fix_dic[key]))
    print("\n(Excludes files in previous categories)")

    # INICIO DA BUSCA
    #res = input("Press Y to find art/tags: ")
    res = "y"

    # 2o SYNC THE TAGS and key !='Cover'
    counts = {}
    attempts = {}

    for key in to_fix_dic:
        if res.lower() == 'y' and len(to_fix_dic[key])>0:
            # REASSIGNS PLAYLIST
            dic = Read_PL.Reassign_PL(PL_Name)
            tracks = dic['tracks']
            result = dic['PL_nbr']
            
            # attempts
            attempts[key]={}
            for i in range(1,6):
                attempts[key][i]=0

            # TYPES LIST 
            # Type_list = []

            # Initiliazes ISSUE COUNTS
            counts[key] = {}
            counts[key]['Searched'] = 0
            counts[key]['No_result'] = 0
            counts[key]['Entries'] = 0
            counts[key]['Found'] = 0
            counts[key]['Match_title'] = 0
            counts[key]['Match_album'] = 0
            counts[key]['Match_both'] = 0
            counts[key]['wrapper=track'] = 0
            counts[key]['wrapper=Album'] = 0
            counts[key]['wrapper=None'] = 0
            counts[key]['Downloaded'] = 0
            counts[key]['iTunes saved'] = 0
            counts[key]['iTunes save exc'] = 0
            counts[key]['iTunes detach'] = 0
            counts[key]['Attached'] = 0
            counts[key]['Attach exc'] = 0
            counts[key]['Apple del'] = 0
            counts[key]['iTunes del'] = 0
            counts[key]['Genre upd'] = 0
            counts[key]['Album upd'] = 0
            counts[key]['Album upd exc'] = 0
            counts[key]['Year upd'] = 0
            counts[key]['Json exc'] = 0
            counts[key]['VA_flag'] = 0
            # COVER RESULTS
            counts[key]['Art2Art'] = 0
            counts[key]['Art2VA'] = 0
            counts[key]['Art2Null'] = 0
            counts[key]['VA2Art'] = 0
            counts[key]['VA2VA'] = 0
            counts[key]['VA2Null'] = 0
            counts[key]['Null2Art'] = 0
            counts[key]['Null2VA'] = 0
            counts[key]['Null2Null'] = 0

            # Albs is a set for albums searched
            Albs_searched = set([])
            Albs_found = set([])
            key_count = len(to_fix_dic[key])
            
            # LOOP
            for i in range(0,len(to_fix_dic[key])):
                n = to_fix_dic[key][i]
                m = Pos[n]
                # INFO THAT GOES IN THE BEGINNING OF THE PRINTED LINE  
                print_head = key + ": File " + str(i+1) + " of " + str(key_count)+":"

                if exists(Arq[n]) and Arq[n].lower() not in PL_files["Looked"]:
                    # first try to match by title
                    dict_aux = Busca.Busca(print_head,i,main_dic[n],nbr_searches=5)
                    counts_tmp = dict_aux['counts']
                    dict_busca = dict_aux['dict_res']
                    achou = dict_busca['Achou']
                    aux = key
                    # COUNTS EVENTS
                    for key1 in counts_tmp.keys():
                        counts[key][key1] = counts[key][key1]+counts_tmp[key1]
                    sleep(2.2)
                    dont_readd = False
                    if dict_busca.get('Hits',False):
                       # se foi hit por title mas nao achou, adicionar 
                       Read_PL.Add_file_to_PL(playlists,"Hits",Arq[n])
                       dont_readd = True
                    
                    # second try to match by album, if 1st attempt fails
                    if not achou:
                        Alb_not_blk = main_dic[n]['AA'] != '' and main_dic[n]['Album'] != ''
                        Alb = main_dic[n]['AA'].lower() + "@" + main_dic[n]['Album'].lower()
                        if Alb not in Albs_searched and Alb_not_blk:
                           # RUNS SEARCH 
                           dict_aux = Busca.Busca(print_head,i,main_dic[n],srch_by="album",nbr_searches=5)
                           counts_tmp = dict_aux['counts']
                           dict_busca = dict_aux['dict_res']
                           achou = dict_busca['Achou']
                           # COUNTS EVENTS
                           for key1 in counts_tmp.keys():
                               counts[key][key1] = counts[key][key1]+counts_tmp[key1]
                           pos = dict_busca.get('Attempt',0)
                           if achou:
                              attempts[aux][pos] = attempts[aux][pos]+1
                           sleep(2.2)

                           if Alb_not_blk:
                              Albs_searched.add(Alb)
                           if achou and Alb_not_blk:
                              Albs_found.add(Alb)
                        else:
                            if Alb in Albs_found and Alb_not_blk:
                               print(print_head,Alb.title(),"-> has been checked already and FOUND\n") 
                               achou = Busca.Busca(print_head,i,main_dic[n],srch_by="album") 
                               sleep(2.2)
                            elif Alb_not_blk:
                                 print(print_head,Alb.title(),"-> has been checked already and NOT found\n")
                            elif not Alb_not_blk:
                                 print(print_head,"Album is blank and can't be searched\n")     
                        # se foi hit por album mas nao achou, adicionar 
                        # se nao bater com anterior
                        if not dict_busca.get('Hits',False) and dont_readd:
                           Read_PL.Add_file_to_PL(playlists,"Hits",Arq[n])

                    if dict_busca.get('RC',False):
                        Attpt = dict_busca.get('Attempt',0)
                        attempts[key][Attpt] = attempts[key][Attpt]+1

                        track = tracks.Item(m)
                        
                        # Updates Genre
                        New_genre = dict_busca.get('Genre','') 
                        Tags.Uptd_genre(playlists,track,New_genre,counts[key]['Genre upd'],Arq[n])
                        
                        # Uppdates Year if it's greater than the current one (which includes missing) 
                        New_year = dict_busca.get('Year',0) 
                        Year_updated = Tags.Uptd_year(playlists,track,New_year,counts[key]['Year upd'],Arq[n])    

                        # Testa baixar/salvar arq
                        # Calls macro to save cover
                        if key=='Cover':
                            dict_aux = Cover_logic.Attach_cover(main_dic[n],dict_busca,track,counts[key],Year_updated)
                            Attached = dict_aux['Attached']
                            if Attached:
                               From = dict_aux['From']
                               To = dict_aux['To']
                               counts[key][From + '2' + To] = counts[key][From + '2' + To]+1
                            # add track to PL 
                            if Attached:
                               Read_PL.Add_file_to_PL(playlists,"Found_Cover",Arq[n])
                     
                    # add track to PL at the end
                    Read_PL.Add_file_to_PL(playlists,"Looked",Arq[n])
        

    print("")
    for key in to_fix_dic.keys():
        if len(to_fix_dic[key])>0:
           print("\nStats for",key,"->",len(to_fix_dic[key]),"tracks\n")
           for key2 in counts[key].keys():
               if counts[key][key2] != 0:
                  print(key,":",key2,"->",counts[key][key2])
           print("\nNow the stats on match attempts\n")
           for key2 in attempts[key].keys():
               print(key,":",key2,"attempts->",attempts[key][key2])
    print("")        

# CALL func
# BY SETTING OVERRIDE_ART TO FALSE, IT WILL NOT TRY AND RE-POPULATE THE COVERS, JUST YEAR AND GENRE
# recheck_files = False => NAO PROCESSA ARQS QUE FORAM CHECADOS ANTES (melhor deixar em True por enqto)
Call_artwork(recheck_files=True,override_art=False)

#Call_art(df,playlists,result,skip_files=True,override_art=True)