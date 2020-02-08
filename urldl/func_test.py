#from urldl.getlink import get_link_from_url
import time, os, re
from os.path import expanduser
from sys import platform
from sklearn.naive_bayes import GaussianNB
import requests, time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from xvfbwrapper import Xvfb

display = Xvfb()
display.start()
driver = webdriver.Firefox()

session = requests.session()
adapter = requests.adapters.HTTPAdapter(max_retries=20)
session.mount('http://', adapter)

try:
    with open('/home/nero/py/ArticleClassify/Data/html_list/Khác', 'r') as f:
        for line in f:
            print(line)
            driver.get(line)
            html = driver.page_source
            soup = bs(html).find_all('p')
            print(soup)
            time.sleep(0.5)
finally:
    display.stop()
    driver.quit()

