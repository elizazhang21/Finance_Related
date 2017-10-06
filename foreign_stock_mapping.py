import pandas as pd
import pandas_datareader as reader
import datetime as dt

start = dt.datetime(2017, 9, 1)
end = dt.datetime(2017, 10, 1)

aapl = reader.get_data_yahoo('AAPL', start, end)
print(aapl)


f = reader.data.DataReader('F', 'google', start, end)
f = f.ix['2017-09-27']


file = 'Foreign_Equity_Mapping.csv'
p = pd.read_csv(filepath_or_buffer=file, sep=',')
print(p)
