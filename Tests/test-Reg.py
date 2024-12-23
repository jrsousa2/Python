from re import sub
#import re

test="test (11).MP3"
#test2= sub(" \(\d\)\.[mM][pP]3", ".mp3", test)
test2= sub(" \(\d+\)\.[mM][pP]3", ".mp3", test)
print(test2)

