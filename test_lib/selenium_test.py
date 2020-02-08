from selenium import webdriver
from bs4 import BeautifulSoup as bs
from xvfbwrapper import Xvfb
import urllib3
import json

http = urllib3.PoolManager()
display = Xvfb()
display.start()
option = webdriver.FirefoxProfile()
option.set_preference('media.volume_scale', '0.0')
driver = webdriver.Firefox(firefox_profile=option)
'''
driver.get('http://mp3.zing.vn/album/Giong-Hat-Moi-Various-Artists/ZOUWWOOO.html')
htmlSource = driver.page_source
soup = bs(htmlSource, "lxml")

json_link = str(soup.find_all(lambda tag : (tag.name == 'div' and tag.get('class') == ['player'])))
print (json_link)
data = json.loads('http://mp3.zing.vn/album/Giong-Hat-Moi-Various-Artists/ZOUWWOOO.html')
print (data)

file_src = str(soup.find_all(lambda tag: tag.name == 'audio'))
file_src = file_src[file_src.index('http'):file_src.index('\">')]
file_src = file_src[0:file_src.index('amp;')] + file_src[file_src.index('amp;') + 4:]
print (file_src)
'''
r = http.request('GET', 'http://zmp3-mp3-s1-tr.zadn.vn/ddedab8173c59a9bc3d4/3052678397498305190?key=FmYFTM_oGYmvXXVIRYhbUQ&expires=1497757130')
#print (r.data)
file = open('raw.mp3', 'wb')
file.write(r.data)
file.close()

