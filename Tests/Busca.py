import coverpy
import requests
import re

def Busca(kw,res):
    print("CoverPy console:")
    busca = coverpy.CoverPy()

    try:
        query = busca.get_cover(kw)
        res['RC'] = True
        res['Type'] = query.type
        res['Artist'] = query.artist
        res['Title'] = query.name
        res['Album'] = query.album
        res['URL'] = query.url
    except coverpy.exceptions.NoResultsException as e:
        res['RC'] = False

# SAVE THE FILE
# #url = 'http://google.com/favicon.ico'
url = "https://is4-ssl.mzstatic.com/image/thumb/Music114/v4/24/2a/94/242a9475-33ac-367a-f063-6785460e218f/source/625x625.jpg"
r = requests.get(url, allow_redirects=True)
filename = "D:\\Z-Covers\\Download_from_iTunes\\capa.jpg"
open(filename, 'wb').write(r.content)        