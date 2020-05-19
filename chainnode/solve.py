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


def write_row_to_csv(data, file_name):
	with open(file_name , 'a+' , newline = "") as datacsv:
		csvwriter = csv.writer(datacsv, dialect = ("excel"))
		csvwriter.writerow(data)


'''
获取chainnode数据
@base_url：基本的 url
@pages：数据总共多少页
@page_item：每一页合法条数
@outfile：输出文件名
'''
def get_chainnode_time_series(base_url, pages, page_item, outfile):
	# with open(out_file , 'w' , newline = "", encoding='utf-8') as datacsv:
	# 	csvwriter = csv.writer(datacsv, dialect = ("excel"))
	# 	csvwriter.writerow(["time", "read_num", "comment_num", "title", "author", "author_url"])
	with open(out_file, 'a') as txtfile:
		for page in range(1, pages + 1):
			url = base_url + str(page)

			user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
			headers = { 'User-Agent' : user_agent }
			req = Request(url, headers = headers)
			# print("request")
			with urlopen(req,timeout=60) as response:
				data = response.read()
			# print("response")
			data = data.decode("utf8")
			# print(data)
			html_data = etree.HTML(data)
			# print(html_data)

			if page == 1:
				data_table = html_data.xpath('//*[@id="app"]/div[2]/div/div[2]/div/div[1]/section[2]/div[2]/div[3]/div')
			else:
				data_table = html_data.xpath('//*[@id="app"]/div[2]/div/div[2]/div/div[1]/section[2]/div[2]/div[1]/div')

			for item in data_table:
				post_title = item.xpath('./div/div[2]/div[1]/h3/a/text()')[0].strip().replace(',', '')
				post_time = item.xpath('./div/div[2]/div[2]/div[1]/time/@datatime')[0].strip().split('T')[0]
				read_num = item.xpath('./div/div[2]/div[2]/div[2]/span[1]/text()')[0].strip()
				comment_num = item.xpath('./div/div[2]/div[2]/div[2]/span[2]/text()')[0].strip()
				
				try:
					author = item.xpath('./div/div[2]/div[2]/div[1]/a[1]/text()')[0].strip().replace(',', '')
					author_url = item.xpath('./div/div[2]/div[2]/div[1]/a/@href')[0].strip().replace(',', '')
				except:
					author = "None"
					author_url = "None"

				print(post_title, post_time, read_num, comment_num, author, author_url)
				data = [post_time, read_num, comment_num, post_title, author, author_url]
				for i in range(len(data) - 1):
					txtfile.write(data[i])
					txtfile.write(',')
				txtfile.write(data[-1])
				txtfile.write('\n')
				# csvwriter.writerow(data)
				# write_row_to_csv(data, out_file)

			print("---------------------page " + str(page) + " ending-----------------------")
			# time.sleep(1)



'''
汇总chainnode数据，生成总发帖数、总阅读数、总评论数时间序列
'''
def merge_time_series(file_name, out_file_name):
	# day:[post_number, read_number, comment_number]
	result_dict = {}
	time_list = []
	with open(file_name) as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=',')
		for row in csv_reader:
			if row[0] == "time":
				continue
			if not row[0] in result_dict:
				time_list.append(row[0])
				result_dict[row[0]] = [0, 0, 0]
			result_dict[row[0]][0] += 1

			if not '万' in row[1]:
				result_dict[row[0]][1] += float(row[1])
			else:
				row[1] = row[1].replace('万', "")
				temp = float(row[1]) * 10000
				result_dict[row[0]][1] += temp

			if not '万' in row[2]:
				result_dict[row[0]][2] += float(row[2])
			else:
				row[2] = row[2].replace('万', "")
				temp = float(row[2]) * 10000
				result_dict[row[0]][2] += temp

	with open(out_file_name , 'w' , newline = "") as datacsv:
		csvwriter = csv.writer(datacsv, dialect = ("excel"))
		csvwriter.writerow(["time", "total_post_number", "total_read_number", "total_comment_number"])
		for t in time_list:
			temp = [t]
			temp += result_dict[t]
			csvwriter.writerow(temp)


