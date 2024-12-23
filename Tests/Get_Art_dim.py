# THIS IS A TEST ONLY TO DETECT IMAGE DIMENSIONS
import stagger, io #traceback
from PIL import Image

def Img_dim(arq):
    dic = {}
    try:
        mp3 = stagger.read_tag(arq)
        im = Image.open(io.BytesIO(mp3[stagger.id3.APIC][0].data))
        # im.save("cover.jpg") # save cover to file
    except:
        dic['ok'] = False
        #print(traceback.format_exc())
    else:
        hei = im.size[0]
        wid = im.size[1]
        dic['ok'] = True
        dic['hei'] = hei
        dic['wid'] = wid
    return dic

#arq = "D:\MP3\Favorites\Debbie Harry - French Kissin' In The USA.mp3"
#v = Img_dim(arq)
#if v['ok']:
#   print(v)