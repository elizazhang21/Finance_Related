__author__ = 'ElizabethZhang'
#Nasdaq:goog
# -*- coding: utf-8 -*-

import urllib
import pandas as pd
from urllib import request as rq
import datetime 
import time 
from bs4 import BeautifulSoup

output_file = '/Users/Elizabeth.Ke.Zhang/Desktop/goog.csv'

output = {}
bad_requests = []
#   headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}

ticker = 'GOOG'
url_string = 'https://www.google.com/finance/historical?q=NASDAQ:GOOG'


print(ticker)
req = rq.Request(url_string)
page = rq.urlopen(req)
soup = BeautifulSoup(page.read(),'lxml')
date_list = []
volume_list = []
close_list = []

for i in range(10):
    #print(ticker)
    close = soup.find_all('td', class_='rgt')[5*i+3].contents[0]
    close = close.split('\n')[0]
    close_list.append(close)
    volume = soup.find_all('td',class_='rgt rm')[i].contents[0]
    volume = int(volume.split('\n')[0].replace(',',''))
    volume_list.append(volume)
    date = soup.find_all('td',class_='lm')[i].contents[0]
    date = date.split('\n')[0]
    date_list.append(date)

s = pd.DataFrame({'Date' : date_list,'Close':close_list,'Volume': volume_list}, columns=['Date','Close','Volume'])
print(s)
s.to_csv(output_file)