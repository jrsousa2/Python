import iptcinfo3, os, sys, random, string

# Random string gennerator
rnd = lambda length=3 : ''.join(random.choices(list(string.ascii_letters), k=length))
# Path to the file, open a IPTCInfo object
path = os.path.join(sys.path[0], 'DSC_7960.jpg')
path = "D:\MP3\Favorites\Neverest - About Us (1).mp3"
info = iptcinfo3.IPTCInfo(path)
# Show the keywords
print(info['keywords'])
# Add a keyword and save
info['keywords'] = [rnd()]
info.save()
# Remove the weird ghost file created after saving
os.remove(path + '~')