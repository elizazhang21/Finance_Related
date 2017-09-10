__author__ = 'ElizabethZhang'
#Nasdaq:goog
# -*- coding: utf-8 -*-

import urllib
import pandas as pd
from urllib import request as rq
import datetime 
import time 
from bs4 import BeautifulSoup

from datetime import datetime

output = {}
bad_requests = []
#   headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}

ticker = 'GOOG'
url_string = 'https://www.google.com/finance/historical?q=NASDAQ:GOOG'

req = rq.Request(url_string)
page = rq.urlopen(req)
soup = BeautifulSoup(page.read(),'lxml')
    
date_list = []
close_list = []
volume_list = []

rows = soup.find('table', class_='gf-table historical_price').find_all('tr')

for row in rows:
    #skip head line which has class attribute
    if 'class' in row.attrs :
        continue
    
    close = row.find_all('td', class_='rgt')[3].contents[0]
    close = (float)(close.split('\n')[0].replace(',',''))
    close_list.append(close)
    
    volume = row.find_all('td', class_='rgt rm')[0].contents[0]
    volume = (int)(volume.split('\n')[0].replace(',',''))
    volume_list.append(volume)
    
    date = row.find_all('td', class_='lm')[0].contents[0]
    date = date.split('\n')[0]
    date = datetime.strptime(date, "%b %d, %Y").strftime("%Y-%m-%d")
    date_list.append(date)
    
df = pd.DataFrame({'Date':date_list, 'Close':close_list, 'Volume':volume_list}, columns=['Date','Close','Volume'])
print(df)