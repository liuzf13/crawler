# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import requests
import numpy as np
import os,base64
import sys
import re
import csv
import datetime

def openBrowser(num):
	#num means the current account ranging from 0 to 9
    global browser

    url = "https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F"
    # Firefox()
    # Chrome()
    browser = webdriver.Chrome()
    browser.get(url)

    # 用户名登录
    browser.find_element_by_id("TANGRAM__PSP_3__footerULoginBtn").click()
    time.sleep(1)
    browser.find_element_by_id("TANGRAM__PSP_3__userName").clear()
    browser.find_element_by_id("TANGRAM__PSP_3__password").clear()
    
    # account = loadAccount()
    # username = account[num][0]
    # password = account[num][1]
    # browser.find_element_by_id("TANGRAM__PSP_3__userName").send_keys(username)
    # time.sleep(1)
    # browser.find_element_by_id("TANGRAM__PSP_3__password").send_keys(password)

    # # id="TANGRAM__PSP_3__submit"
    # browser.find_element_by_id("TANGRAM__PSP_3__submit").click()
    # print("ready for new site...")

    # print("Verifying")
    # time.sleep(5)
    print("Please input your username and passwd. After login, please input 'y' in the cmd.")
    while True:
    	p = input()
    	if p == 'y' or p == 'yes':
    		break
    # if p == 'y' or p == 'yes':
    # 	pass
    # else:
    # 	browser.find_element_by_id("TANGRAM__22__button_send_email").click()
    # 	time.sleep(5)

    # 	mail = loadMail()
    # 	msg = rcvmail.rcvmail(mail[num][0],mail[num][1],mail[num][2])
    # 	veri_code = rcvmail.getMailText(msg)
    # 	browser.find_element_by_id("TANGRAM__22__input_vcode").send_keys(veri_code)
    # 	browser.find_element_by_id("TANGRAM__22__button_submit").click()
    # 	time.sleep(5)


def retry(current_keyword, province, city, half, year):
	browser.refresh()
	time.sleep(5)

	# bitcoin 不需要 chooseCity
	#chooseCity(province,city)

	time.sleep(5)
	chooseTime(half[0],half[1],year)
	time.sleep(2)

def init(current_keyword, current_account):
	openBrowser(current_account)
	js = 'window.open("http://index.baidu.com");'
	browser.execute_script(js)
	time.sleep(1)
	handles = browser.window_handles
	browser.switch_to_window(handles[-1])
	time.sleep(5)
	# input the keyword
	browser.find_element_by_class_name("search-input").clear()
	browser.find_element_by_class_name("search-input").send_keys(current_keyword)
	browser.find_element_by_class_name("search-input-cancle").click()
	time.sleep(5) #wait for response
	browser.maximize_window()
	time.sleep(2)

def writeCSV(data, file_name):
    with open(file_name, 'a+', newline="") as datacsv:
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        csvwriter.writerow(data)

# 模拟鼠标移动，读取数值
def moveFocus(year, out_file):
	# xoyelement = browser.find_element_by_class_name("index-trend-chart")
	# ActionChains(browser).move_to_element_with_offset(xoyelement, 50, 90).perform()
	# time_element = browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]/div[1]/div[1]/div/div[2]/div[1]')
	# index_time = time_element.text.split(' ')[0]  
	# print(index_time)
	# index_element = browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]/div[1]/div[1]/div/div[2]/div[2]/div[2]')
	# index_value = index_element.text.replace(' ','')
	# print(index_value)

	# 获得趋势框，总宽度为 1256
	xoyelement = browser.find_element_by_class_name("index-trend-chart")
	width = 1256
	if year % 4 == 0:
		days = 366
	else:
		days = 365

	step = width / days
	x_0 = 0
	y_0 = 90
	for i in range(days):
		ActionChains(browser).move_to_element_with_offset(xoyelement, x_0, y_0).perform()
		time_element = browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]/div[1]/div[1]/div/div[2]/div[1]')
		index_time = time_element.text.split(' ')[0]  
		index_element = browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]/div[1]/div[1]/div/div[2]/div[2]/div[2]')
		index_value = index_element.text.replace(' ','')
		data = [index_time, index_value]
		print(data)
		writeCSV(data, out_file)

		x_0 += step
		time.sleep(1)
	# ActionChains(browser).move_to_element_with_offset(xoyelement, 50, 90).perform()
	# time.sleep(5)
	

