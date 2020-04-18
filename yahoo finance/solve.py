import json
import os
import time
import urllib.request as request
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import csv
from lxml import etree
import datetime as dt

def writeToCsv(data):
	with open('coinUrl.csv' , 'a+' , newline = "") as datacsv:
		csvwriter = csv.writer(datacsv, dialect = ("excel"))
		csvwriter.writerow(data)

def getCoinUrl(end_time, old_url_file):
	# 获取上一次爬取时的 coin symbol-coinname 关系
	symbol_name_dict = {}
	with open(old_url_file) as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		for row in readCSV:
			symbol_name_dict[row[0].strip()] = row[1]

	# 目前Yahoo总共112种货币。如果超过了150，这里需要修改
	url = "https://finance.yahoo.com/cryptocurrencies?all=&offset=0&count=150"
	
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
	headers = { 'User-Agent' : user_agent }
	req = Request(url, headers = headers)
	print("request")
	with urlopen(req,timeout=30) as response:
		data = response.read()
	print("response")
	data = data.decode("utf8")
	htmlData = etree.HTML(data)

	# 网站可能改版，这里需要修改
	coinTable = htmlData.xpath('//*[@id="scr-res-table"]/div[1]/table/tbody/tr')
	
	for row in coinTable:
		temp = row.xpath('./td[1]/a/@href')[0].split('?')

		# 后面对应的时间戳也要修改，去网站上看
		coinUrl = "https://finance.yahoo.com" + temp[0] + "/history?period1=1279296000&period2=" + str(end_time) + "&interval=1d&filter=history&frequency=1d"
		
		coinName = row.xpath('./td[2]/text()')[0].split(' USD')[0]
		symbol = row.xpath('./td[1]/a/text()')[0].strip()
		data = []
		data.append(symbol)

		# yahoo 上货币名字可能会改变。为了方便后续合并，我们与过去的 symbol-coinname-url 进行对比
		# 对于 symbol 相同的货币，采用过去的 coinname 进行命名
		if symbol in symbol_name_dict:
			coinName = symbol_name_dict[symbol]
		else:
			print(symbol)

		data.append(coinName)
		data.append(coinUrl)
		writeToCsv(data)



def getData():
	monthDict = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09',
				'Oct':'10', 'Nov':'11', 'Dec':'12', }
	driver = webdriver.Chrome()

	with open("coinUrl.csv") as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		for row in readCSV:
			if '/' in row[1]:
				row[1] = row[1].replace('/' , '-')
			if '*' in row[1]:
				row[1] = row[1].replace('*', '')
			symbol = row[0]
			coinName = row[1]
			url = row[2]

			# 注意最開始的保存路徑
			fileName = 'C:\\Users\\liuzhifeng\\Downloads\\' + coinName + '.csv'
			if os.path.isfile(fileName):
				print(coinName + " has been downloaded.")
				continue

			try:
				driver.get(url)
			except:
				print("Loading web failed")
			time.sleep(5)
			downloadIcon = driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a/span')
			downloadIcon.click()
			time.sleep(2)
			fileName = 'C:\\Users\\liuzhifeng\\Downloads\\' + symbol + ".csv"
			newFileName = 'C:\\Users\\liuzhifeng\\Downloads\\' + coinName + ".csv"
			os.rename(fileName, newFileName)
			print("Download " + coinName + " data successfully.")


if __name__ == "__main__":
	# 第一步，获取yahooFinance上coin的链接
	# 参数为 yahoo 上货币 historical data time period 选择 max 时，最大的时间（网址上）
	getCoinUrl(1584835200, "coinUrl_201904.csv")

	# 第二步，从coin链接上下载数据。下载完重命名，保存到C盘下载路径下
	getData()
	
