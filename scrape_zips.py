from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests, zipfile, io
import time
import re
import os

#You may need to change this path to match your chromedriver path
executable_path = {"executable_path": "chromedriver"}

URL = 'https://s3.amazonaws.com/tripdata/index.html'

#This is just the path this file is stored in. Should be run from parent folder containing your Resources folder.
FILE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Resources/site_csv_downloads')

#Excludes years up to param and only grabs hrefs that end in 'zip'
def get_regex(year = 2013):
    range = (year % 10)
    reg_ex = f"^(?!https://s3.amazonaws.com/tripdata/201[0-{range}]).+zip$"
    return reg_ex


def Get_Html():
    browser = Browser('chrome', **executable_path, headless=True)
    browser.visit(URL)
    time.sleep(2)
    html = browser.html
    browser.quit()
    return bs(html, 'html.parser')

soup = Get_Html()
a_list = soup.find_all("a", href=re.compile(get_regex(2017)))

count = int(0)
for a in a_list:
    href = a['href']
    r = requests.get(href)
    if(r.ok):
        count += 1
        print(">>>Downloading/Extracting Zips: " + str(int(round((count/len(a_list)) * 100))) + "%", end="\r", flush=True)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(FILE_PATH)
        z.close()

print(">>>Downloading/Extracting Zips: DONE")