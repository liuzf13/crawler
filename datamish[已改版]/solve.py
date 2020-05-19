import logging
import time
import sys
import websocket
import urllib.request as request
import requests
import re
import datetime as dt
import os
import csv

def writeRowToCsv(data, fileName):
	with open(fileName , 'a+', newline = "") as datacsv:
		csvwriter = csv.writer(datacsv, dialect = ("excel"))
		csvwriter.writerow(data)

def changeTime(timeStamp):
	timeArray = time.localtime(timeStamp)
	otherStyleTime = time.strftime("%Y/%m/%d", timeArray)
	return otherStyleTime

def changeTime2(timeStamp):
	temp = str(dt.datetime.fromtimestamp(float(timeStamp))).split('.')[0]
	#temp = str(dt.datetime.fromtimestamp(float(timeStamp)))
	return temp

def getLongAndShort(symbolList):
	# get long and short data from datamish.com
	for symbol in symbolList:
		fileName = './long_short/' + symbol + ".csv"
		if os.path.exists(fileName):
			print(symbol + " has been downloaded.")
			continue
		firstLine = ["date", "symbol", "long", "short"]
		writeRowToCsv(firstLine, fileName)
		# total longs and usd rates
		longUrl = "https://datamish.com/api/datasources/proxy/1/query?db=bfx&q=SELECT%20last(%22total%22)%20FROM%20%22bfx_margin_longs%22%20WHERE%20(%22symbol%22%20%3D%20%27" + symbol + "%27%20AND%20%22type%22%20%3D%20%27longs%27)%20AND%20time%20%3E%3D%201470881100898ms%20GROUP%20BY%20time(1d)%20fill(previous)%3BSELECT%20mean(%22last_price%22)%20FROM%20%22bfx_rates%22%20WHERE%20(%22symbol%22%20%3D%20%27USD%27)%20AND%20time%20%3E%3D%201470881100898ms%20GROUP%20BY%20time(30d)%20fill(previous)&epoch=ms"

		# total shorts and symbol rates
		shortUrl = "https://datamish.com/api/datasources/proxy/1/query?db=bfx&q=SELECT%20last(%22total%22)%20FROM%20%22bfx_margin_shorts%22%20WHERE%20(%22symbol%22%20%3D%20%27" + symbol + "%27%20AND%20%22type%22%20%3D%20%27shorts%27)%20AND%20time%20%3E%3D%201470881749580ms%20GROUP%20BY%20time(1d)%20fill(previous)%3BSELECT%20mean(%22ask%22)%20FROM%20%22bfx_rates%22%20WHERE%20(%22symbol%22%20%3D%20%27" + symbol + "%27)%20AND%20time%20%3E%3D%201470881749580ms%20GROUP%20BY%20time(30d)%20fill(previous)&epoch=ms"

		resultDict = {}
		try:
			r = requests.get(longUrl)
			result = r.json()
			valueList = result["results"][0]['series'][0]["values"]
			for value in valueList:
				if not value[1]:
					continue
				if not value[0] in resultDict:
					resultDict[value[0]] = {"long":'', "short":''}
				resultDict[value[0]]["long"] = value[1]
		except:
			print("Getting " + symbol + " error.")

		try:
			r = requests.get(shortUrl)
			result = r.json()
			valueList = result["results"][0]['series'][0]["values"]
			for value in valueList:
				if not value[1]:
					continue
				resultDict[value[0]]["short"] = value[1]
		except:
			print("Getting " + symbol + " error.")

		#print(resultDict)

		for date in resultDict:
			data = []
			data.append(changeTime2(float(date) / 1000))
			data.append(symbol)
			data.append(resultDict[date]["long"])
			data.append(resultDict[date]["short"])
			writeRowToCsv(data, fileName)

		print("Download " + symbol + " successfully.")

		time.sleep(5)


