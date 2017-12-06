# -*- coding: utf-8 -*-
from PIL import Image
import time
import pytesseract
if __name__ == "__main__":
	image = Image.open("20110101-mobilezoom.jpg")
	print(image.format, image.size, image.mode)
	code = pytesseract.image_to_string(image)
	print(code)
	'''
	fileaccount = open("citys.txt", encoding='UTF-8')
	fileWrite = open("newCitys.txt", 'a', encoding='UTF-8')
	while 1:
		str = fileaccount.readline()
		if not str:
			break
		str = str.strip().split(", ")

		for i in str:
			i = i.split(":")
			print(i)
			fileWrite.write("'" + i[1] + "':")
			fileWrite.write("'" + i[0] + "', ")
		fileWrite.write('\n')
	fileaccount.close()
	fileWrite.close()
	'''
	'''
	monthDict = {'1':'31', '2':'28', '3':'31', '4':'30', '5':'31', '6':'30', '7':'31', '8':'31', '9':'30','10':'31','11':'30','12':'31'}
	year = 2011
	day = 1
	month = 1

	fileWrite = open("testName.txt", 'a', encoding='UTF-8')

	while 1:
		# 查找...
		if month <= 6: # 前半年
			if year % 4 == 0:
				size = 6.707
			else:
				size = 6.74
		else:
			if year != 2017:
				size = 6.633
			else:
				size = 1214 / (151 + int(time.strftime("%d"))) # 这里如果到2018年了还需要修改的



		# 截图命名...
		if month < 10:
			monthName = '0' + str(month)
		else:
			monthName = str(month)
		if day < 10:
			dayName = '0' + str(day)
		else:
			dayName = str(day)
		name = str(year) + monthName + dayName
		#fileWrite.write(name + "\n")
		print(name + " " + str(size))
		
		# 下面是日期修改
		if str(day) == monthDict.get(str(month)):
			if month != 12:
				day = 0
				month += 1
			else:
				day = 0
				month = 1
				year += 1
				if year % 4 == 0:
					monthDict['2'] = '29'
				else:
					monthDict['2'] = '28'

		if year == 2017 and month == 12 and day == int(time.strftime("%d")):
			break

		day += 1
		
	fileWrite.close()
	'''

