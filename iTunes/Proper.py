# SUBROUTINE CALLED BY CALL_PROPER
#FUNCAO PARA ARRUMAR O CASO DAS TAGS
# ESSA FUNCAO PODE PRECISAR DE MAIS DE UMA EXECUCAO PARA SUBSTITUIR CORRETAMENTE
# E.G. fabio -> Fabio -> Fábio

import re

# VARIOUS ARTISTS
VA=["vários","various","various","varios"]

#DICTIONARY
# NAO PRECISA DE ESPACO NAS KW, ESSE ESPACO JA EH CONSIDERADO NA LOGICA (REPLACE)
Kw = {}
Kw['Dj']='DJ'
Kw['D.j.']='DJ'
Kw['Mr']='Mr.'
Kw['Ub40']='UB40'
Kw['Jr']='Jr.'
Kw['Dr']='Dr.'
Kw['Ac/Dc']='AC/DC'
Kw['AC\DC']='AC/DC'
Kw['Ac\Dc']='AC/DC'
Kw['Ii']='II'
Kw['Iii']='III'
Kw['Lil']="Lil'"
Kw['Uk']='UK'
Kw['Lmfao']='LMFAO'
Kw['Nao']='Não'
Kw['Voce']='Você'
Kw['Legiao']='Legião'
Kw['Coracao']='Coração'
Kw['Coraçao']='Coração'
Kw['Acustico']='Acústico'
Kw['Mtv']='MTV'
Kw['Fabio']='Fábio'
Kw['Sao']='São'
Kw['Varios']='Vários'
Kw['Sr']='Sr.'
Kw['Ze Ramalho']='Zé Ramalho'
Kw['Feat']='Feat.'
Kw['Ft']='Feat.'
Kw['Ft.']='Feat.'
Kw['ft.']='Feat.'
Kw['Tupac']='2Pac'
Kw['Vs']='Vs.'
Kw['vs']='Vs.'
Kw['Bpm']='BPM'
Kw['Rpm']='RPM'
Kw['Omd']='OMD'
Kw['Dmc']='DMC'
Kw['`']="'"
Kw['Dont']="Don't"
Kw['Jay-z']="Jay-Z"
Kw['.mp3']='.mp3'
Kw['.Mp3']='.mp3'
Kw['Joao']='João'
Kw['Hip-hop']='Hip-Hop'
Kw['IPhone']='iPhone'
Kw['R&b']='R&B'
Kw['RnB']='R&B'
Kw['Xororo'] = 'Xororó'
#Kw['Drum & Bass']='D&B'
Kw["12''"]="12 Inch"
Kw["7''"]="7 Inch"

#for key in Kw:
    #print("Key",key,"=",Kw[key])

# USADO NA LOGICA
spec_char="("
num_spec_chars=1

# BEGINNING THE LOGIC OF REPLACEMENTS
def Proper(Str,Tag="art"):
    New_str = ""
    if Str != "":    
       # BELOW REMOVES DUPE SPACES 
       Aux_str=re.sub(' +', ' ',Str)
       Aux_str=" " + Aux_str.strip() + " " #REMOVES LEADING AND TRAILING SPACES
       Aux_str=Aux_str.replace("("," ( ")
       Aux_str=Aux_str.replace(")"," ) ")
       # KEYWORD REPLACEMENT
       for key in Kw:
           Aux_str = Aux_str.replace(" "+key+" "," "+Kw[key]+" ") 
       if Tag.lower()=="aa":
          Aux_str = Aux_str.replace(" Volume "," Vol. ")      
       # REMOVING DUPE SPACES AGAIN */
       Aux_str = re.sub(' +', ' ',Aux_str)
       Aux_str = Aux_str.strip()
        
       # NESSA LOGICA EU VOU PALAVRA POR PALAVRA E UPCASE A 1a LETRA
       # Note que Aux eh usado, mas a subs eh feita em New
       # Abaixo cria lista de palavras separando palavras por SPACE
       if Tag.lower() == "genre":
           words = Aux_str.split("\\")
           sep = "\\"
       else:
           words = Aux_str.split()    
           sep = " "

       for j in range(0,len(words)):
           word = words[j]
           if word != '':
              if word[0] != word[0].upper() and word not in Kw.values():
                 words[j] = words[j][0].upper()+words[j][1:]

       # CONCATENA TODAS AS LETRAS DA LISTA SEM ESPACO
       New_str = sep.join(words) 

        # FIX THE SPEC CHARS NOW: "(","[" */
       New_str=New_str.replace(" ( "," (")
       New_str=New_str.replace(" )",")")
       New_str=re.sub(' +', ' ',New_str) # REMOVE DUPE SPACES
       New_str=New_str.strip() #LEADING/TRIL SPACES
       #if New_str[0:1]==" (":
       #   New_str=New_str[1:] 

        # CORRIGE UM SPACE NO INICIO DA PALAVRA
       if New_str[0:2]=="( ":
          New_str="("+New_str[2:]
           #New_str=New_str.strip()

        # REPLACING SQUARE BRACKETS
       if Tag.lower() in ("art","title","file"):
          New_str=New_str.replace("[","(")
          New_str=New_str.replace("]",")")
          New_str=re.sub(' +', ' ',New_str) # Remove duplicated blanks
          New_str=New_str.strip()

        # Essa daqui nao deve mais ser necessario
       if Tag.lower()=="file":
          New_str.replace(" .mp3",".mp3")

    return New_str

# CHAMA A FUNCAO
#print("Func:",Proper("  Dj likE a (  sTone ) Fabio ft Julia","Art"),":")