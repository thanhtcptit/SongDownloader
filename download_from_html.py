from selenium import webdriver
from bs4 import BeautifulSoup as bs
from xvfbwrapper import Xvfb
import urllib3, json, re, time
from sys import argv

def find_all_ss(patern, string):
    return [m.start() for m in re.finditer(patern, string)]

def json_link_fliter(string):
    json_idx = string.find('/json')
    link_len = 46
    if string.find('playlist') > 0:
        link_len = 59
    json = string[json_idx:json_idx + link_len]
    return url_website + json

def get_names_artists(string):
    names = []
    artists = []
    name_start_idxs = find_all_ss('name', string)
    artists_start_idxs = find_all_ss('\"artist', string)
    artists_end_idxs = find_all_ss('\"link', string)
    for ni, asi, aei in zip(name_start_idxs, artists_start_idxs, artists_end_idxs):
        song_name = string[ni + 7:asi - 2]
        artist_name = string[asi + 10:aei - 2]
        names.append(song_name)
        artists.append(artist_name)
    return names, artists

def get_server_link(string):
    server_link = []
    json = json_link_fliter(string)
    driver.get(json)
    html = driver.page_source
    info = get_names_artists(html)
    start_idxs = [i + 15 for i in find_all_ss('source_list', html)]
    end_idxs = [i - 7 for i in find_all_ss('source_base', html)]
    print ('Get server link..')
    for s, e in zip(start_idxs, end_idxs):
        link = html[s:e]
        amp_idx = link.index('amp;')
        link = link[0:amp_idx] + link[amp_idx + 4:]
        server_link.append(link)
    return server_link, info

def download_item(server_container):
    server_links, info = server_container
    names, artists = info
    print ('Downloading...')
    for i, link, name, artist in zip(range(len(server_links)), server_links, names, artists):
        r = http.request('GET', link)
        file = open(download_folder + '%s.mp3' % (name + ' - ' + artist), 'wb')
        file.write(r.data)
        file.close()
        time.sleep(0.5)

http = urllib3.PoolManager()
display = Xvfb()
display.start()

if len(argv) == 2:
    script, url = argv
    download_folder = '~/py/DownloadTool/Download/'
elif len(argv) == 3:
    script, url, download_folder = argv
tmp_idx = find_all_ss('/', url)
url_website = url[:tmp_idx[2]]
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(chrome_options=chrome_options)
print ('Send request.')
driver.get('http://mp3.zing.vn/album/Tuyen-Tap-Cac-Bai-Hat-Hay-Nhat-Cua-Linkin-Park-Linkin-Park/ZWZAFAWF.html')
htmlSource = driver.page_source
soup = bs(htmlSource, "lxml")
json_html = str(soup.find_all(lambda tag : (tag.name == 'div' and tag.get('class') == ['player'])))
server_container = get_server_link(json_html)
download_item(server_container)

display.stop()
driver.quit()
print ("Finish")