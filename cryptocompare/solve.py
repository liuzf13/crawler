import json
import os
import time
import csv
from cryptocompy import coin
from cryptocompy import price
import datetime as dt

def getCoins():
	coinData = coin.get_coin_list(coins = 'all')
	print(coinData)
	symbolDict = {} # symbol name
	for i in coinData:
		symbolDict[i] = coinData[i]['CoinName']

	'''
	with open('coin.csv' , 'w' , newline = "", encoding='utf-8') as datacsv:
		csvwriter = csv.writer(datacsv, dialect = ("excel"))
		csvwriter.writerow(["symbol", "coinName"])
		for i in symbolDict:
			data = []
			data.append(i)
			data.append(symbolDict[i])
			csvwriter.writerow(data)
	'''
	return symbolDict

def getDaily(symbol, coinName):
	if '/' in coinName:
		coinName = coinName.replace('/', '-')
	fileName = 'E:\\scrapy\\phoenixHealth\\code\\scapy\\newCryptoCompare\\daily\\' + coinName + '.csv'
	if os.path.isfile(fileName):
		print(coinName + " has been downloaded.")
		return

	# API限制，只能爬2000天
	test = price.get_historical_data(symbol, 'USD', 'day', info = 'full', aggregate = 1, limit = 2000)
	
	with open(fileName , 'w' , newline = "", encoding='utf-8') as datacsv:
		csvwriter = csv.writer(datacsv, dialect = ("excel"))
		firstLine = ["date" , "cryptocurrrency", "open" , "high" , "low" , "close" , "volume"]
		csvwriter.writerow(firstLine)
		for i in test:
			if i['high'] == 0 and i['low'] == 0 and i['open'] == 0 and i['close'] == 0 and i['volumeto'] == 0:
				continue
			data = []
			date = i['time'].split(' ')[0].replace('-', '/')
			data.append(date)
			data.append(coinName)
			data.append(i['open'])
			data.append(i['high'])
			data.append(i['low'])
			data.append(i['close'])
			data.append(i['volumeto'])
			csvwriter.writerow(data)
	print("Generate " + coinName + ".csv successfully.")



def getCurrencyDaily(symbol, currency):
	fileName = 'E:\\scrapy\\phoenixHealth\\code\\scapy\\newCryptoCompare\\currency-daily\\' + symbol + currency + '.csv'
	if os.path.isfile(fileName):
		print(coinName + " has been downloaded.")
		return
	test = price.get_historical_data(symbol, currency, 'day', info = 'full', aggregate = 1, limit = 2000)
	with open(fileName , 'w' , newline = "", encoding='utf-8') as datacsv:
		csvwriter = csv.writer(datacsv, dialect = ("excel"))
		firstLine = ["date" , "cryptocurrrency", "open" , "high" , "low" , "close" , "volume-from", "volume-to"]
		csvwriter.writerow(firstLine)
		for i in test:
			if i['high'] == 0 and i['low'] == 0 and i['open'] == 0 and i['close'] == 0 and i['volumeto'] == 0:
				continue
			data = []
			date = i['time'].split(' ')[0].replace('-', '/')
			data.append(date)
			data.append(symbol + currency)
			data.append(i['open'])
			data.append(i['high'])
			data.append(i['low'])
			data.append(i['close'])
			data.append(i['volumefrom'])
			data.append(i['volumeto'])
			csvwriter.writerow(data)
	print("Generate " + symbol + currency + ".csv successfully.")


if __name__ == "__main__":
	# 第一步，获取cryptocompare上所有货币信息
	symbolDict = getCoins()
	# print(symbolDict)
	
	# 第二步，爬取每个货币的信息。API限制，只能往前爬2000天
	for symbol in symbolDict:
		getDaily(symbol, symbolDict[symbol])
	


