from urldl.getlink import *
import urllib3, time, os
from sys import argv
from os.path import expanduser
from eyed3 import id3

def end_char(start_idx, string):
    for i in range(start_idx + 1, len(string)):
        asckey = ord(string[i])
        if (asckey < 48 or asckey > 122) or (asckey > 57 and asckey < 65):
            return i

def download_audio(urls, folder='/Audio/'):
    print ('Number of audio files selected : %i' % len(urls))
    print ('Downloading')
    audio_folder = download_folder + folder
    if os.path.exists(audio_folder) == False:
        os.mkdir(audio_folder)
    for url in urls:
        name = url[url.rfind('/'):end_char(url.rfind('/'), url)] + '.mp3'
        r = http.request('GET', url)
        file = open(audio_folder + name, 'wb')
        file.write(r.data)
        file.close()
        tag.parse(audio_folder + name)
        if tag.title != None:
            song_name = tag.title.encode('utf-8').decode('ascii', 'ignore').strip().replace('/', '')
            print (song_name)
            os.rename(audio_folder + name, audio_folder + song_name + '.mp3')
        print ('-', end="")
        time.sleep(0.05)
    print ('\nDone')

start = time.time()
home_dir = expanduser('~')
download_folder = home_dir + '/Download'
url = 'http://mp3.zing.vn/album/Nhung-Bai-Hat-Hay-Nhat-Cua-Trung-Quan-Idol-Trung-Quan-Idol/ZWZBIBBI.html'
if len(argv) == 3:
    scripts, url, download_folder = argv
elif len(argv) == 2:
    scripts, url = argv

if os.path.exists(download_folder) == False:
    os.mkdir(download_folder)
http = urllib3.PoolManager()
tag = id3.Tag()
audio_links = get_download_link(url, type=['audio'])
download_audio(audio_links, folder='/Trung Quan/')
print (time.time() - start)
