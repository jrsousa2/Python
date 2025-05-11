# SUBROUTINE CALLED BY OTHER CODES
import Tags
import Images


def Busca(print_head,i,main_dict,srch_by="title",nbr_searches=1):

    Arq = main_dict['Arq']
    Art = main_dict['Art']
    Title = main_dict['Title']
    AA = main_dict['AA']
    Album = main_dict['Album']
    Genre = main_dict['Genre']
    Year = main_dict['Year']

    kw = ""
    if srch_by=="title" and Art != '' and Title != '':
       kw = Art + " " + Title
       print(print_head,"Searching by title:",kw)
    elif srch_by=="file":
         file = Tags.File_no_nbr_no_ext(Arq)
         Art_Title = file.split(" - ")
         if len(Art_Title)==2:
            Art = Art_Title[0]
            Title = Art_Title[1]
            kw = file.replace(" - "," ")
            srch_by = "title"
            print(print_head,"Searching by filename (title):",kw)
         else:
            print(print_head,"Problem with by filename:",file)      
    elif AA != '' and Album != '':
       kw = AA + " " + Album
       print(i+1,"Searching by album:",kw)
    
    counts = {}
    dict_res = {}
    dict_res['Hits'] = False
    dict_res['RC'] = False
    dict_res['Achou'] = False
    
    if kw != '':
        counts['Searched'] = 1
        # tenta pegar erros:
        try:
            # dict is a LIST of dictionaries
            dict = []
            Images.get_cover(kw,nbr_searches,dict,srch_by)
        except Exception:
            print("Exception")
        else:
            print("No exception",dict[0]['N'],"results\n")
            # no results
            if dict[0]['N']==0:
               counts['No_result'] = 1
            
            # Check results   
            j=0
            while dict_res['RC']== False and j<dict[0]['N']:
                  # routine
                  dict_res['Art'] = dict[j].get('artistName',"")
                  dict_res['Title'] = dict[j].get('trackName',"")
                  dict_res['AA'] = dict[j].get('collectionArtistName',"")
                  dict_res['Album'] = dict[j].get('collectionName',"")
                  dict_res['Date'] = dict[j].get('releaseDate', "")
                  if dict_res['Date'] != '':
                     dict_res['Year'] = int(dict_res['Date'][0:4])
                  else:
                     dict_res['Year']=0

                  # standardizes VA album
                  if dict_res['AA'] == '' and dict_res['Album'] != '':
                     dict_res['AA'] = dict_res['Art']

                  if dict_res['AA'] != '':
                     if dict_res['AA'].lower().strip()=="various artists":
                        dict_res['AA'] = "Various"
                     elif dict_res['AA'].lower().strip()=="vários artistas":
                        dict_res['AA'] = "Várious"   

                  # Type of the match
                  # Counts by match type
                  if dict[j].get('wrapperType',"").lower() == 'track':
                     dict_res['wrapper'] = 'track'
                     counts['wrapper=track'] = 1
                  elif dict[j].get('wrapperType',"").lower()=='collection':
                        dict_res['wrapper'] = 'Album'
                        counts['wrapper=Album'] = 1
                  else:
                     dict_res['wrapper'] = 'None'
                     counts['wrapper=None'] = 1

                  # YES RESULTS
                  if (dict_res['Art'] != '' and dict_res['Title'] != '') or \
                     (dict_res['AA'] != '' and dict_res['Album'] != ''):
                     counts['Entries'] = 1
                     dict_res['Hits'] = True
                     # tags
                     std_art = Tags.Stdz(Art)
                     std_title = Tags.Stdz(Title)
                     std_art_title = Tags.Stdz(Art+" - "+Title)
                     
                     # searches
                     std_art_srch = Tags.Stdz(dict_res['Art'])
                     std_title_srch = Tags.Stdz(dict_res['Title'])
                     std_art_title_srch = Tags.Stdz(dict_res['Art']+" - "+dict_res['Title'])
                     
                     print(print_head,"-","match attempt",j+1,", search: engine=",dict_res['wrapper'],",code=",srch_by.title())
                     print("\tArt:",Art,"->",dict_res['Art'])
                     print("\tTitle:",Title,"->",dict_res['Title'])
                     # NAO MOSTRAR OS MATCH STD, SO PARA TROUBLESHOOTING
                     #print("\tArt stdz:",std_art,"->",std_art_srch)
                     #print("\tTitle stdz:",std_title,"->",std_title_srch,"\n")

                     Is_Brasil = Genre.lower().find("brasil")>=0
                     Is_Live = Genre.lower().find("live")>=0
                     if Is_Brasil:
                           Alb_ok = Is_Live == (dict_res['Album'].lower().find("vivo")>=0)
                     else:
                           Alb_ok = Is_Live == (dict_res['Album'].lower().find("live")>=0)

                     # Does the data match?
                     # Eh possivel que numa busca por title, a track nao bate mas o album sim
                     # isso aqui agiliza a busca (tomar cuidado se for search por varios)
                     match_title = (std_art==std_art_srch and std_title==std_title_srch)
                     match_title = match_title or (std_art_title == std_art_title_srch)
                     
                     # match on VA albums only if the Year also matches
                     match_album = False
                     if AA.strip() !='' and Album.strip() !='':
                           std_aa = Tags.Stdz(AA)
                           std_album = Tags.Stdz(Album)
                           std_aa_album = Tags.Stdz(AA+" - "+Album)
                           std_aa_srch = Tags.Stdz(dict_res['AA'])
                           std_album_srch = Tags.Stdz(dict_res['Album'])
                           std_aa_album_srch = Tags.Stdz(dict_res['AA']+" - "+dict_res['Album'])
                           # MOSTRAR SO PARA TROUBLESHOOTING
                           #print("\tArt+Title stdz:",std_art_title,"->",std_art_title_srch)
                           #print("\tAA+Album stdz:",std_aa_album,"->",std_aa_album_srch,"\n")

                           # Current and srch album  should match here anyway despite the names
                           great_hits = Tags.Greatest_Hits(Album)
                           Cur_alb_by_art = Tags.Alb_by_art(Art,AA,Title)
                           Srch_alb_by_art = Tags.Alb_by_art(dict_res['Art'],dict_res['AA'],dict_res['Title'])
                           
                           # creates album match flag
                           if not Cur_alb_by_art or not Srch_alb_by_art or great_hits:
                              match_album = std_art==std_art_srch and std_aa==std_aa_srch and std_album==std_album_srch and Year==dict_res['Year'] and Year !=0
                              match_album = match_album or (std_art==std_art_srch and std_aa_album == std_aa_album_srch and Year==dict_res['Year'] and Year !=0)
                           else:
                              match_album = (std_art==std_art_srch or std_aa==std_aa_srch) and std_album==std_album_srch
                              match_album = match_album or (std_aa_album == std_aa_album_srch)

                     # res['Match'] is the actual match
                     if match_title:
                        counts['Match_title'] = 1
                        dict_res['Match'] = "Title"
                     if match_album:
                        counts['Match_album'] = 1
                        dict_res['Match'] = "Album"
                     if match_title and match_album:
                        counts['Match_both'] = 1
                        dict_res['Match'] = "Title & Album"

                     match = match_title or match_album

                     # check if there was an accurate match
                     if  Alb_ok and match:
                           #stats[j+1] = stats[j+1]
                           dict_res['Achou'] = True
                           dict_res['Attempt'] = j+1
                           dict_res['RC'] = True
                           # a match was found
                           counts['Found'] = 1

                           # Prints confirmation
                           print("Found! At attemp",j+1,"! Matches on:",dict_res['Match']) 
                           print("Album:",AA,"-",Album,"->",dict_res['AA'],"-",dict_res['Album'],"\n")

                           dict_res['Genre'] = dict[j].get('primaryGenreName', "")
                           
                           dict_res['URL'] = dict[j].get('artworkUrl100', "")
                           if dict_res['URL'] != '':
                              size = 600
                              dict_res['URL'] = dict_res['URL'].replace('100x100bb', "%sx%s" % (size, size))
                  # Try next dictionary entry      
                  j=j+1   
        if len(dict)>0:
           counts['Json exc'] = dict[0].get('Json exc', 0)
    # result of the search 
    # Aux dict
    aux_dic = {'counts': counts, 'dict_res': dict_res}      
    return aux_dic