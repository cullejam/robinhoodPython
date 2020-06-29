import robin_stocks as r
import requests
import json
import time
import numpy as np

login = r.login('username', 'password')
#these will go together
priceArray = np.array([])
nameArray = np.array([])
priceArrayCurrent = np.array([])
nameArrayCurrent = np.array([])


def currentStocks(price, name):
	my_stocks = r.build_holdings()
	for key,value in my_stocks.items():
		price = np.append(price, value['price'])
		name = np.append(name, key)
		print(key, value['price'])
	return(price, name)

def maxMinSwap(priceOriginal, priceCurrent, nameOriginal, nameCurrent):
	maxName, minName = mostChanged(priceOriginal, priceCurrent, nameOriginal, nameCurrent)
	SHARES_BUY = 1
	SHARES_SELL = 1
	r.orders.order_sell_market(maxName, SHARES_SELL)
	r.orders.order_buy_market(minName, SHARES_BUY)
	return minName, maxName

def mostChanged(priceOriginal, priceCurrent, nameOriginal, nameCurrent):
	nameOriginal, priceOriginal = editSize(priceOriginal, priceCurrent, nameOriginal, nameCurrent)
	currentMaxPercent = -10000
	currentMaxStock = ''
	priceCurrent = priceCurrent.astype(np.float)
	priceOriginal = priceOriginal.astype(np.float)
	for x in range(priceOriginal.size):
		if(((priceCurrent[x]-priceOriginal[x])/priceOriginal[x]) > currentMaxPercent):
			currentMaxPercent = ((priceCurrent[x]-priceOriginal[x])/priceOriginal[x])
			currentMaxStock = nameCurrent[x]

	currentMinPercent = 10000
	currentMinStock = ''
	for y in range(priceOriginal.size):
		if(((priceCurrent[x]-priceOriginal[x])/priceOriginal[x]) < currentMinPercent):
			currentMinPercent = ((priceCurrent[x]-priceOriginal[x])/priceOriginal[x])
			currentMinStock = nameCurrent[x]
	return (currentMaxStock, currentMinStock)

def editSize(priceOriginal, priceCurrent, nameOriginal, nameCurrent):
	if(nameOriginal.size == nameCurrent.size):
		return(nameOriginal, priceOriginal)
	else:
		for x in range(nameOriginal.size):
			exists = existsInArray(nameOriginal[x], nameCurrent)
			if(exists == False):
				nameOriginal = np.delete(nameOriginal, x)
				priceOriginal = np.delete(priceOriginal, x)
	return(nameOriginal, priceOriginal)

def existsInArray(name, nameCurrent):
	return(name in nameCurrent)

#test for mostChanged function
#print(mostChanged(np.array([1,2,3,4,5,6]),np.array([5,4,3,2,1]), np.array(['BTC','ETH','ROB','FCB','DDM','ASD']), np.array(['BTC','ETH','ROB','FCB','DDM'])))

#gets initial values
priceArray, nameArray = currentStocks(priceArray, nameArray)
time.sleep(30)
#gets values after x minutes
priceArrayCurrent, nameArrayCurrent = currentStocks(priceArrayCurrent, nameArrayCurrent)
maxMinSwap(priceArray, priceArrayCurrent, nameArray, nameArrayCurrent)
time.sleep(300)


while True:
	#sets the bought values to the price and name array
	priceArray = priceArrayCurrent
	nameArray = nameArrayCurrent
	#sets the current prices and names to current data
	priceArrayCurrent, nameArrayCurrent = currentStocks(priceArrayCurrent, nameArrayCurrent)
	#buys with new values
	maxMinSwap(priceArray, priceArrayCurrent, nameArray, nameArrayCurrent)
	#patiently waits 5 minutes to repeat
	time.sleep(300)