def getPercent(symbolList):
	# get long/short percent data from datamish.com
	for symbol in symbolList:
		fileName = './percent/' + symbol + ".csv"
		if os.path.exists(fileName):
			print(symbol + " has been downloaded.")
			continue
		firstLine = ["date", "symbol", "longPercent", "shortPercent"]
		writeRowToCsv(firstLine, fileName)

		# percern long/shorts
		percentUrl = "https://datamish.com/api/datasources/proxy/1/query?db=bfx&q=SELECT%20last(%22long_pct%22)%20FROM%20%22bfx_pct_long_short%22%20WHERE%20(%22symbol%22%20%3D%20%27" + symbol + "%27)%20AND%20time%20%3E%3D%201470884082429ms%20GROUP%20BY%20time(1d)%20fill(previous)%3BSELECT%20last(%22short_pct%22)%20FROM%20%22bfx_pct_long_short%22%20WHERE%20(%22symbol%22%20%3D%20%27" + symbol + "%27)%20AND%20time%20%3E%3D%201470884082429ms%20GROUP%20BY%20time(1d)%20fill(previous)&epoch=ms"

		resultDict = {}
		try:
			r = requests.get(percentUrl)
			result = r.json()
			valueList = result["results"][0]['series'][0]["values"]
			for value in valueList:
				if not value[1]:
					continue
				if not value[0] in resultDict:
					resultDict[value[0]] = {"longPercent":'', "shortPercent":''}
				resultDict[value[0]]["longPercent"] = value[1]

			valueList = result["results"][1]['series'][0]["values"]
			for value in valueList:
				if not value[1]:
					continue
				resultDict[value[0]]["shortPercent"] = value[1]
		except:
			print("Getting " + symbol + " error.")

		#print(resultDict)
		for date in resultDict:
			data = []
			data.append(changeTime2(float(date) / 1000))
			data.append(symbol)
			data.append(resultDict[date]["longPercent"])
			data.append(resultDict[date]["shortPercent"])
			writeRowToCsv(data, fileName)

		print("Download " + symbol + " successfully.")

		time.sleep(5)


def getShortDetails(symbolList):
	# get short detail data from datamish.com
	for symbol in symbolList:
		fileName = './shortDetail/' + symbol + ".csv"
		if os.path.exists(fileName):
			print(symbol + " has been downloaded.")
			continue
		firstLine = ["date", "symbol", "shortCurrent", "hedgedCurrent"]
		writeRowToCsv(firstLine, fileName)

		# shorts details
		shortDUrl = "https://datamish.com/api/datasources/proxy/1/query?db=bfx&q=SELECT%20last(%22short%22)%20FROM%20%22bfx_margin_shorts%22%20WHERE%20(%22symbol%22%20%3D%20%27" + symbol + "%27)%20AND%20time%20%3E%3D%201470884499034ms%20GROUP%20BY%20time(1d)%20fill(previous)%3BSELECT%20last(%22hedged%22)%20FROM%20%22bfx_margin_shorts%22%20WHERE%20(%22symbol%22%20%3D%20%27" + symbol + "%27)%20AND%20time%20%3E%3D%201470884499034ms%20GROUP%20BY%20time(1d)%20fill(previous)&epoch=ms"

		resultDict = {}
		try:
			r = requests.get(shortDUrl)
			result = r.json()
			valueList = result["results"][0]['series'][0]["values"]
			for value in valueList:
				if not value[1]:
					continue
				if not value[0] in resultDict:
					resultDict[value[0]] = {"shortCurrent":'', "hedgedCurrent":''}
				resultDict[value[0]]["shortCurrent"] = value[1]

			valueList = result["results"][1]['series'][0]["values"]
			for value in valueList:
				if not value[1]:
					continue
				resultDict[value[0]]["hedgedCurrent"] = value[1]
		except:
			print("Getting " + symbol + " error.")

		#print(resultDict)
		for date in resultDict:
			data = []
			data.append(changeTime2(float(date) / 1000))
			data.append(symbol)
			data.append(resultDict[date]["shortCurrent"])
			data.append(resultDict[date]["hedgedCurrent"])
			writeRowToCsv(data, fileName)

		print("Download " + symbol + " successfully.")

		time.sleep(5)


