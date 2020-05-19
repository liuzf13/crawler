#### 主要思路

> 本代码主要是从网上爬取不同数字货币的 unconfirmed transaction number 数据，爬取过程关注于每天的 unconfirmed tx 数量，但是不涉及具体的交易信息。
>
> 爬取过程主要有两个数据源：
>
> * [jochen的个人网站](https://jochen-hoenicke.de/queue/)：记录了 BTC、LTC、DASH、BSV、BCH 等货币的 unconfirmed tx number 信息
> * [blochchain.info](https://api.blockchain.info/charts/mempool-count?timespan=all&format=csv)：记录了 BTC 的 unconfirmed tx number 信息
>
> 对于 jochen 个人网站上的数据，主要是从后台的 js 直接获取数据（json），并进行解析。例如：
>
> ```LTC:   https://johoe.jochen-hoenicke.de/queue/litecoin/all.js```
>
> 对于 blockchain.info 的数据，直接访问 api 链接下载 csv 即可。但是要将系统设置为英文，网站无法解析 zh-cn。
>
> ```https://api.blockchain.info/charts/mempool-count?timespan=all&format=csv```
