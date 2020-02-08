from bs4 import BeautifulSoup as bs
import urllib3
import json

http = urllib3.PoolManager()
r = http.request('GET', "http://mp3.zing.vn/bai-hat/Dung-Ai-Nhac-Ve-Anh-Ay-Tra-My-Idol/ZW7FC0FB.html")
soup = bs(r.data, "lxml")
html = str(soup.find_all(lambda tag : (tag.name == 'div' and tag.get('class') == ['player'])))
print (html)
json_key = html[html.index('/json'):html.index('" id')]
url = 'http://mp3.zing.vn' + json_key
print (url)
json_r = http.request('GET', url)
print (json_r.data)
data = json.loads(json_r.data.decode())
print (data)
