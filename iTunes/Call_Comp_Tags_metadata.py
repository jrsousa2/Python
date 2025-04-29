# COMPARES ITUNES (OR WMP) TAGS WITH ACTUAL FILE METADATA
# SINCE EYED3 AND TINYTAG PRODUCE THE SAME RESULTS, ONLY TINYTAG IS BEING USED
# (PREVIOUSLY WAS USING BOTH EYED3 AND TINYTAG)
# IN CASE OF MISMATCH, REWRITES THE TAGS IN ITUNES OR WMP 
# ITUNES DIDN'T HAVE MATERIAL MISMATCHES WITH TINYTAG (VERY FEW DUE TO SPECIAL CHARS)
# ALL THE DIFFERENCES WITH WMP HAVE BEEN FIXED (INITIALLY CIRCA 700)
from os.path import exists
import Files

# TENHO QUE PASSAR OS PMTS PARA QUE ELES POSSAM RETORNAR A ROTINA PRINCIPAL
def Reads_tags(Arq,i,dict_main,tag_app,tag_tiny):
    # populates the dicts
    for key in dict_main.keys():
        tag_app[key] = dict_main[key][i]
        tag_tiny[key] = Files.read_tinytag(Arq[i], key)

# A FUNCAO PRINCIPAL
def Comp(iTunes=True,rows=None):
    # CALLS FUNCTION
    col_names =  ["Arq","Art","Title","AA","Album","Genre", "PID", "Group"] # "Group"

    if iTunes:
       import Read_PL
       # INITIALIZE
       dict = Read_PL.Init_iTunes()
       App = dict['App']
       PLs = dict['PLs']
       dict = Read_PL.Read_xml(col_names,rows=rows)
       df = dict['DF']
    else:   
        import WMP_Read_PL as WMP # type: ignore
        # EXCLUDE INVALID TAGS 
        col_names =  ["Arq","Art","Title","AA","Album","Genre", "Group"] # "Group"
        dict = WMP.Read_WMP_PL(col_names,Do_lib=True,rows=rows) 
        library = dict["Lib"]
        df = dict["DF"]

    # TEST LIST CREATION (list comprehension) 
    PID = []
    Arq = [x for x in df['Arq']]
    Art = [x for x in df['Art']]
    Title = [x for x in df['Title']]
    AA = [x for x in df['AA']]
    Album = [x for x in df['Album']]
    Genre = [x for x in df['Genre']]
    Group = [x for x in df['Group']]
    nbr_files = len(Arq)

    #THIS IS A DICTIONARY OF LISTS (Lists are Art thru Genre)
    dict_main = {}
    dict_main['Art'] = Art
    dict_main['Title'] = Title
    dict_main['AA'] = AA
    dict_main['Album'] = Album
    dict_main['Genre'] = Genre

    # LIST OF TAGS TO BE CHECKED
    tags_comp_lst = list(dict_main.keys())

    to_fix_dic = {}
    to_fix_dic['All'] = []
    for key in dict_main.keys():
        to_fix_dic[key] = []

    # TAGS JA COMPARADAS
    if iTunes:
       #PID = [x for x in df['PID2']]
       Alrdy_srchd = "Tags_already_comp"
       PL = Read_PL.Create_PL(Alrdy_srchd,recreate="N")   
       PL_Mismatch = "Tags_Mismatch"
       PL = Read_PL.Create_PL(PL_Mismatch,recreate="N")

    print("\nTags Comparison\n")
    for i in range(nbr_files):
        if exists(Arq[i]) and "Tags_match" not in Group[i]: #track.Grouping:
           print("\nTags Comparison",i+1,"of",len(Arq),":",Files.file_w_ext(Arq[i]))
           # DICIONARIOS PRECISAM SER INICIALIZADOS
           dict_app = {}
           dict_tiny = {}
           
           # PASSO O DICIONARIO PRINCIPAL PARA A FUNCAO
           # NOTE QUE DICT_MAIN NAO EH O MESMO TIPO DE DICIONARIO QUE DICT_ITUNES
           Reads_tags(Arq,i,dict_main,dict_app,dict_tiny)

           # eyed3_mism = dict_iTunes != dict_eyed3
           tiny_mism = dict_app != dict_tiny
           if tiny_mism:
              print("\nFile mismatches!",Arq[i])
              # ADICIONA NA LISTA GERAL DE MISMATCHES
              to_fix_dic['All'].append(i)
              # add track to PL if Tags MISMATCH
              if iTunes:
                 Read_PL.Add_file_to_PL(PLs,PL_Mismatch,Arq[i]) 
              
              # ADICIONA NA LISTA PROPRIA DA TAG QUE MISMATCH
              for key in dict_app.keys():
                  if dict_app[key] != dict_tiny[key]:
                     print("\n",key,"differs:",dict_app[key], "->", dict_tiny[key])
                  if dict_app[key] != dict_tiny[key] and dict_tiny[key] != '':
                     to_fix_dic[key].append(i)
              print("\n") 
        #    else:
        #       track = App.LibraryPlaylist.Tracks.ItemByPersistentID(*PID[i])
        #       New_Group = Tags.Add_to_tag(track,"Tags_mismatch",Tag="Group") 
              #Read_PL.Add_file_to_PL(PLs,Alrdy_srchd,Arq[i])

    # SAINDO DO LOOP   
    nbr_updt = len(to_fix_dic['All']) 
    print("\nFiles to have tags synced:",nbr_updt,"\n")
    
    # CHAMA A FUNCAO QUE CRIA PL PARA CADA TAG MISMATCH
    # CRIA PLAYLIST APENAS SE HOUVER ARQUIVOS EM CADA TAG ESPECIFICA
    if iTunes:
        for key in to_fix_dic.keys():
            nbr_updt_key = len(to_fix_dic[key])
            if nbr_updt_key>0:
               Tag_PL = Read_PL.Create_PL("Compara_"+key,recreate="Y")
               print(key,"that differ:",nbr_updt_key)

            for i in range(nbr_updt_key):
                n = to_fix_dic[key][i]
                if key != 'All':
                    print(i+1,"Arq",Arq[n],"->",key,"differs:",dict_main[key][n],"->",Files.read_tinytag(Arq[n],key))
                #Tag_PL.AddFile(Arq[n])
                # ADICIONA ARQUIVO Arq[n] A PLAYLIST "Comp_"+key
                Read_PL.Add_file_to_PL(PLs,"Comp_"+key,Arq[n])
            print("")    

    #res = input("Press Y to sync:")
    res = "Y"

    # START SYNC THE TAGS
    if res.lower() == 'y':
       fixed = {}
       for key in tags_comp_lst:
           fixed[key] = 0

       for i in range(nbr_updt):
           n = to_fix_dic['All'][i]
           print("\nFixing",i+1,"of",nbr_updt,":",Files.file_w_ext(Arq[n]))
           dict_tiny = Files.tag_dict(Arq[n],tags_comp_lst)
           if iTunes:
              track = App.LibraryPlaylist.Tracks.ItemByPersistentID(*PID[n])
              dict_app = Read_PL.iTunes_tag_dict(track,tags_comp_lst)
           else: 
               track = library[n]   
               dict_app = WMP.WMP_tag_dict(track,tags_comp_lst)

           for key in tags_comp_lst:
               if dict_app[key] != dict_tiny[key]:
                  fixed[key] = fixed[key]+1
                  print(fixed[key],"Rewriting",key,"// From",dict_app[key],"->",dict_tiny[key])

                  # UPDATE TAG
                  if iTunes:
                     # get the attribute name from the dictionary
                     attr_name = Read_PL.iTu_tag_dict[key]
                     # update the attribute value of the track object dynamically
                     setattr(track, attr_name, dict_app[key])
                  else:
                     # Get the attribute name from the dictionary
                     attr_name = WMP.tag_dict[key]
                     new_value = dict_tiny[key]
                     track.setItemInfo(attr_name, new_value)
        
       print("")
       for key in fixed.keys():
           print("Final:",fixed[key],key,"tags synced")

# CALLS FUNC
Comp(iTunes=False,rows=None)