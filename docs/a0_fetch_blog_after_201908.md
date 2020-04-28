# 2019 年日志列表页和详情页 404 之后的思路

人人的 SNS 资产在 2019 年卖给了 Donews，从 2019 年 8 月开始，Web 日志列表页和日志详情页就 404 了，而且一直没有恢复的迹象，后来 Donews 发布了新的人人手机端应用，可以正常看到日志，说明数据没有丢

在 2020.04 经人提醒，日志可以通过如下的 URL 来看到摘要

> http://dnactivity.renren.com/index.html?p=601%2F30314%2F966126912

参数里 `%2F` 分隔的后两个字段分别是 `uid` 和 `blog_id`，虽然直接访问只能看到摘要，会被提示要打开 APP 查看全文，但实际打开看全文的 HTML 都吐出来了，用前端样式拦了下而已，只要想抓就能抓到

从请求来看，直接访问这个链接返回的只是 SPA 的框架部分，实际的全文是后面 POST 到 https://dnactivity.renren.com/api/blog/getBlogBody 的请求在获取，参数如下

```json
host_id: 30314
owner_id: 30314
blog_id: 966126912
time: 1588038712159
sign: 8b8c4a44a5931e6b919de8ebcddb3bd5128d2e97
```

里面那个 `sign` 按经验是个和参数相关的签名，这种一般都是把参数拼在一起加个 secret 做个 hash。扒了下混淆的 js 代码，可知 time 是用 `new Date().getTime()` 拿到的，就是当前时间的毫秒数，另外拼接和 hash 规则如下 Python 测试结果

```
>>> hashlib.sha1("blog_id=966126912&host_id=30314&owner_id=30314&time=1588038712159#1588038712159".encode()).hexdigest()
'8b8c4a44a5931e6b919de8ebcddb3bd5128d2e97'
```

至此，如果知道要抓谁的某篇特定日志就能直接抓，那么，前序问题就变成怎么获取用户的日志列表。在当前 Web 端日志列表页是 404 的情况下，似乎只能通过新鲜事页面来获取，新鲜事是动态加载的，看起来就是通过这个 GET 请求在拿

> http://www.renren.com/timelinefeedretrieve.do?ownerid=30314&render=0&begin=0&limit=30&year=2016&month=2&isAdmin=false

参数很直观，返回是拼装好了的 HTML，只要用 `href="http://blog.renren.com/GetEntry.do?id=([0-9]+)&owner` 的正则去判一下就能拿到 `blog_id`

这么看大体的逻辑就完整了，剩下就是体力劳动
