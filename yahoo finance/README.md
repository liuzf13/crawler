#### 主要思路

> yahoo finance 上每种货币都提供了历史数据的下载链接，我们要做的是获取到每种货币在 yahoo finance 上对应的链接，然后再获取下载历史数据的链接。这里直接采用 selenium  点击每个货币的历史数据上的 ”Download Data“ 进行下载

#### 主要步骤

* 获取所有货币的历史数据链接

> 首先，[该网站](https://finance.yahoo.com/cryptocurrencies?all=&offset=0&count=150)展示了 yahoo finance上的所有货币，我们可以通过 etree + xpath 的方式获取所有的货币，然后基于货币名称，加上我们需要的数据日期范围，构造得到每种货币的历史数据链接 ，例如 ：
>
> ```coinUrl = "https://finance.yahoo.com" + temp[0] + "/history?period1=1279296000&period2=" + str(end_time) + "&interval=1d&filter=history&frequency=1d```

* 爬取每种货币的历史数据

> 通过 selenium 模拟浏览器浏览每种货币的历史数据链接，然后点击 “Download Data”，下载 csv 格式的数据