def getSymbolRate(symbolList):
	# get symbol rate data from datamish.com
	for symbol in symbolList:
		fileName = './symbolRate/' + symbol + ".csv"
		if os.path.exists(fileName):
			print(symbol + " has been downloaded.")
			continue
		firstLine = ["date", "symbol", "symbolFrr", "USDFrr"]
		writeRowToCsv(firstLine, fileName)

		# shorts details
		symbolRateUrl = "https://datamish.com/api/datasources/proxy/1/query?db=bfx&q=SELECT%20mean(%22frr%22)%20FROM%20%22bfx_rates%22%20WHERE%20(%22symbol%22%20%3D%20%27" + symbol + "%27)%20AND%20time%20%3E%3D%201471141123854ms%20GROUP%20BY%20time(1d)%20fill(previous)%3BSELECT%20mean(%22last_price%22)%20FROM%20%22bfx_rates%22%20WHERE%20(%22symbol%22%20%3D%20%27" + symbol + "%27)%20AND%20time%20%3E%3D%201471141123854ms%20GROUP%20BY%20time(30d)%20fill(previous)&epoch=ms"
		usdRateUrl = "https://datamish.com/api/datasources/proxy/1/query?db=bfx&q=SELECT%20mean(%22frr%22)%20FROM%20%22bfx_rates%22%20WHERE%20(%22symbol%22%20%3D%20%27USD%27)%20AND%20time%20%3E%3D%201471141123854ms%20GROUP%20BY%20time(1d)%20fill(previous)%3BSELECT%20mean(%22last_price%22)%20FROM%20%22bfx_rates%22%20WHERE%20(%22symbol%22%20%3D%20%27USD%27)%20AND%20time%20%3E%3D%201471141123854ms%20GROUP%20BY%20time(30d)%20fill(previous)&epoch=ms"
		
		resultDict = {}
		try:
			r = requests.get(symbolRateUrl)
			result = r.json()
			valueList = result["results"][0]['series'][0]["values"]
			for value in valueList:
				if not value[1]:
					continue
				if not value[0] in resultDict:
					resultDict[value[0]] = {"symbolFrr":'', "USDFrr":''}
				resultDict[value[0]]["symbolFrr"] = value[1]
		except:
			print("Getting " + symbol + " error.")

		try:
			r = requests.get(usdRateUrl)
			result = r.json()
			valueList = result["results"][0]['series'][0]["values"]
			for value in valueList:
				if not value[1]:
					continue
				resultDict[value[0]]["USDFrr"] = value[1]
		except:
			print("Getting " + symbol + " error.")

		#print(resultDict)
		for date in resultDict:
			data = []
			data.append(changeTime2(float(date) / 1000))
			data.append(symbol)
			data.append(resultDict[date]["symbolFrr"])
			data.append(resultDict[date]["USDFrr"])
			writeRowToCsv(data, fileName)

		print("Download " + symbol + " successfully.")

		time.sleep(5)



def getUserDefined(symbolList):
	# get user defined data from datamish.com
	for symbol in symbolList:
		fileName = './userDefined/' + symbol + ".csv"
		if os.path.exists(fileName):
			print(symbol + " has been downloaded.")
			continue
		firstLine = ["date", "symbol", "LongChange", "shortChange"]
		writeRowToCsv(firstLine, fileName)

		# user defined details
		userUrl = "https://datamish.com/api/datasources/proxy/1/query?db=bfx&q=SELECT%20derivative(mean(%22total%22)%2C%205m)%20FROM%20%22bfx_margin_longs%22%20WHERE%20(%22symbol%22%20%3D%20%27" + symbol + "%27)%20AND%20time%20%3E%3D%201471145800513ms%20GROUP%20BY%20time(1d)%20fill(null)%3BSELECT%20derivative(mean(%22total%22)%2C%205m)%20FROM%20%22bfx_margin_shorts%22%20WHERE%20(%22symbol%22%20%3D%20%27" + symbol + "%27)%20AND%20time%20%3E%3D%201471145800513ms%20GROUP%20BY%20time(1d)%20fill(null)&epoch=ms"

		resultDict = {}
		try:
			r = requests.get(userUrl)
			result = r.json()
			valueList = result["results"][0]['series'][0]["values"]
			for value in valueList:
				if not value[1]:
					continue
				if not value[0] in resultDict:
					resultDict[value[0]] = {"longChange":'', "shortChange":''}
				resultDict[value[0]]["longChange"] = value[1]

			valueList = result["results"][1]['series'][0]["values"]
			for value in valueList:
				if not value[1]:
					continue
				if value[0] in resultDict:
					resultDict[value[0]]["shortChange"] = value[1]
		except:
			print("Getting " + symbol + " error.")

		#print(resultDict)
		for date in resultDict:
			data = []
			data.append(changeTime2(float(date) / 1000))
			data.append(symbol)
			data.append(resultDict[date]["longChange"])
			data.append(resultDict[date]["shortChange"])
			writeRowToCsv(data, fileName)

		print("Download " + symbol + " successfully.")

		time.sleep(5)

