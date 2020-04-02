#### 主要思路

> coinmarketcap 上货币的历史数据都是静态的，可以直接通过 etree + xpath 的方式进行爬取，还可以直接在 url 中指定数据的时间范围。例如，这是[bitcoin 的历史数据](https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20130429&end=20200402)。
>
> 爬取 coinmarketcap 所有货币历史数据的步骤主要分为两步
>
> * 获取所有货币的历史数据链接
> * 爬取每种货币的历史数据



#### 主要步骤

* 获取所有货币的历史数据链接

> 首先，[该网站](https://coinmarketcap.com/all/views/all/)展示了 coinmarketcap 上的所有货币，但是默认只加载 200 条，每次滚动条下滑到底，点击 load more，会继续加载新的货币。我们可以通过开发者模式中的 network 查看点击 load more 时后台执行的 request，如下图所示
>
> ​	![image](https://github.com/liuzf13/crawler/blob/master/images/coinmarketcap_request.jpg)
>
> 因此，我们可以通过发起这个 request url，以 json 的方式获得后台返回的货币信息，然后根据货币的 “slug” item 来构造其对应的历史数据 url 链接，并补充我们想查询的历史区间
>
> `coin_url = "https://coinmarketcap.com/currencies/" + item["slug"] + "/historical-data/?start=20130428&end=" + str(end_date)`
>
> 最后，把每个货币的历史数据链接保存下来，方便后续爬取数据



* 爬取每种货币的历史数据

> 通过 xpath 的方式获取历史数据，这里就比较简单了。
>
> ![image](https://github.com/liuzf13/crawler/blob/master/images/coinmarketcap_xpath.jpg)

