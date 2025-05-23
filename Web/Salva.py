import requests
import re

def getFilename_fromCd(cd):
# Get filename from content-disposition
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]


#url = 'http://google.com/favicon.ico'
url = "https://is4-ssl.mzstatic.com/image/thumb/Music114/v4/24/2a/94/242a9475-33ac-367a-f063-6785460e218f/source/625x625.jpg"
r = requests.get(url, allow_redirects=True)
filename = getFilename_fromCd(r.headers.get('content-disposition'))
filename = "D:\\Z-Covers\\Download_from_iTunes\\capa.jpg"
open(filename, 'wb').write(r.content)