def merge(symbolList):
	fileList = ["long_short", "percent", "shortDetail", "symbolRate", "userDefined"]
	firstLine = ["date", "symbol", "long", "short", "longPercent", "shortPercent", "shortCurrent", "hedgedCurrent", "symbolFrr", "USDFrr", "longChange", "shortChange"]
	writeRowToCsv(firstLine, "datamish.csv")

	for symbol in symbolList:
		result = {}
		for path in fileList:
			fileName = './' + path + '/' + symbol + ".csv"
			with open(fileName) as csvfile:
				readCSV = csv.reader(csvfile, delimiter=',')
				for row in readCSV:
					if row[0] == "date":
						continue
					if not row[0] in result:
						result[row[0]] = {"long":'', "short":'', "longPercent":'', "shortPercent":'', "shortCurrent":'', "hedgedCurrent":'', "symbolFrr":'', "USDFrr":'', "longChange":'', "shortChange":''}
					if path == "long_short":
						result[row[0]]["long"] = row[2]
						result[row[0]]["short"] = row[3]
					elif path == "percent":
						result[row[0]]["longPercent"] = row[2]
						result[row[0]]["shortPercent"] = row[3]
					elif path == "shortDetail":
						result[row[0]]["shortCurrent"] = row[2]
						result[row[0]]["hedgedCurrent"] = row[3]
					elif path == "symbolRate":
						result[row[0]]["symbolFrr"] = row[2]
						result[row[0]]["USDFrr"] = row[3]
					elif path == "userDefined":
						result[row[0]]["longChange"] = row[2]
						result[row[0]]["shortChange"] = row[3]						
		for date in result:
			if result[date]["long"] == '':
				continue
			data = []
			data.append(date)
			data.append(symbol)
			data.append(result[date]["long"])
			data.append(result[date]["short"])
			data.append(result[date]["longPercent"])
			data.append(result[date]["shortPercent"])
			data.append(result[date]["shortCurrent"])
			data.append(result[date]["hedgedCurrent"])
			data.append(result[date]["symbolFrr"])
			data.append(result[date]["USDFrr"])
			data.append(result[date]["longChange"])
			data.append(result[date]["shortChange"])
			writeRowToCsv(data, "datamish.csv")
		print("Merge " + symbol + " successfully.")

