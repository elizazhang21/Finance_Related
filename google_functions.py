#__author__ = 'Elizabeth Zhang'

# this file is written for mainly getting intraday data of given stocks from local excel file
# on google finance and then output them back to the excel file
# last modified in Oct 2017 by Elizabeth


import openpyxl
import datetime
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import time
import numpy
import os
import sys

# the core function of getting intraday data 1 min close price from google
# at one point


def getting_intraday_stock_data_at_one_point(date1, Ticker):
    # date1 is a datetime object which contains date and time
    # if date1 is 9:35:04 then return the close price for 9:36:00
    # if date1 is 9:45:00 then return the close price for 9:35:00
    # the function will return 1 min close price exactly one minute after
    # the given time

    # the Google finance url to get data, for intraday data it can only get past 15 business day
    # http://www.networkerror.org/component/content/article/1-technical-wootness/44-googles-undocumented-finance-api.html
    """
    q - Stock symbol
    x - Stock exchange symbol on which stock is traded (ex: NASD)
    i - Interval size in seconds (86400 = 1 day intervals)
    p - Period. (A number followed by a "d" or "Y", eg. Days or years. Ex: 40Y = 40 years.)
    f - What data do you want? d (date - timestamp/interval, c - close, v - volume, etc...) Note: Column order may not match what you specify here
    """
    url = 'https://finance.google.com/finance/getprices?i=60&p=15d&f=d,c&df=cpct&q='+Ticker
    # reading the url, using exception control to reconnect to url
    try:
        html = urlopen(url).read()
    except URLError:
        return 'No data'
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print(('Reason: ', e.reason))
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        pause()
        try:
            html = urlopen(url).read()
        except URLError as e:
            if hasattr(e, 'reason'):
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
            pause()
            html = urlopen(url).read()
    # if the data is successfully read, it's a long string, so splitline()
    datalist = html.splitlines()
    # please refer to https://www.google.com/finance/getprices?i=60&p=1M&f=d,c&df=cpct&q=ROP
    # to see detail data format

    # line 8 starts to show the data needed
    if len(datalist) > 7:
        for i in range(7, len(datalist)):
            date_from_google = datalist[i].split(',')[0]
            # that means a unix time stamp started with the letter 'a', i.e. 'a123557546'
            # to transfer a unix time stamp to regular date time, google unix
            # time stamp converter
            if (date_from_google[0] == 'a'):
                # print date_from_google
                # message started from 'a' is Unix time stamp
                unix_timestamp = int(date_from_google[1:])
                # translate unix time stamp to normal date
                date_from_google_modified = datetime.datetime.fromtimestamp(
                    int(date_from_google[1:]))
                # we only need the date same as given date
                if (date_from_google_modified.date() == date1.date()):
                    # i is recorded as the given date
                    # print date_from_google_modified.date()
                    break

        # since google finance intraday one minute data may be missing in one possible minute
        # so to get close to input date time with comparing to Unix stamp
        inputtime_price = float('NaN')
        # to convert date1 into unix time stamp
        date1_timestamp = time.mktime(date1.timetuple())
        for j in range(i+1, len(datalist)):
            # loop over every available minute on the date
            # unix time stamp unit is 1 sec, so the time will be the minute
            # times 60
            curr_time = unix_timestamp + int(datalist[j].split(',')[0])*60

            # find the first price that its time pass the given time
            if (curr_time+1 > date1_timestamp):
                # get the price and return
                inputtime_price = datalist[j].split(',')[1]
                break
    else:
        return float('NaN')
    return inputtime_price


def getting_intraday_stock_data_range_avg(date1, date2, Ticker):
    # get intraday data for the given Ticker within the given time range between the datetime
    # date1 and date2, they must be the same date
    if (date1 > date2):
        print('Wrong range time input! Exit!')
        sys.exit(1)

    url = 'https://finance.google.com/finance/getprices?i=60&p=15&f=d,c&df=cpct&q='+Ticker
    # reading the url
    try:
        html = urlopen(url).read()
    except URLError as e:
        return 'No data'
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        pause()
        try:
            html = urlopen(url).read()
        except URLError as e:
            if hasattr(e, 'reason'):
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
            pause()
            html = urlopen(url).read()
    # start to find given date's are the same with the date in the data
    datalist = html.splitlines()

    if len(datalist) > 7:
        for i in range(7, len(datalist)):
            date_from_google = datalist[i].split(',')[0]
            if (date_from_google[0] == 'a'):
                # print date_from_google
                # message started from 'a' is Unix time stamp
                unix_timestamp = int(date_from_google[1:])
                # translate unix time stamp to normal date
                date_from_google_modified = datetime.datetime.fromtimestamp(
                    int(date_from_google[1:]))
                # we only need the date same as start date
                if (date_from_google_modified.date() == date1.date()):
                    # print date_from_google_modified.date()
                    break

        # since google finance intraday one minute data may be missing in one possible minute
        # so to get close to input date time with comparing to Unix stamp
        inputtime_price = float('NaN')
        date1_timestamp = time.mktime(date1.timetuple())
        date2_timestamp = time.mktime(date2.timetuple())
        range_price = []

        # this will be the index of i in the previious for loop.
        break_index = i
        # started from the date we found
        for j in range(break_index+1, len(datalist)):
            # loop over every available minute on the date
            curr_time = unix_timestamp + int(datalist[j].split(',')[0])*60

            # insert from the first price that its time pass the given time
            if (curr_time+1 > date1_timestamp):
                try:
                    range_price.append(float(datalist[j].split(',')[1]))
                except:
                    return float('NaN')
            if (curr_time+1 > date2_timestamp):
                try:
                    inputtime_price = numpy.mean(range_price)
                except:
                    inputtime_price = float('NaN')
                break

    else:
        return float('NaN')
    return inputtime_price

# in case url of google don't work


def rest():
    xlxoutput = openpyxl.Workbook()
    sheetoutput = xlxoutput.active
    resttime = 1
    time.sleep(resttime)


def pause():
    print(time.localtime())
    rest()
    print(time.localtime())
