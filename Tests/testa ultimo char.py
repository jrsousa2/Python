#import re

url = "a625x625.jpg"
print(url[url.rfind("."):])

path = "d:\\mp3\\a625x625.jpg"
path = path[path.rfind("\\")+1:]
path = path[:path.rfind(".")]
print(path)