'''
获取股吧用户数据，包括影响力、吧龄、关注、粉丝、总访问股吧次
'''
def get_guba_uesr_info(user, user_url, star_dict):
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
	headers = { 'User-Agent' : user_agent }
	req = Request(user_url, headers = headers)
	# print("request")
	with urlopen(req,timeout=60) as response:
		data = response.read()
	# print("response")
	data = data.decode("utf8")
	# print(data)
	htmlData = etree.HTML(data)
	# print(htmlData)
	influence_star = star_dict[htmlData.xpath('//*[@id="influ_star"]/@class')[0]]
	register_year = htmlData.xpath('//*[@id="others"]/div/div[1]/div[2]/div[1]/div[2]/p[2]/span/text()')[0]
	follows = htmlData.xpath('//*[@id="tafollownav"]/p/span/text()')[0]
	fans = htmlData.xpath('//*[@id="tafansa"]/p/span/text()')[0]
	totoal_visit_number = htmlData.xpath('//*[@id="others"]/div/div[1]/div[2]/div[3]/p[1]/span[1]/text()')[0]
	
	return [user, influence_star, register_year, follows, fans, totoal_visit_number]


# 获取用户数据
def get_info(file_name, out_file_name, star_dict):
	user_url_dict = {}
	with open(file_name, encoding="utf-8") as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=',')
		for row in csv_reader:
			if row[0] == "time":
				continue

			if not row[5] == "none":
				user_url_dict[row[4]] = row[5]
	# print(user_url_dict, len(user_url_dict))


	solved_url_set = set([])
	solved_file = out_file_name.replace(".csv", "_solved.csv")
	bad_info_file = out_file_name.replace(".csv", "_bad_info.csv")
	if os.path.exists(solved_file):
		with open(solved_file, encoding="utf-8") as csvfile:
			csv_reader = csv.reader(csvfile, delimiter=',')
			for row in csv_reader:
				solved_url_set.add(row[0])

	print(solved_url_set)



	write_row_to_csv(["user", "影响力", "吧龄", "关注", "粉丝", "总访问"], out_file_name)
	for user in user_url_dict:
		user_url = user_url_dict[user]
		print("Going to parse " + user + "  " + user_url)

		if user_url in solved_url_set: 
			# print(user + " " + user_url + " has been solved.")
			continue
		solved_url_set.add(user_url)
		
		# 用户可能已注销
		# 如 http://i.eastmoney.com/3179094302573106 一梦千年等一回
		try:
			user_info = get_guba_uesr_info(user, user_url, star_dict)
			write_row_to_csv(user_info, out_file_name)
			write_row_to_csv([user_url], solved_file)
			# print("get user info from " + user + " " + user_url + " successfully.")
		except:
			print("Bad info" + user + " " + user_url)
			write_row_to_csv([user_url], bad_info_file)



if __name__ == "__main__":
	# 由于数据存在中文，utf-8 存储为 csv 后，需要手动导入到 excel，从而显示正常编码

	# bitcoin
	base_url = "https://www.chainnode.com/forum/1-"
	pages = 323
	page_item = 35
	out_file = "chainnode_bitcoin.txt"
	# get_chainnode_time_series(base_url, pages, page_item, out_file)
		
	# merge guba time series
	file_name = "chainnode_bitcoin.csv"
	out_file_name = "chainnode_bitcoin_time_series.csv"
	merge_time_series(file_name, out_file_name)

	# get user info
	# star_dict = {"stars0":0, "stars05":0.5, "stars1":1, "stars15":1.5, "stars2":2, "stars25":2.5, "stars3":3, 
	# "stars35":3.5, "stars4":4, "stars45":4.5, "stars5":5}

	# file_name = "USD.csv"
	# out_file_name = "USD_userinfo.csv"

	# get_info(file_name, out_file_name, star_dict)