import json
import os
import time
import csv
import datetime as dt



if __name__ == "__main__":
	itemDict = {} # {'coinName' : 'dataList'}
	filePath = './data/total_name/'
	dateList = []
	getDateFlag = 0
	for fileName in os.listdir(filePath):
		coinName = fileName.split('_')[0]
		dataList = []
		with open(filePath + fileName, encoding='UTF-8') as csvfile:
			readCSV = csv.reader(csvfile, delimiter=',')
			count = 0
			for row in readCSV:
				if len(row) < 2:
					continue
				if not '-' in row[0]:
					continue
				#print(row)
				dataList.append(row[1])
				if getDateFlag == 0:
					dateList.append(row[0])
		itemDict[coinName] = dataList
		if dateList:
			getDateFlag = 1


	
	with open('totalNameResult_20180830.csv' , 'w' , newline = "") as datacsv:
		csvwriter = csv.writer(datacsv, dialect = ("excel"))
		firstLine = []
		firstLine.append('Date')
		for i in itemDict:
			firstLine.append(i)
		csvwriter.writerow(firstLine)
		for i in range(len(dateList)):
			data = []
			data.append(dateList[i])
			for j in itemDict:
				if itemDict[j]:
					data.append(itemDict[j][i])
				else:
					data.append(' ')
			csvwriter.writerow(data)
	

	
	with open('googleTrends_20180902.csv' , 'w' , newline = "") as datacsv:
		csvwriter = csv.writer(datacsv, dialect = ("excel"))
		firstLine = ['date', 'cryptocurrency', 'searchVolume']
		csvwriter.writerow(firstLine)
		for cryptocurrency in itemDict:
			for index in range(len(dateList)):
				data = []
				data.append(dateList[index])
				data.append(cryptocurrency)
				if itemDict[cryptocurrency]:
					data.append(itemDict[cryptocurrency][index])
				else:
					data.append('')
				csvwriter.writerow(data)
	