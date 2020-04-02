import json
import os
import time
import urllib.request as request
import requests
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import csv
from lxml import etree

def writeToCsv(data):
	with open('coinUrl.csv' , 'a+' , newline = "") as datacsv:
		csvwriter = csv.writer(datacsv, dialect = ("excel"))
		csvwriter.writerow(data)

def write_row_to_csv(data, file_name):
	with open(file_name , 'a+' , newline = "") as datacsv:
		csvwriter = csv.writer(datacsv, dialect = ("excel"))
		csvwriter.writerow(data)


# 旧爬虫，oinmarketcap.com/all/views/all/ 直接显示所有的coin，因此直接访问+静态爬取
# 20200323 已改版，每次只加载 200 个 coin
def getCoinUrl(end_date):
	url = "https://coinmarketcap.com/all/views/all/"
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
	headers = { 'User-Agent' : user_agent }
	req = Request(url, headers = headers)
	print("request")
	with urlopen(req,timeout=30) as response:
		data = response.read()
	print("response")
	data = data.decode("utf8")
	htmlData = etree.HTML(data)

	# 这里可能需要修改，根据网站的变化情况
	coinTable = htmlData.xpath('//*[@id="currencies-all"]/tbody/tr')
	for row in coinTable:
		coinName = row.xpath('./td[2]/a/text()')[0]
		coinUrl = row.xpath('./td[2]/a/@href')[0]
		data = []
		data.append(coinName)

		# 更新信息，修改这里的日期
		temp = "https://coinmarketcap.com" + str(coinUrl) + "historical-data/?start=20130428&end=" + str(end_date) # 20190329
		
		data.append(temp)
		print(data)
		writeToCsv(data)


# 获取所有 coin 的 symbol-name-coinurl
# python 改用下划线了
# 20200323 总共 2466 个货币
def get_coin_url_new(max_num, end_date):
	start = 1
	while start < max_num:
		url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?convert=USD,BTC,ETH,XRP,BCH,LTC&cryptocurrency_type=all&limit=200&sort=market_cap&sort_dir=desc&start=" + str(start)
		user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
		headers = { 'User-Agent' : user_agent }
		req = Request(url, headers = headers)
		# print("request")
		with urlopen(req,timeout=30) as response:
			data = response.read()
		# print("response")
		data = data.decode("utf8")
		data = json.loads(data)
		# print(data)

		print(len(data["data"]))
		for item in data["data"]:
			coin_name = item["name"]
			coin_symbol = item["symbol"]
			coin_url = "https://coinmarketcap.com/currencies/" + item["slug"] + "/historical-data/?start=20130428&end=" + str(end_date)
			data = [coin_symbol, coin_name, coin_url]
			write_row_to_csv(data, "coin_url.csv")


		time.sleep(2)

		start += 200



def get_data(coinName, url):
	monthDict = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09',
				'Oct':'10', 'Nov':'11', 'Dec':'12', }
	fileName = 'E:\\scrapy\\phoenixHealth\\code\\scapy\\coinmarketcapcom\\daily\\' + coinName + '.csv'
	if os.path.isfile(fileName):
		print(coinName + " has been downloaded.")
		return
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
	headers = { 'User-Agent' : user_agent }
	req = Request(url, headers = headers)
	# print("request")
	with urlopen(req,timeout=60) as response:
		data = response.read()
	# print("response")
	data = data.decode("utf8")
	# print(data)
	htmlData = etree.HTML(data)

	# 这里可能需要修改，根据网站的变化情况
	dataTable = htmlData.xpath('//*[@id="__next"]/div/div[2]/div[1]/div[2]/div[3]/div/ul[2]/li[5]/div/div/div[2]/div[3]/div/table/tbody/tr')
	if len(dataTable) == 0:
		dataTable = htmlData.xpath('//*[@id="__next"]/div/div[2]/div[1]/div[2]/div[4]/div/ul[2]/li[5]/div/div/div[2]/div[3]/div/table/tbody/tr')
	
	with open(fileName , 'w' , newline = "") as datacsv:
		csvwriter = csv.writer(datacsv, dialect = ("excel"))
		firstLine = ["date" , "cryptocurrrency", "open" , "high" , "low" , "close" , "volume", "marketCap"]
		csvwriter.writerow(firstLine)
		for row in dataTable:
			temp = row.xpath('./td[1]/div/text()')[0].split(' ')
			year = temp[2]
			month = monthDict[temp[0]]
			day = temp[1].split(',')[0]
			date = year + '-' + month + '-' + day
			openPrice = row.xpath('./td[2]/div/text()')[0]
			highPrice = row.xpath('./td[3]/div/text()')[0]
			lowPrice = row.xpath('./td[4]/div/text()')[0]
			closePrice = row.xpath('./td[5]/div/text()')[0]
			volume = row.xpath('./td[6]/div/text()')[0]
			mktCap = row.xpath('./td[7]/div/text()')[0]
			data = [date, coinName, openPrice, highPrice, lowPrice, closePrice, volume, mktCap]
			for i in range(2, len(data)):
				data[i] = data[i].replace(',', '')
			csvwriter.writerow(data)

	print("Download daily data for " + coinName + " successfully.")
	time.sleep(5)



if __name__ == "__main__":
	# 爬取最新的coinmarketcap信息

	# 首先，获取所有货币的coinURL，存到coinUrl.csv
	# getCoinUrl(20200322)
	get_coin_url_new(2466, 20200322)

	# 然后，爬取每个货币的数据
	# with open("coin_url.csv") as csvfile:
	# 	csv_reader = csv.reader(csvfile, delimiter=',')
	# 	for row in csv_reader:
	# 		coin_name = row[1]
	# 		if '/' in coin_name:
	# 			coin_name = coin_name.replace('/' , '-')
	# 		coin_url = row[2]
	# 		try:
	# 			get_data(coin_name, coin_url)
	# 		except:
	# 			print("Download " + coin_name + " failed.")
	

	