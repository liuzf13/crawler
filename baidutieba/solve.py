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

# f = codecs.open('btc_tieba.csv', 'a+', 'utf_8_sig')
# writer = csv.writer(f)

# ff = codecs.open('post_time.csv', 'a+', encoding="gbk")
# time_writer = csv.writer(ff)

def write_row_to_csv(data, file_name):
	with open(file_name , 'a+' , newline = "", encoding="utf-8") as datacsv:
		csvwriter = csv.writer(datacsv, dialect = ("excel"))
		csvwriter.writerow(data)

# 获取百度贴吧数据，注意先不获取发帖时间，而是获取帖子的url，后续再访问url获取发帖时间
# btc贴吧中，pn += 50 为下一页
def get_tieba_data(base_url, pn, max_pn):
	url = base_url + str(pn)
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

	# 选择所有 class = j_thread_list clearfix 的 li 节点
	# 这些节点代表一个个帖子
	# http://www.imooc.com/article/46694
	data_table = html_data.xpath('//li[@class=" j_thread_list clearfix"]')

	print("data table len: ", len(data_table))

	for item in data_table:
		data = str(item.xpath('./@data-field')[0])
		data = json.loads(data)
		reply_num = data['reply_num']
		post_title = item.xpath('./div/div[2]/div[1]/div[1]/a/@title')[0].strip().replace(',', '')
		post_url = item.xpath('./div/div[2]/div[1]/div[1]/a/@href')[0].strip()
		author = data['author_name']
		author_url = item.xpath('./div/div[2]/div[1]/div[2]/span[1]/span[1]/a/@href')[0].strip().replace(',', '')
		data = [post_url, reply_num, post_title, author, author_url]
		# print(data)
		writer.writerow(data)

	pn += 50
	if pn > max_pn:
		return
	try:
		print("next pn: " + str(pn) + ", next url: " + base_url + str(pn))
		print("--------------------------------------------------------")
		get_tieba_data(base_url, pn, max_pn)
	except:
		print("error, exit")
		f.close()
		return

# 获取每个帖子的发帖时间
def get_post_time(i, url):
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
	headers = { 'User-Agent' : user_agent }
	req = Request(url, headers = headers)
	# print("request")
	with urlopen(req,timeout=60) as response:
		data = response.read()
	# print("response")
	data = data.decode("utf-8")
	html_data = etree.HTML(data)

	replys = html_data.xpath('//*[@id="j_p_postlist"]/div')
	post_time = ''
	for item in replys:
		data = str(item.xpath('./@data-field')[0])
		data = json.loads(data)
		post_time = data['content']['date'].strip().split()[0]
		
		print(i, url, post_time)
		time_writer.writerow([url, post_time])
		
		break

# 合并多进程发帖时间结果
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

# 部分帖子被删除掉了，需要按照发帖时间结果，对最初的帖子信息进行过滤
# 百度贴吧充满了重复的帖子。。。应该要在 post_info 基础上对重复的做一次筛选
# 爬 usd 和 stock 的时候要记得，这样还能减少待爬取的帖子数
def post_filter(post_time_file, post_info_file):
	legal_url_set = set([])
	with open("post_time_filter.csv", 'w' , newline = "") as datacsv:
		csvwriter = csv.writer(datacsv, dialect = ("excel"))

		with open(post_time_file) as csvfile:
			csv_reader = csv.reader(csvfile, delimiter=',')
			for row in csv_reader:
				url = row[0].replace("http://tieba.baidu.com", "")
				# print(url)
				if not url in legal_url_set:
					csvwriter.writerow(row)
					legal_url_set.add(url)

	print(len(legal_url_set))

	legal_post_info_url = set([])
	fff = codecs.open('post_info_filter.csv', 'a+', 'utf_8_sig')
	filter_writer = csv.writer(fff)
	with open(post_info_file, encoding="utf-8") as csvfile: 
		csv_reader = csv.reader(csvfile, delimiter=',')
		for row in csv_reader:
			url = row[2]
			if url in legal_url_set and not url in legal_post_info_url:
				legal_post_info_url.add(url)
				filter_writer.writerow(row)
	print(len(legal_post_info_url))
	fff.close()


# 汇总得到发帖数、回复数的时间序列
def merge_time_series(file_name, out_file_name):
	# day:[post_number, comment_number]
	result_dict = {}
	time_list = []
	with open(file_name, encoding="utf-8") as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=',')
		for row in csv_reader:
			if row[0] == "post_time":
				continue
			if not row[0] in result_dict:
				time_list.append(row[0])
				result_dict[row[0]] = [0, 0]
			result_dict[row[0]][0] += 1

			if not '万' in row[1]:
				result_dict[row[0]][1] += float(row[1])
			else:
				row[1] = row[1].replace('万', "")
				temp = float(row[1]) * 10000
				result_dict[row[0]][1] += temp


	with open(out_file_name , 'w' , newline = "", encoding="utf-8") as datacsv:
		csvwriter = csv.writer(datacsv, dialect = ("excel"))
		csvwriter.writerow(["time", "total_post_number", "total_comment_number"])
		for t in time_list:
			temp = [t]
			temp += result_dict[t]
			csvwriter.writerow(temp)


if __name__ == "__main__":
	# max pn: 70250
	# base_url = "https://tieba.baidu.com/f?kw=%E6%AF%94%E7%89%B9%E5%B8%81&ie=utf-8&pn="
	# pn = 48500
	# max_pn = 70250
	# get_tieba_data(base_url, pn, max_pn)

	# 获取帖子发帖时间
	# post_url_list = []
	# with open("post_url.csv") as csvfile:
	# 	csv_reader = csv.reader(csvfile, delimiter=',')
	# 	for row in csv_reader:
	# 		post_url_list.append(row[0])
	# print(len(post_url_list))
	# start_index = 989
	# for i in range(start_index, 6000):
	# 	url = post_url_list[i]
	# 	url = "http://tieba.baidu.com" + url
	# 	# print(url)
	# 	try:
	# 		get_post_time(i, url)
	# 	except:
	# 		# time.sleep(10)
	# 		# get_post_time(i, url)
	# 		time.sleep(5)
	# 		continue
	# ff.close()

	# 汇总多进程得到的发帖时间结果
	# merge_post_time(10, "btc_post_time.csv")

	# 按照 post_time 结果，再把帖子信息过滤一下。有一些被删掉了，或者禁止访问的
	# post_filter("post_time.csv", "post_info.csv")

	# 汇总得到发帖数和评论数的时间序列
	merge_time_series("btc_tieba_time_reply.csv", "btc_tieba_time_series.csv")
