# __Author__ = 'Elizabeth Zhang'
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.common import *
from ibapi.contract import *
import pandas as pd
import pandas_datareader as reader
import numpy as np

# ================================ Part 1 ===================================
# read input files
path = '/Users/Elizabeth.Ke.Zhang/Desktop/Oct/Germany_Equities.csv'

f = pd.read_csv(filepath_or_buffer=path, sep=',')
col_index = [f.columns[0], f.columns[4]]
df = f[col_index]
df.columns = ['Symbol', 'Exchange']
Tickers = np.asarray(df['Symbol'])
Exchanges = np.asarray(df['Exchange'])
print(Tickers, Exchanges)


# ================================ Part 2 ===================================
# Get access to IB
class TestApp(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        print('Error:', reqId, ' ', errorCode, ' ', errorString)

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        print('ContractDetails:', reqId, ' ', contractDetails)


def main():
    for i in range(1472):

        app = TestApp()

        app.connect('127.0.0.1', 7497, 0)
        contract = Contract()
        contract.symbol = Tickers[i]
        contract.exchange = Exchanges[i]
        contract.secType = "STK"
        contract.currency = 'EUR'
        contract.primaryExchange = Exchanges[i]
        app.reqContractDetails(i, contract)
        app.run()

if __name__ == '__main__':
    main()
