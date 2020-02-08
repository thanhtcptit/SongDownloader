from selenium import webdriver
from xvfbwrapper import Xvfb
import re
import urllib, magic
from urllib.request import urlopen

def find_all_ss(patern, string):
    return [m.start() for m in re.finditer(patern, string)]

def end_index(from_idx, string, semicolon=None):
    if string[from_idx - 1] == '(':
        end_idx = ')'
    elif string[from_idx - 1] == '{':
        end_idx = '}'
    elif string[from_idx - 1] == '[':
        end_idx = ']'
    else:
        end_idx = string[from_idx - 1]
    if semicolon == True:
        end_idx = '\"'

    for i in range(from_idx + 1, len(string)):
        if string[i] == end_idx:
            return i

def get_domain(url):
    tmp_idx = find_all_ss('/', url)
    if url.find('http') >= 0:
        domain = url[:tmp_idx[2]]
    else:
        domain = url[:tmp_idx[0]]
    return domain

def is_downloadable_url(url):
    if len(url) < 40:
        return False
    if url.find('.html') >= 0 or url.find('.css') >= 0 or url.find('.js') >= 0:
        return False
    return True

def get_http_link(html):
    http_idxs = find_all_ss('http://', html) + find_all_ss('https://', html)
    http_links = []
    for i in http_idxs:
        link = html[i: end_index(i, html)]
        if is_downloadable_url(link) == False:
            continue
        if link.find('amp;') >= 0:
            amp_idx = link.index('amp;')
            link = link[0:amp_idx] + link[amp_idx + 4:]
        http_links.append(link)
    return http_links

def get_json_container(domain, html):
    json_idxs = find_all_ss('/json', html)
    json_links = []
    for i in json_idxs:
        json_links.append(domain + html[i:end_index(i, html, True)])
    return json_links

def get_http_from_json(json_links):
    http_links = []
    for json in json_links:
        driver.get(json)
        content = driver.page_source
        http_links = http_links + get_http_link(content)

    return http_links

def get_links_from_url(url):
    domain = get_domain(url)
    print('Send request')
    driver.get(url)
    htmlSource = driver.page_source
    print('Get http links')
    https_links = get_http_link(htmlSource)
    json_links = get_json_container(domain, htmlSource)
    https_links = https_links + get_http_from_json(json_links)
    display.stop()
    driver.quit()
    return https_links

def get_mime_types(https_link, type):
    image = type.__contains__('image')
    mime_types = {}
    print("Number of URL: %i" % len(https_link))

    for url in https_link:
        if image == False:
            if url.find('.jpg') >=0 or url.find('.png') >=0 or url.find('.jpeg') >=0 or url.find('.gif') >= 0:
                continue
        try:
            request = urllib.request.Request(url)
            response = urlopen(request, timeout=1)
            mime_type = magic.from_buffer(response.read(10))
            mime_types[url] = mime_type
        except Exception as e:
            continue

    return mime_types

def get_file_type(https_link, type):
    audio_links = {}
    img_links = {}
    video_links = {}
    mime_types = get_mime_types(https_link, type)

    for url, mtype in mime_types.items():
        if mtype.find('ID3') >= 0:
            audio_links[url] = 'mp3'
        elif mtype.find('JPEG') >= 0 or mtype.find('JPG') >= 0:
            img_links[url] = 'jpg'
        elif mtype.find('PNG') >= 0:
            img_links[url] = 'png'
        elif mtype.find('GIF') >= 0:
            img_links[url] = 'gif'
    print ("Audio files : %i" % len(audio_links))
    print ("Image files : %i" % len(img_links))
    print (img_links)
    return audio_links

def get_download_link(url, type=['image', 'audio', 'video', 'other']):
    https_link = get_links_from_url(url)
    return get_file_type(https_link, type)


print ("Initialize driver")
display = Xvfb()
display.start()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(chrome_options=chrome_options)

