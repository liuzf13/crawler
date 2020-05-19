import sys
import datetime as dt
import json
import time
import os
import csv

def convert_timestamp_to_day(time_stamp):
    date_array = dt.datetime.fromtimestamp(time_stamp)
    new_time = date_array.strftime("%Y-%m-%d %H:%M:%S")
    # time_tuple = time.localtime(time_stamp)
    # new_time = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple)
    return new_time

def write_row_to_csv(data, file_name):
    with open(file_name, 'a+', newline="") as datacsv:
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        csvwriter.writerow(data)

if __name__ == "__main__":
    # 目标：爬取 https://jochen-hoenicke.de/queue/ 上货币的 unconfirmed tx daily 数据

    # 首先，手动加载 johoe 网站中几种货币的 all.js 数据，保存到 ./data/ 目录下
    # 可以采用 request.urlopen(url) 的方法进行加载数据，但是太慢了，而且经常访问失败
    # 获取 all.js 的方法：F12 进入开发者模式，观察点击 all 时 network 执行的 all.js，获取链接
    # BTC：  https://johoe.jochen-hoenicke.de/queue/all.js
    # LTC:   https://johoe.jochen-hoenicke.de/queue/litecoin/all.js
    # DASH:  https://johoe.jochen-hoenicke.de/queue/dash/all.js
    # BSV:   https://sv.jochen-hoenicke.de/queuesv/all.js
    # BCH:   https://johoe.jochen-hoenicke.de/queue/cash/all.js

    # 另一种BTC
    # BTC:   https://api.blockchain.info/charts/mempool-count?timespan=all&format=csv  （需要设置系统语言为英文）
    
    '''
    url = "https://johoe.jochen-hoenicke.de/queue/litecoin/all.js"
    resp = request.urlopen(url)
    result = resp.read().decode('utf-8')
    print(result)
    result = resp.read().decode('utf-8').replace("call(", "").replace(")", "").replace(" ", "").replace("\n", "").strip()
    print(result)
    result = result[:-2] + ']'
    print(result)
    print(type(result))
    print("-------------------------------------------------")
    result = json.loads(result)
    print(result)
    print(type(result))
    '''


    # 然后，加载数据，并将 str 转化为 dict 格式
    # 对于每个时间戳，将其转为日期格式，然后算出 tx 总和，写入结果文件
    path = "./data/"
    out_path = "./result/"
    symbol_list = ["BTC", "BCH", "BSV", "DASH", "LTC"]
    for symbol in symbol_list:
        file_name = path + symbol + ".txt"
        out_file_name = out_path + symbol + ".csv"
        if os.path.exists(out_file_name):
            print(symbol + " has been downloaded.")
            continue

        f = open(file_name)
        result = ""
        while True:
            line = f.readline().strip()
            if '(' in line or ')' in line:
                continue
            if not line:
                break

            # print(line)

            # 获取时间戳，并将时间戳转化为日期
            time_end_index = line.index(',')
            time_stamp = line[1:time_end_index]
            new_time = convert_timestamp_to_day(int(time_stamp))
            # print(time_stamp, new_time)

            # 获取代表 tx 数量的数组（第一个数组）
            # 并通过 json.loads() 将 str 转为 list
            tx_list = line[time_end_index + 1:line.index(']') + 1]
            tx_list = json.loads(tx_list)
            # print(tx_list, sum(tx_list))

            # print(time_stamp, new_time, sum(tx_list))

            # 保存结果
            data = [new_time, sum(tx_list)]
            write_row_to_csv(data, out_file_name)


