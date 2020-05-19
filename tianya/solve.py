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
import codecs

f = codecs.open('post_info.csv', 'a+', 'utf_8_sig')
writer = csv.writer(f)

ff = codecs.open('post_url.csv', 'a+', encoding="gbk")
url_writer = csv.writer(ff)

fff = codecs.open('post_time.csv', 'a+', encoding="gbk")
time_writer = csv.writer(fff)

def write_row_to_csv(data, file_name):
	with open(file_name , 'a+' , newline = "", encoding="utf-8") as datacsv:
		csvwriter = csv.writer(datacsv, dialect = ("excel"))
		csvwriter.writerow(data)


def write_row_to_txt(data, file_name):
	with open(file_name, 'a+') as txtfile:
		for i in range(len(data) - 1):
			txtfile.write(data[i])
			txtfile.write(',')
		txtfile.write(data[-1])
		txtfile.write('\n')


def get_tianya_data(url, page_num):
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
	data_table = html_data.xpath('//*[@id="main"]/div[7]/table/tbody/tr')
	print("data table len: ", len(data_table) - 1)
	# with open("tianya.txt", 'a+', encoding='utf-8') as txtfile:

	for i in range(1, len(data_table)):
		item = data_table[i]
		post_title = item.xpath('./td[1]/a/text()')[0].strip().replace(',', '')
		if post_title == '':
			continue
		post_url = item.xpath('./td[1]/a/@href')[0].strip()
		author = item.xpath('./td[2]/a/text()')[0].strip().replace(',', '')
		author_url = item.xpath('./td[2]/a/@href')[0].strip()
		read_num = item.xpath('./td[3]/text()')[0].strip()
		comment_num = item.xpath('./td[4]/text()')[0].strip()
		data = [post_url, read_num, comment_num, post_title, author, author_url]
		# print(data)
		writer.writerow(data)
		url_writer.writerow([post_url])
		# write_row_to_csv([post_url], "post_url.csv")
	
	next_page_url = "http://bbs.tianya.cn"
	try:
		if page_num == 1:
			next_page_url += html_data.xpath('//*[@id="main"]/div[8]/div/a[2]/@href')[0]
		else:
			next_page_url += html_data.xpath('//*[@id="main"]/div[8]/div/a[3]/@href')[0]
		page_num += 1
		print("next page: " + str(page_num) + ", next url: " + next_page_url)
		print("--------------------------------------------------------")
		get_tianya_data(next_page_url, page_num)
	except:
		print("error, exit")
		f.close()
		ff.close()
		return


def get_post_time(i, url):
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
	info = html_data.xpath('//div[@class="atl-info"]')
	if len(info) == 0:
		time_element = html_data.xpath('//div[@class="q-info"]')
		post_time = time_element[0].xpath('./span[2]/text()')[1].strip().split()[0].split('：')[1]
	else:
		time_element = html_data.xpath('//div[@class="atl-info"]')
		post_time = time_element[0].xpath('./span[2]/text()')[0].split(' ')[0].split('：')[1]

	# if "-1-1" in url:
	# 	time_element = html_data.xpath('//div[@class="q-info"]')
	# 	post_time = time_element[0].xpath('./span[2]/text()')[1].strip().split()[0].split('：')[1]
	# else:
	# 	time_element = html_data.xpath('//div[@class="atl-info"]')
	# 	post_time = time_element[0].xpath('./span[2]/text()')[0].split(' ')[0].split('：')[1]
	
	print(i, url, post_time)
	time_writer.writerow([url, post_time])
	# write_row_to_csv([url, post_time], "post_time.csv")


def merge_post_time(file_num, out_file_name):
	with open(out_file_name , 'w' , newline = "") as datacsv:
		csvwriter = csv.writer(datacsv, dialect = ("excel"))
		file_list = ["post_time.csv"]
		for i in range(2, file_num + 1):
			temp = "post_time" + str(i) + ".csv"
			file_list.append(temp)
		print(file_list)

		for file in file_list:
			with open(file) as csvfile:
				csv_reader = csv.reader(csvfile, delimiter=',')
				for row in csv_reader:
					csvwriter.writerow(row)

'''
汇总天涯数据，生成总发帖数、总阅读数、总评论数时间序列
'''
def merge_time_series(file_name, out_file_name):
	# day:[post_number, read_number, comment_number]
	result_dict = {}
	time_list = []
	with open(file_name) as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=',')
		for row in csv_reader:
			if row[0] == "post_time":
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




if __name__ == "__main__":
	# 天涯论坛中，下一页的链接id是由当前页最后一条帖子的时间戳决定的
	# 由于网页上最后一页帖子时间不显示秒，无法直接转换时间戳获取id（小时+分钟，转换不准）
	# 所以我们在爬取数据的时候，获取完帖子信息，还要从“下一页”按钮拿到下一页的链接，然后再次爬取
	# 注意，论坛也是按回复排序的。我们需要获取每个帖子的 url，然后进入每个帖子，获取发帖时间
	
	# 股票相关
	# 获取帖子信息
	# get_tianya_data("http://bbs.tianya.cn/list.jsp?item=1179&nextid=1539437116000", 1526)

	# 获取帖子发帖时间
	# post_url_list = []
	# with open("post_url.csv") as csvfile:
	# 	csv_reader = csv.reader(csvfile, delimiter=',')
	# 	for row in csv_reader:
	# 		post_url_list.append(row[0])
	# print(len(post_url_list))
	# start_index = 27835
	# for i in range(start_index, 30000):
	# 	url = post_url_list[i]
	# 	url = "http://bbs.tianya.cn" + url
	# 	# print(url)
	# 	try:
	# 		get_post_time(i, url)
	# 	except:
	# 		time.sleep(10)
	# 		get_post_time(i, url)
	# fff.close()

	# 汇总多进程得到的发帖时间结果
	# merge_post_time(5, "btc_post_time.csv")

	# 汇总时间序列
	file_name = "bitcoin_tianya.csv"
	out_file_name = "bitcoin_tianya_time_series.csv"
	merge_time_series(file_name, out_file_name)