if __name__ == "__main__":
	symbolList = ["BCH", "BTC", "EOS", "ETH", "IOT", "LTC", "XMR", "ZEC", "XRP"]
	getLongAndShort(symbolList)
	'''
	getLongAndShort(symbolList)
	getPercent(symbolList)
	getShortDetails(symbolList)
	getSymbolRate(symbolList)
	getUserDefined(symbolList)
	'''
	# merge(symbolList)
	

	'''
	# total longs and usd rates
	longUrl = "https://datamish.com/api/datasources/proxy/1/query?db=bfx&q=SELECT%20last(%22total%22)%20FROM%20%22bfx_margin_longs%22%20WHERE%20(%22symbol%22%20%3D%20%27" + symbol + "%27%20AND%20%22type%22%20%3D%20%27longs%27)%20AND%20time%20%3E%3D%201470881100898ms%20GROUP%20BY%20time(1d)%20fill(previous)%3BSELECT%20mean(%22last_price%22)%20FROM%20%22bfx_rates%22%20WHERE%20(%22symbol%22%20%3D%20%27USD%27)%20AND%20time%20%3E%3D%201470881100898ms%20GROUP%20BY%20time(30d)%20fill(previous)&epoch=ms"

	# total shorts and symbol rates
	shortUrl = "https://datamish.com/api/datasources/proxy/1/query?db=bfx&q=SELECT%20last(%22total%22)%20FROM%20%22bfx_margin_shorts%22%20WHERE%20(%22symbol%22%20%3D%20%27" + symbol + "%27%20AND%20%22type%22%20%3D%20%27shorts%27)%20AND%20time%20%3E%3D%201470881749580ms%20GROUP%20BY%20time(1d)%20fill(previous)%3BSELECT%20mean(%22ask%22)%20FROM%20%22bfx_rates%22%20WHERE%20(%22symbol%22%20%3D%20%27" + symbol + "%27)%20AND%20time%20%3E%3D%201470881749580ms%20GROUP%20BY%20time(30d)%20fill(previous)&epoch=ms"

	# percern long/shorts
	percentUrl = "https://datamish.com/api/datasources/proxy/1/query?db=bfx&q=SELECT%20last(%22long_pct%22)%20FROM%20%22bfx_pct_long_short%22%20WHERE%20(%22symbol%22%20%3D%20%27" + symbol + "%27)%20AND%20time%20%3E%3D%201470884082429ms%20GROUP%20BY%20time(1d)%20fill(previous)%3BSELECT%20last(%22short_pct%22)%20FROM%20%22bfx_pct_long_short%22%20WHERE%20(%22symbol%22%20%3D%20%27" + symbol + "%27)%20AND%20time%20%3E%3D%201470884082429ms%20GROUP%20BY%20time(1d)%20fill(previous)&epoch=ms"

	# shorts details
	shortDUrl = "https://datamish.com/api/datasources/proxy/1/query?db=bfx&q=SELECT%20last(%22short%22)%20FROM%20%22bfx_margin_shorts%22%20WHERE%20(%22symbol%22%20%3D%20%27" + symbol + "%27)%20AND%20time%20%3E%3D%201470884499034ms%20GROUP%20BY%20time(1d)%20fill(previous)%3BSELECT%20last(%22hedged%22)%20FROM%20%22bfx_margin_shorts%22%20WHERE%20(%22symbol%22%20%3D%20%27" + symbol + "%27)%20AND%20time%20%3E%3D%201470884499034ms%20GROUP%20BY%20time(1d)%20fill(previous)&epoch=ms"

	# symbol rate
	symbolRateUrl = "https://datamish.com/api/datasources/proxy/1/query?db=bfx&q=SELECT%20mean(%22frr%22)%20FROM%20%22bfx_rates%22%20WHERE%20(%22symbol%22%20%3D%20%27" + symbol + "%27)%20AND%20time%20%3E%3D%201471141123854ms%20GROUP%20BY%20time(10m)%20fill(previous)%3BSELECT%20mean(%22last_price%22)%20FROM%20%22bfx_rates%22%20WHERE%20(%22symbol%22%20%3D%20%27" + symbol + "%27)%20AND%20time%20%3E%3D%201471141123854ms%20GROUP%20BY%20time(30d)%20fill(previous)&epoch=ms"
	usdRateUrl = "https://datamish.com/api/datasources/proxy/1/query?db=bfx&q=SELECT%20mean(%22frr%22)%20FROM%20%22bfx_rates%22%20WHERE%20(%22symbol%22%20%3D%20%27USD%27)%20AND%20time%20%3E%3D%201471141123854ms%20GROUP%20BY%20time(10m)%20fill(previous)%3BSELECT%20mean(%22last_price%22)%20FROM%20%22bfx_rates%22%20WHERE%20(%22symbol%22%20%3D%20%27USD%27)%20AND%20time%20%3E%3D%201471141123854ms%20GROUP%20BY%20time(30d)%20fill(previous)&epoch=ms"
	'''