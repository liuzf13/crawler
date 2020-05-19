import requests
import time
import json
import os
import csv
import urllib.request as request
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from lxml import etree
from lxml import html

def get_tree(url):
    time.sleep(1)
    r = requests.get(url)
    root = html.fromstring(r.content)
    return root

def get_href(rt, filter):
    return [url for url in rt.xpath("//a/@href") if filter in url]

PATH = "data/"
try:
    os.makedirs(PATH)
except:
    pass


def getHrefs():
    main_page = get_tree("https://www.walletexplorer.com")
    hrefs = get_href(main_page,"/wallet/")
    hrefs = [i.replace("/wallet/","") for i in hrefs]
    return hrefs

def _get_address(name , p = 1, q= None):
    F = PATH + "{}_{}.json".format(name, p)
    if os.path.isfile(F) and p>1:
        return
    url = "https://www.walletexplorer.com/wallet/{}/addresses?page={}".format(name, p)
    root = get_tree(url)
    rows = root.xpath("//table//tr")
    ans = []
    for r in rows:
        tds = r.xpath("./td")
        if len(tds)>0 and (len(tds[0].xpath("./a"))>0):
            ans.append([tds[0].xpath("./a")[0].text.strip(), name]
            +[i.text.strip() for i in tds[1:]])
    json.dump(ans, open(F,"w"))
    if p<2:
        hrefs = get_href(root,"wallet/{}/addresses?page=".format(name))
        mp = p
        for i in hrefs:
            if int(i.split("=")[-1])>mp:
                mp = int(i.split("=")[-1])
        for i in range(p+1, mp+1):
            if q:
                q.put((name, i))

def writeToCsv(fileName, data):
    with open(fileName , 'a+' , newline = "") as datacsv:
        csvwriter = csv.writer(datacsv, dialect = ("excel"))
        csvwriter.writerow(data)


def getAddressUrl(names):
    doneList = []
    if os.path.exists("addressURL.csv"):
        with open("addressURL.csv") as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                doneList.append(row[0])

    print('totalExchanges:', len(names))
    count = 1
    for i in names:
        if i in doneList:
            print(i + " has been downloaded.")
            count += 1
            continue
        url = 'https://www.walletexplorer.com/wallet/' + i + '/addresses?page='
        tempUrl = url + '1'
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        headers = { 'User-Agent' : user_agent }
        req = Request(tempUrl, headers = headers)
        # print("request")
        with urlopen(req,timeout=60) as response:
            data = response.read()

        data = data.decode("utf8")
        htmlData = etree.HTML(data)
        allPages = htmlData.xpath('//*[@id="main"]/div[@class="paging"]/text()[1]')[0].split('/')[1].strip()
        data = [i, url, allPages]
        writeToCsv('addressURL.csv', data)
        
        print(data, count)
        count += 1

def getAddress(urlFile):
    with open(urlFile) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            PATH = "data/" + row[0] + '/'
            if not os.path.isdir(PATH):
                os.mkdir(PATH)
            maxPages = int(row[2])
            baseUrl = row[1]
            print("========================================================")
            print("Get addresses from " + row[0] + ", maxPages=" + str(maxPages))
            for i in range(1, maxPages + 1):
                fileName = PATH + str(i) + '.csv'
                if os.path.exists(fileName):
                    continue
                url = baseUrl + str(i)
                user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                headers = { 'User-Agent' : user_agent }
                req = Request(url, headers = headers)
                # print("request")
                try:
                    with urlopen(req,timeout=30) as response:
                        data = response.read()
                except:
                    time.sleep(30)
                    with urlopen(req,timeout=30) as response:
                        data = response.read()

                data = data.decode("utf8")
                htmlData = etree.HTML(data)
                dataTable = htmlData.xpath("//table//tr")
                # print(dataTable)
                for row in dataTable:
                    tds = row.xpath("./td")
                    if len(tds) > 0:
                        if len(tds[0].xpath("./a")) > 0:
                            address = tds[0].xpath('./a')[0].text.strip()
                            balance = tds[1].text.strip()
                            incomingTx = tds[2].text.strip()
                            lastUsdBlock = tds[3].text.strip()
                            data = [address, balance, incomingTx, lastUsdBlock]
                            writeToCsv(fileName, data)
                print(i)


