# 日志

跟状态、留言板类似，进入日志列表页看不到 xhr 请求，一翻页就看到，还是直接拿 xhr 请求从第一页开始拿

列表页的返回大致如下

```python
ret = {
    "count": count,                 # 总的日志数
    "data": [
        {
            "createTime": ctime,    # 发表时间，格式是 "%y-%m-%d %H:%M:%S"
            "category": category,   # 类型，我们请求的时候没管类型全都拿下来了
            "title": title,         # 日志标题
            "summary": summary,     # 日志摘要，在列表页显示的部分
            "commentCount": ccount, # 评论数
            "shareCount": scount,   # 转发数
            "likeCount": lcount,    # 点赞数
            "readCount": rcount,    # 阅读数
        }
    ]
}
```


## 日志正文解析

日志详情页不是 ajax 请求来的，也不知道怎么构建

看了下 HTML 格式，直接裸抓。人人吐出来的 HTML 日志内容部分在一行，那就摸那一行，连正则都不用，直接 find 就可以搞定

只是有坑的地方是人人 `\r` 和 `\n` 乱用，在浏览器调试工具里看 Network 请求里的 response 看不出来，一开始多抓了一部分无效内容，后面分清楚就好了


## 日志点赞信息

抓日志正文页的时候看评论还是 xhr 请求来的，直接用通用抓取部分去拿了

但是没看到取点赞名单的请求，不想裸解析 HTML，按原来的 URL 和格式猜了个点赞请求，直接能拿到，完美
