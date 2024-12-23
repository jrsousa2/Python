# THIS CODE IS A SUBROUTINE CALLED BY CALL_ART
# As covers sao salvas em:
# 1) covers_by_art: se mudou o album mas nao o AA
# 2) VA2Art: se mudou de VA para Alb_by_art
# 3) Caso contrario elas ficam em download_from_itunes (from Apple)

# ESSE CODE PRECISA SER REVISTA E FINALIZADA

import Tags
from os.path import exists
from os import rename, remove
from Images import hei, wid, Dwld_cover_Apple, Has_artwork, Save_cover_iTu

# Change type 1
iTu_detach_folder = "D:\\Z-Covers\\Replace_iTunes\\"
Apple_dwl_folder = "D:\\Z-Covers\\Replace_Apple\\"

# Change type 2
VA2Art_old_folder = "D:\\Z-Covers\\Replace_VA2Art_Old\\"
VA2Art_new_folder = "D:\\Z-Covers\\Replace_VA2Art_New\\"

# Change type 3
Any2Art_folder = "D:\\Z-Covers\\Replace_Any2Art\\"

# SE FOR UPGRADE E O ALBUM MUDAR, SALVAR EM UM DIRETORIO DIFERENTE
# Change type 4
VA2VA_upg_folder = "D:\\Z-Covers\\Replace_upg_VA2VA\\"

# Change type 5
# The difference of this folder to Any2Art_folder is that here
# there won't be same album upgrades
Art2Art_upg_folder = "D:\\Z-Covers\\Replace_upg_Art2Art\\"

# NAO TINHA COVER ANTES
No_prior_VA_folder = "D:\\Z-Covers\\Replace_No_Prior_VA\\"
No_prior_Art_folder = "D:\\Z-Covers\\Replace_No_Prior_Art\\"