def combine():
    filePath = "E:\\scrapy\\phoenixHealth\\code\\scapy\\newWalleteExplorar\\data\\"
    csvPath = "E:\\scrapy\\phoenixHealth\\code\\scapy\\newWalleteExplorar\\csv\\"
    dirList = os.listdir(filePath)
    for d in dirList:
        # if d != "SheepMarketplace":
            # continue

        # 把xx.old, xx-2等等合并起来
        exchange = d.lower().replace('.com', '').replace('.net', '').replace(".co.kr", '')
        for i in range(40, 1, -1):
            temp = "-old" + str(i)
            if temp in exchange:
                exchange = exchange.replace(temp, '')
                break
        if "-old" in exchange:
            exchange = exchange.replace("-old", '')
        if "-2" in exchange and exchange[-1] == '2':
            exchange = exchange.replace("-2", '')
        if "-output" in exchange:
            exchange = exchange.replace("-output", '')
        if "-cold2" in exchange:
            exchange = exchange.replace("-cold2", '')
        if "-cold" in exchange:
            exchange = exchange.replace("-cold", '')
        if "-incoming" in exchange:
            exchange = exchange.replace("-incoming", '')
        if "-original" in exchange:
            exchange = exchange.replace("-original", '')
        if "-chatbot" in exchange:
            exchange = exchange.replace("-chatbot", '')
        if "-hotwallet" in exchange:
            exchange = exchange.replace("-hotwallet", '')
        if "-pirateat40" in exchange:
            exchange = exchange.replace("-pirateat40", '')
        csvName = csvPath + exchange + ".csv"

        firstLine = ["address" , "balance" , "incoming txs" , "last used in block"]
        with open(csvName , 'a+', newline = "") as datacsv:
            csvwriter = csv.writer(datacsv, dialect = ("excel"))
            if not os.path.exists(csvName):
                csvwriter.writerow(firstLine)
            for file in os.listdir(filePath + d + "\\"):
                with open(filePath + d + "\\" + file) as csvfile:
                    readCSV = csv.reader(csvfile, delimiter=',')
                    try:
                        for row in readCSV:
                            csvwriter.writerow(row)
                    except:
                        print(file)
        print("solve " + d + " successfully.")


def compare():
    ourExchangeDict = {}
    csvPath = "E:\\scrapy\\phoenixHealth\\code\\scapy\\newWalleteExplorar\\csv\\"
    for file in os.listdir(csvPath):
        exchange = file.replace(".csv", '').lower().strip()
        print(file)
        if not exchange in ourExchangeDict:
            ourExchangeDict[exchange] = set([])
        with open(csvPath + file) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                if not row:
                    break
                if row[0] == "address":
                    continue
                # if not row[0] in ourExchangeDict[exchange]:
                ourExchangeDict[exchange].add(row[0])


    # for key in ourExchangeDict:
        # print(key)

    paperExchangeDict = {}
    with open("griffinData.csv") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if row[2] == "address":
                continue
            exchange = row[1].strip().lower()
            exchange = exchange.replace('.com', '').replace('.net', '').replace(".co.kr", '')
            if not exchange in paperExchangeDict:
                paperExchangeDict[exchange] = set([])

            # if not row[2] in paperExchangeDict[exchange]:
            paperExchangeDict[exchange].add(row[2])

            for key in ourExchangeDict:
                if row[2] in ourExchangeDict[key] and exchange != key:
                    print(row[2], exchange, key)

    # 看看论文数据，是否有exchange是我们之前没捕捉到的
    for exchange in paperExchangeDict:
        csvName = csvPath + exchange + ".csv"
        if not exchange in ourExchangeDict:
            with open(csvName , 'a+', newline = "") as datacsv:
                csvwriter = csv.writer(datacsv, dialect = ("excel"))
                for address in paperExchangeDict[exchange]:
                    csvwriter.writerow([address])
            # print(exchange, paperExchangeDict[exchange])
        else:
            for address in paperExchangeDict[exchange]:
                if not address in ourExchangeDict[exchange]:
                    writeToCsv(csvName, [address])