def getIndex(current_keyword, current_city):
	print("Start Time: " + str(time.strftime("%H:%M:%S")))

	'''
	# bitcoin 全国指数，不考虑城市信息
	current_city = current_city.strip('\n')
	p_c = current_city.split(' ')
	province = p_c[0]
	city = p_c[1]
	chooseCity(province,city)
	'''

	province = "所有省份"
	city = "所有省份"

	# TODO: choose time, generate pic, etc
	halfYear =[[1, 12]] 
	for year in range(2019, 2020):
		print("loading data in year " + str(year))
		out_file = './data/' + current_keyword + "_" + str(year) + ".csv"
		for half in halfYear:
			if chooseTime(half[0],half[1],year) == -1:
				retry(current_keyword, province, city, half, year)
			
			time.sleep(10)
			moveFocus(year, out_file)

	summary.close()

	return 1


def chooseCity(province, city):
	browser.find_element_by_class_name("index-region").click()
	time.sleep(2)
	browser.find_element_by_xpath("//*[text()='" + province + "']").click()
	print(province)
	if province == city:
		time.sleep(4)
		return
	time.sleep(1)
	browser.find_element_by_xpath("//*[text()='" + city + "']").click()
	print(city)
	time.sleep(4)


def chooseDate(timestr, targetM, targetY, x):
	curr = text2Data(timestr)
	if curr == []:
		return -1

	iconB = browser.find_elements_by_class_name("fa-icon")
	lastY = iconB[1 + 4 * x]
	formerY = iconB[2 + 4 * x]
	lastM = iconB[3 + 4 * x]
	formerM = iconB[4 + 4 * x]
	if curr[0] < targetY:
		#press the right button
		for i in range(targetY - curr[0]):
			formerY.click()
			time.sleep(0.5)
	elif curr[0] > targetY:
		#press the left button
		for i in range(curr[0] - targetY):
			lastY.click()
			time.sleep(0.5)
	else:
		#do nothing
		pass

	if curr[1] < targetM:
		#press the right button
		for i in range(targetM - curr[1]):
			formerM.click()
			time.sleep(0.5)
	elif curr[1] > targetM:
		#press the left button
		for i in range(curr[1] - targetM):
			lastM.click()
			time.sleep(0.5)
	return 1

def chooseTime(start, end, year):
	time.sleep(2)
	browser.find_element_by_class_name("index-date-range-picker").click()
	time.sleep(1)
	se = browser.find_elements_by_class_name("date-panel")

	startTime = se[0].text
	# print(startTime)
	if chooseDate(startTime, start, year, 0) == -1:
		return -1
	#press the button with text 1, e.g. 1.1 or 7.1
	dates = browser.find_elements_by_class_name("veui-calendar-day")
	dates[0].click()
	time.sleep(1)

	#input endTime
	se[1].click()
	time.sleep(1)

	endTime = se[1].text
	if chooseDate(endTime, end, year, 1) == -1:
		return -1
	#press the button with the last day of the month, e.g. 6.30 or 12.31
	dates = browser.find_elements_by_class_name("veui-calendar-body")[1].find_elements_by_class_name("veui-calendar-day")
	dates[monthday(end,year) - 1].click()
	time.sleep(1)

	browser.find_elements_by_class_name("primary")[0].click()

	return 1

def downloadControl():
	# current_account = 0
	# current_city = 0
	current_keyword = 'bitcoin'
	fcity = open("sim_city.txt",'r',encoding='utf-8')
	cities = fcity.readlines()
	fcity.close()
	flagMat = []
	for city in cities:
		flagMat.append([city,0])

	# 初始化，打来自动浏览器
	init(current_keyword, 0)

	# bitcoin 只考虑全国，不考虑分地区
	getIndex(current_keyword, "全国")

	browser.quit()

# 合并每一年的结果
def merge(out_file):
	files = os.listdir('./data/')

	with open(out_file, 'w', newline="") as datacsv:
		csvwriter = csv.writer(datacsv, dialect=("excel"))
		csvwriter.writerow(["date", "index"])

		for file in files:
			in_file = './data/' + file
			with open(in_file) as csvfile:
				csvreader = csv.reader(csvfile, delimiter=',')
				for row in csvreader:
					if ',' in row[1]:
						row[1] = row[1].replace(',', '')
					csvwriter.writerow(row)

	# 检查日期是否连续
	last_time = "2010/12/31"
	with open(out_file) as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',')
		for row in csvreader:
			if row[0] == "date":
				continue
			now_time = row[0]
			now_datetime = datetime.datetime.strptime(now_time, '%Y/%m/%d')
			last_datetime = datetime.datetime.strptime(last_time, '%Y/%m/%d')
			delta = (now_datetime - last_datetime).days

			if delta > 1:
				print(row)


			last_time = now_time
			


if __name__ == '__main__':
	# downloadControl()
	merge("bitcoin_daily.csv")