# Tries to attach cover and change tags
# Nao aplicar essa rotina 
# busca eh um vetor contento algumas info
def Attach_cover(main_dict,busca,track,fixed,Year_updated):
    # main_dict is a dictionary of lists
    Arq = main_dict['Arq']
    Art = main_dict['Art']
    Title = main_dict['Title']

    ##############################################################
    # SEARCH APPLE SITE-remote  

    # busca is a dictionary
    # Srch_art = busca.get('Art','')
    Srch_AA = busca.get('AA','') 
    Srch_Album = busca.get('Album','') 
    Srch_Genre = busca.get('Genre','') 
    Srch_Yr_updt = Year_updated
    
    # Name of the cover file
    Srch_cover_file = Dwld_cover_Apple(Arq,busca,path=Apple_dwl_folder)
    
    Srch_has_cover = False
    Srch_cover_hei = 0
    Srch_cover_wid = 0
    if exists(Srch_cover_file):
       fixed['Downloaded'] = fixed['Downloaded']+1
       Srch_cover_hei = wid(Srch_cover_file)
       Srch_cover_wid = hei(Srch_cover_file)
       if Srch_cover_hei>200 and Srch_cover_wid>200:
          Srch_has_cover = True

    # RULES to attach cover Nice_cover(Album,Genre)
    # Blank pmt below is the genre (can't be novela, now, nice, etc.)
    Srch_res = Tags.Score(Art,Title,Srch_AA,Srch_Album,"",Srch_has_cover,Srch_cover_wid,Srch_cover_hei,Srch_Yr_updt)
    Srch_score = Srch_res['score']
    Srch_ratio = Srch_res['ratio']
    Srch_alb_not_miss = Srch_res['alb_not_miss']
    Srch_alb_by_art = Srch_res['alb_by_art']
    Srch_alb_not_nice = not Tags.Nice_cover(Srch_Album,Srch_Genre)

    ##############################################################
    # iTunes  
    Cur_AA = track.AlbumArtist
    Cur_Album = track.Album
    Cur_Genre = track.Genre
    Cur_Yr_updt = False

    Cur_has_cover = False
    Cur_cover_hei = 0 
    Cur_cover_wid = 0
    # check art
    Artwork_Ok = Has_artwork(track)
    if Artwork_Ok: # Fix this part WHICH HAS A BUG
       Cur_cover_file = Save_cover_iTu(track,iTu_detach_folder)
       if exists(Cur_cover_file):
              fixed['iTunes saved'] = fixed['iTunes saved']+1
              Cur_has_cover = True 
              Cur_cover_hei = wid(Cur_cover_file)
              Cur_cover_wid = hei(Cur_cover_file)
       else:
          fixed['iTunes save exc'] = fixed['iTunes save exc']+1

    # calls score function   
    Cur_res = Tags.Score(Art,Title,Cur_AA,Cur_Album,Cur_Genre,Cur_has_cover,Cur_cover_wid,Cur_cover_hei,Cur_Yr_updt)
    Cur_score = Cur_res['score']
    Cur_ratio = Cur_res['ratio'] 
    Cur_alb_not_miss = Cur_res['alb_not_miss']
    Cur_alb_by_art = Cur_res['alb_by_art']
    Cur_alb_not_nice = not Tags.Nice_cover(Cur_Album,Cur_Genre)


    ##############################################################
    # REST OF THE LOGIC
    # If to upgrade cover dimension, override Albs_eq
    Albs_eq = Tags.Stdz(Srch_AA+" - "+Srch_Album) == Tags.Stdz(Cur_AA+" - "+Cur_Album)
    if Albs_eq and not Cur_has_cover:
       Albs_eq = False # So I can attach the cover

    # Cover/image quality upgrade for EQUAL albums
    Srch_cover_upg = False
    if Albs_eq and Srch_has_cover and Cur_has_cover:
       Srch_cover_upg = True 
       Albs_eq = False
       Cur_alb_not_nice = True

    # Don't replace VA with another VA (unless min_dim<500) or Upgd
    VA_flag = Srch_has_cover
    if not Srch_alb_by_art and (not Cur_alb_by_art and Cur_has_cover):
       if (min(Cur_cover_hei,Cur_cover_wid)>=500 or not Srch_has_cover) and not Albs_eq:
           VA_flag = False

    # Don't replace Alb_by_art (even wo/ cover) with VA with cover! (for now)
    # Unless in the below cases
    # Upgrade of the cover because the albums are the same
    Cur_alb_has_no_art = not Cur_has_cover and Srch_has_cover and not Cur_alb_by_art
    Fazer = Srch_alb_by_art or Cur_alb_has_no_art
    if not Cur_alb_by_art and not Srch_alb_by_art:
       if Srch_cover_upg:
          Fazer = True

    # Upgrade for different albums
    # Exception for VA->VA Art->Art if dimensions are very low
    # HERE ALBUMS ARE NOT EQUAL, WHICH WOULD FALL INTO A SCENARIO ABOVE 
    diff_alb_upg = False
    if Srch_has_cover and Cur_has_cover:
       Ratio_comp = Cur_ratio<0.9 and Srch_ratio>0.9 and min(Srch_cover_hei,Srch_cover_wid)>=500
       Dim_comp = Cur_cover_hei<400 and Srch_cover_hei>=500
       if Srch_alb_by_art and Cur_alb_by_art and (Dim_comp or Ratio_comp):
          Srch_cover_upg = True
          Fazer = True
          diff_alb_upg = True
       if not Srch_alb_by_art and not Cur_alb_by_art and (Dim_comp or Ratio_comp):
          Srch_cover_upg = True 
          Fazer = True
          diff_alb_upg = True

    # Flag for result of the cover attachment
    Attached = False
    From = ""
    To = ""

    # Here I'm assuming that the srch cover will always exist (for now)
    # It's actually not bad to have tags wo/ having a cover
    if Srch_score>Cur_score and not Albs_eq and Cur_alb_not_nice and Fazer and VA_flag:
        # Try to change tags
        try:
            track.AlbumArtist = Srch_AA
            track.Album = Srch_Album 
        except Exception:
            print("Album update exception has occurred")
            fixed['Album upd exc'] = fixed['Album upd exc']+1
            #fixed['Attach exc']=fixed['Attach exc']+1
        else: 
            fixed['Album upd'] = fixed['Album upd']+1

            # updates the Genre
            New_genre = Tags.Handle_genre(track,"AlbumIsCorrect")
            if not Tags.Is_VA(Srch_AA) and not Srch_alb_by_art and New_genre !='':
               track.Genre = New_genre
               fixed['VA_flag']= fixed['VA_flag']+1 

            if exists(Srch_cover_file):
                #Art = Artobj.Item(1)
                if Cur_has_cover and exists(Cur_cover_file):
                   itu_Cover = track.Artwork.Item(1)
                   itu_Cover.Delete()
                   fixed['iTunes detach'] = fixed['iTunes detach']+1
                # TRY TO MODIFY THE ARTWORK 
                try:
                    track.AddArtworkFromFile(Srch_cover_file)
                except:
                    fixed['Attach exc']=fixed['Attach exc']+1
                    print("Attach exception has occurred")
                else:
                    fixed['Attached'] = fixed['Attached']+1
                    Attached = True

                # move files
                # if both have art (cur and srch), and cur is an alb by art (not VA), move both to Replaced_covers_by_art
                # if both have art (cur and srch), and cur is not an alb by art (VA), move new to Replace_VA2Art_new (not VA)
                # and old to Replace_VA2Art_old (VA)
                if Srch_has_cover and Cur_has_cover:
                   if diff_alb_upg:
                      if Srch_alb_by_art and Cur_alb_by_art:
                         Tags.Move_covers1(Srch_cover_file,Cur_cover_file,Art2Art_upg_folder)
                      else:
                          Tags.Move_covers1(Srch_cover_file,Cur_cover_file,VA2VA_upg_folder)
                   if not diff_alb_upg:
                      if Srch_alb_by_art:
                         Tags.Move_covers1(Srch_cover_file,Cur_cover_file,Any2Art_folder)
                      else: # This never had a hit (it will probably crash)
                          aux = {}
                          aux['AA1'] = Srch_AA
                          aux['Album1'] = Srch_Album
                          aux['cover1'] = Srch_cover_file
                          aux['AA2'] = Cur_AA
                          aux['Album2'] = Cur_Album
                          aux['cover2'] = Cur_cover_file
                          Tags.Move_covers2(Arq,VA2Art_new_folder,aux)
                elif Srch_has_cover:
                     if Srch_alb_by_art:
                        Tags.Move_covers(Srch_cover_file,No_prior_Art_folder)
                     else:
                         Tags.Move_covers(Srch_cover_file,No_prior_VA_folder)   
                # CUR     
                if Cur_alb_by_art:
                   From = "Art"  
                elif Cur_alb_not_miss:
                   From = "VA"
                else:
                   From = "Null"   
                # SRCH    
                if Srch_alb_by_art:
                   To = "Art"  
                elif Srch_alb_not_miss:
                   To = "VA"
                else:
                   To = "Null" 
    else:
        if Cur_has_cover and exists(Cur_cover_file):
           remove(Cur_cover_file)
           fixed['iTunes del'] = fixed['iTunes del']+1
        if Srch_has_cover and exists(Srch_cover_file):
           remove(Srch_cover_file)
           fixed['Apple del'] = fixed['Apple del']+1
    # Proxima faixa
    print("")
    aux_dic = {}
    aux_dic['Attached'] = Attached
    aux_dic['From'] = From
    aux_dic['To'] = To
    return aux_dic

