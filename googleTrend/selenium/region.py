import json
import os
import time
import csv



if __name__ == "__main__":
	itemDict = {} # {'coinName' : 'cityDict'}
	filePath = 'E:\\scrapy\\scrapyProject\\googleTrends\\data\\city_name\\'
	cityList = []
	getCityFlag = 0
	for fileName in os.listdir(filePath):
		coinName = fileName.split('_')[0]
		dataDict = {}
		with open(filePath + fileName, encoding='UTF-8') as csvfile:
			readCSV = csv.reader(csvfile, delimiter=',')
			count = 0
			for row in readCSV:
				count += 1
				if count < 4:
					continue
				dataDict[row[0]] = row[1]
				if getCityFlag == 0:
					cityList.append(row[0])
		itemDict[coinName] = dataDict
		if cityList:
			getCityFlag = 1
	#print(itemDict['StarCoin'])

	with open('cityNameResult.csv' , 'w' , newline = "") as datacsv:
		csvwriter = csv.writer(datacsv, dialect = ("excel"))
		firstLine = []
		firstLine.append('City')
		for i in itemDict:
			firstLine.append(i)
		csvwriter.writerow(firstLine)
		for i in cityList:
			data = []
			data.append(i)
			for j in itemDict:
				if itemDict[j][i]:
					data.append(itemDict[j][i])
				else:
					data.append(' ')
			csvwriter.writerow(data)