# 是否有地址属于多个exchange
def findRepeat():
    ourExchangeDict = {}
    exchangeList = []
    csvPath = "E:\\scrapy\\phoenixHealth\\code\\scapy\\newWalleteExplorar\\csv\\"
    for file in os.listdir(csvPath):
        exchange = file.replace(".csv", '').lower().strip()
        if not exchange in ourExchangeDict:
            ourExchangeDict[exchange] = set([])
            exchangeList.append(exchange)
        with open(csvPath + file) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                if not row:
                    break
                if row[0] == "address":
                    continue
                # if not row[0] in ourExchangeDict[exchange]:
                ourExchangeDict[exchange].add(row[0])

    for exchange in exchangeList:
        temp = ourExchangeDict[exchange]
        for exchange2 in exchangeList:
            if exchange == exchange2:
                continue
            temp2 = ourExchangeDict[exchange2]
            if len(temp & temp2) > 0 :
                print(exchange, exchange2, temp & temp2)

def countAddress():
    csvPath = "E:\\scrapy\\phoenixHealth\\code\\scapy\\newWalleteExplorar\\csv\\"
    griffinSet = set()
    ourSet = set()
    griffinNew = set()
    count = 0
    for file in os.listdir(csvPath):
        fileName = csvPath + file
        with open(fileName) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                if len(row) == 1:
                    count += 1
                    print(file.replace(".csv", ''))
                    break
                else:
                    break
    print(count)
    '''
    for file in os.listdir(csvPath):
        fileName = csvPath + file
        with open(fileName) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                if len(row) > 1:
                    ourSet.add(row[0])
                elif len(row) == 1:
                    griffinNew.add(row[0])


    with open("otherAddress.csv") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if row[0] == "group_name":
                continue
            griffinSet.add(row[2])

    print("Our address Num:", len(ourSet))
    print("Griffin address Num:", len(griffinSet))
    print("Repeat address Num:", len(griffinSet) - len(griffinNew))
    '''

def generateDatabase():
    originPath = "./csv/"
    samplePath = "./database/sample/"
    totalPath = "./database/total/"
    for file in os.listdir(originPath):
        fileName = originPath + file
        sampleList = []
        totalList = []
        with open(fileName) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=",")
            for row in readCSV:
                if not row:
                    break
                if len(row) == 1:
                    sampleList.append(row[0])
                totalList.append(row[0])
        totalOutFile = totalPath + file
        with open(totalOutFile , 'w' , newline = "") as datacsv:
            csvwriter = csv.writer(datacsv, dialect = ("excel"))
            for address in totalList:
                data = [address]
                csvwriter.writerow(data)

        sampleOutFile = samplePath + file
        with open(sampleOutFile , 'w' , newline = "") as datacsv:
            csvwriter = csv.writer(datacsv, dialect = ("excel"))

            if len(sampleList) >= 10:
                for i in range(10):
                    data = [sampleList[i]]
                    csvwriter.writerow(data)
            else:
                for address in sampleList:
                    data = [address]
                    csvwriter.writerow(data)
                for i in range(10 - len(sampleList)):
                    try:
                        data = [totalList[i]]
                        csvwriter.writerow(data)
                    except:
                        break
        print("solve" + file + "successfully.")



if __name__ == "__main__":
    # 第一步，爬取walletExplorar所有Exchange的Address URL，存储到addressURL.csv
    # 每个exchange的address URL有一个最大页数，需要遍历 page=1 --> page=maxPage
    # urls = getHrefs()
    # getAddressUrl(urls)

    # 第二步，爬取每个Exchange的每页Address数据
    # 数据格式："address, balance, incoming Tx, last used Block"
    # fileName = input('Please input url file.')
    # getAddress(fileName)

    # 第三步，合并数据，每个交易所合并为一个csv
    # combine()
