# crawler
### 这个 Repo 主要记录平时做的一些小爬虫



#### 1. 贴吧相关爬虫

爬取的内容主要是 [发帖时间、帖子标题、作者、作者 url、回帖数量、点击数、阅读数]等等，没有涉及到帖子的具体内容。

已完成的部分包括：

* [百度贴吧](https://tieba.baidu.com/)
* [链节点](https://www.chainnode.com/)
* [股吧](http://guba.eastmoney.com/)
* [天涯论坛](http://bbs.tianya.cn/)



#### 2. 数字货币相关爬虫

爬取的内容主要是数字货币的 price、volume、marketcap 等信息

已完成的部分包括：

* [coinmarketcap](https://coinmarketcap.com/)
* [cryptocompare](https://www.cryptocompare.com/)
* [yahoo finance](https://finance.yahoo.com/cryptocurrencies?all=&offset=0&count=150)
* [datamish](https://datamish.com/)
* [coincheckup](https://coincheckup.com/)
* [jochen's unconfirmed tx](https://jochen-hoenicke.de/queue/)
* [walletexplorer](https://www.walletexplorer.com/)



#### 3. 其他爬虫

已完成的部分包括：

* [google trend 谷歌趋势指数](https://trend.google.com/)
* [百度指数](http://index.baidu.com/v2/index.html)
* [百度风云榜](http://top.baidu.com/)
* [中国证券监督管理委员会IPO信息](http://eid.csrc.gov.cn/ipo/checkClick.action?choice=info)



---

#### 说明

* 爬虫的思路主要分为两类

  > 对于一些比较繁琐，有很多 js、ajax 脚本的网站（如百度指数），或者直接提供数据下载按钮的网站，如果能直接从后来看到调用 json 数据的 api 链接，就直接访问 api；否则采用 selenium 模拟浏览器爬取

  > 对于大部分是静态数据的页面，采用 etree + xpath 的方式进行爬取

* 网站经常会进行改版，因此爬虫需要阶段性更新（如百度指数，从2017开始更新过三个版本）

* 不同爬虫是不同阶段写的，因此**代码里的代码风格并没有统一**！暂时还没有批量修正，这也是需要反思的一点

* 目前也只是因为感兴趣，阶段性地接触了一些爬虫知识，希望后续能有机会系统性地看看相关书籍

