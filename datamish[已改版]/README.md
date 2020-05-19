#### 主要思路

> 通过查看后台的方式获取 datamish 上的数据来源（json），并进行解析处理。例如：
>
> ```symbolRateUrl = "https://datamish.com/api/datasources/proxy/1/query?db=bfx&q=SELECT%20mean(%22frr%22)%20FROM%20%22bfx_rates%22%20WHERE%20(%22symbol%22%20%3D%20%27" + symbol + "%27)%20AND%20time%20%3E%3D%201471141123854ms%20GROUP%20BY%20time(1d)%20fill(previous)%3BSELECT%20mean(%22last_price%22)%20FROM%20%22bfx_rates%22%20WHERE%20(%22symbol%22%20%3D%20%27" + symbol + "%27)%20AND%20time%20%3E%3D%201471141123854ms%20GROUP%20BY%20time(30d)%20fill(previous)&epoch=ms"```
>
> 不过202004 datamish 进行了一次改版，原来的代码似乎用不了了，后续有需求的话需要重写一个。

