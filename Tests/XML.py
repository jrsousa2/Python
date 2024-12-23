import pandas as pd
import xml.etree.ElementTree as ET ## XML parsing
from os.path import exists
import Cria_PL

Cria_PL.Cria_PL("Move_files")

# NOME DO ARQUIVO DA BIBILIOTECA DO ITUNES
#lib = r'C:\Users\JR Sousa\Music\iTunes\iTunes Music Library.xml'
lib = r'D:\iTunes\Playlist.xml'

# LE O ARQUIVO ESPECIFICADO
tree = ET.parse(lib)
root = tree.getroot()
main_dict=root.findall('dict')
for item in list(main_dict[0]):    
    if item.tag=="dict":
        tracks_dict=item
        break
tracklist=list(tracks_dict.findall('dict'))

# MOSTRA PARTE DA LISTA
L = list(tracklist[0])
#print(L,"tamanho",L.__len__)
#for it in L:
    #print("Element",L.index(it),"is",it)

# DEF. LISTA DAS tracks
tracks = []

# CRIA LISTA COM AS 5 MUSICAS
c = 0 
for item in tracklist:
    x = list(item)
    print("Elemento eh", x[0], "Tamanho do elemento eh", len(x))
    c=c+1
    tracks.append(list(item))
    #for i in range(len(x)):
            
# IMPRIME SOME ELEMENTOS
print ("Contagem:",c)
print ("Number of tracks under tracks:",str(len(tracks)))

#FUNCAO ABAIXO VAI RETORNAR AS COLUNAS DO ARQUIVO
def cols(kind):
    cols=[]
    for i in range(len(kind)):
        for j in range(len(kind[i])):
            if kind[i][j].tag=="key":
                cols.append(kind[i][j].text)
    return set(cols)

# CHAMA A FUNCAO
tracks_cols=cols(tracks)
print("Cols:",tracks_cols)

# TRANSFORMA EM DATAFRAME COM PANDAS
def df_creation(kind,cols):
    df=pd.DataFrame(columns=cols)
    dict1={}
    for i in range(len(kind)):
        for j in range(len(kind[i])):
            if kind[i][j].tag=="key":
                dict1[kind[i][j].text]=kind[i][j+1].text
        list_values=[i for i in dict1.values()]
        list_keys=[j for j in dict1.keys()]
        df_temp=pd.DataFrame([list_values],columns=list_keys)
        df = pd.concat([df,df_temp],axis=0,ignore_index=True,sort=True)
    return df

# CHAMA A FUNCAO    
df_tracks = df_creation(tracks,tracks_cols)

# IMPRIME (ISSO AQUI NAO TA FUNCIONANDO)
# df_tracks.head()

# PRINT NUMBER OF ROWS
print("Number of recs",len(df_tracks.index),"number of cols",len(df_tracks.columns),"\n")

# COLS. SELECIONADAS
cols_to_sel=['Album','Album Artist','Artist','Artwork Count','Bit Rate','Genre','Grouping',
'Location','Name','Rating','Size','Total Time','Track ID','Year']

# CRIA UMA SUBSET DO ARQ ORIGINAL/RESTRINGE AS COLS.
df_tracks=df_tracks.loc[:,cols_to_sel]

print("INFO SOBRE O ARQ modificado \n")
print(df_tracks.info())

#print("INFO SOBRE O ARQ ORIGINAL\n")
# print("\n")
#print(df_tracks.info())

print("TESTA FUNCOES DE PANDA")
# SUMMARY STATISTICS
print("Test1")
print(df_tracks['Year'].value_counts)
print("\n")
print("Test2",df_tracks['Album'].count())
print("Test3",df_tracks['Album'].nunique())
print("Test4",df_tracks['Album'].unique()) #Lista os valores distintos

#LISTA OS FULLNAMES DOS ARQUIVOS
L=list(df_tracks['Location'].unique())
print("Arquivos distintos,",len(L),",sao:",L)

# IMPRIME ARQUIVOS UM A UM
for arq in L:
    arq2=arq.replace("file://localhost/","")
    arq2=arq2.replace("%20"," ")
    #arq2=arq2.replace("/","\\")
    print("Arq",L.index(arq)+1,"is",arq2)
    print("File exists:",exists(arq2))