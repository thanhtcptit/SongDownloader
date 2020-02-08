import dryscrape
from bs4 import BeautifulSoup
session = dryscrape.Session()
session.visit('http://mp3.zing.vn/bai-hat/Dung-Ai-Nhac-Ve-Anh-Ay-Tra-My-Idol/ZW7FC0FB.html')
response = session.body()
soup = BeautifulSoup(response)
print (soup.prettify())