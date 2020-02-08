import urllib
import magic, time
from eyed3 import id3
from urllib.request import urlopen
import os
#Audio, MPEG,
#JPG, JPEG, PNG, GIF
start = time.time()
url = "http://zmp3-mp3-s1-te-zmp3-fpthn-1.zadn.vn/4602587f513bb865e12a/4783556439703645280?key=ICbP4E63GGP-coiNZBLzHQ&expires=1497957582"
request = urllib.request.Request(url)
response = urlopen(request)
mime_type = magic.from_buffer(response.read(128))
print(mime_type)
tag = id3.Tag()
tag.parse('/home/nero/Download/Audio/77.mp3')
if tag.title == None:
    print (1)
#os.listdir('../Download/')
os.rename('/home/nero/Download/Audio/77.mp3', "/home/nero/Download/Audio/" + tag.title)
#print (tag.title)
print (time.time() - start)