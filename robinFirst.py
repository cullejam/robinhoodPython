import robin_stocks as r
import requests
import json
import time
import numpy as np

login = r.login('username', 'password')

def currentStocks():
	my_stocks = r.build_holdings()
	for key,value in my_stocks.items():
		print(key, value)



def getOptions():
	optionData = r.find_options_for_list_of_stocks_by_expiration_date(['fb','aapl','tsla','BTC'],
		expirationDate='2020-05-17',optionType='call')
	for item in optionData:
		print(' price -',item['strick_price'],' exp -',item['expiration_date'],' symbol - ',
			item['chain_symbol'],' delta - ',item['delta'],' theta - ',item['theta'])

def getPriceBitcoin():
	return r.crypto.get_crypto_quote('BTC', 'ask_price')

start = time.time()
bitcoinPrice = np.array([])
for x in range(100):
	price = getPriceBitcoin()
	bitcoinPrice = np.append(bitcoinPrice, [price])


print(time.time() - start)
print(bitcoinPrice, getPriceBitcoin())
#currentStocks()

#114,563
#getOptions()

#plan:
#1. buy
#2. if over x% sell immediatly
