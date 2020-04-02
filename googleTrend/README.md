#### 主要思路

谷歌趋势的爬取方式有两种，一种是采用 selenium 的方式访问 google trend 进行数据下载，另一种是通过后台 API 的方式进行访问。~~~两种方式都需要科学上网~~~

* selenium 访问谷歌趋势

> 通过 selenium 访问谷歌趋势，设置搜索的关键词、地区、区间范围，然后进行搜索。搜索完成后，直接点击图表右上角的 ”下载“ 按钮，下载 csv 数据
>
> ​    ![image](https://github.com/liuzf13/crawler/blob/master/images/google_trend_download.jpg)
>
> 这种方式同样适用于谷歌趋势主要城市热度的爬取，只需要修改一下 selenium 的点击目标即可
>
> 然而，**当时间跨度比较大时，这种方式下载到的数据粒度比较粗**。例如，当爬取过去 5 年的数据时，返回的图表是 weekly 的，超过 5 年则是 monthly 的。由于每张图表中最大值都是 100，粒度粗的时候，一些趋势值较小的时间点的数据会被缩放成 0。
>
> 



* API 访问数据

> 通过 pytrends API 进行数据访问，指定开始时间、结束时间后，对搜索词的历史数据进行分批次爬取，不同批次之间具有重复日期，从而进行数据的缩放。同时，也可以在函数中指定想要爬取的地区 geo (`pytrend.build_payload(kw_list=kw_list, timeframe = timeframe, geo=region)`)
>
> 这种方式可以获取到 daily 的数据，但是由于手动做了缩放，数据是小数值。缺点是 **API 访问较慢**
>
> 

