# 为什么要做这个

自己是人人（校内）的早期用户和重度用户，也曾经在人人网工作了快两年，在上面留下的牛逼的二逼的傻逼的记录也不少，现在看看总担心说不定这个站哪天都不在了，等官方有导出工具还是别想了，自己来吧

找了一圈找到了如下几个备份工具，不过看说明从 2017 年某个时刻后都不能用了（应该是登录时密码终于不是明文传），自己学着改改看

* https://github.com/xinyu3ru/renren-bak
* https://github.com/threegirl2014/RenRenDownload
* https://github.com/kngxscn/backup-renren-status


## 文档结构

后面的一系列说明不一定是按我做事的过程来，但是可以体现最后的解决问题思路，大概会涉及到的点包括

1. 登录：RSA，Cookie，请求信息，requests
2. 通用抓取：获取和拼接 URL，提取 json，重试，本地保存，翻页
    - 评论
    - 点赞
    - 图片保存到本地
3. 状态
4. 留言板：解析 HTML，正则匹配
5. 相册：从 HTML 里提取 json
6. 日志：解析 HTML
7. 存储：SQLite，peewee
8. 展示：flask，jinja，Semantic-UI

## 代码结构

```shell
.
├── config.py         # 配置文件
├── crawl             # 抓取模块
│   ├── album.py          # 抓相册
│   ├── blog.py           # 抓日志
│   ├── crawler.py        # 抓取器，封装相关接口，对上层透明重试等机制
│   ├── gossip.py         # 抓留言板
│   ├── status.py         # 抓状态
│   └── utils.py          # 抓图到本地、抓评论、抓点赞
├── doc               # 文档目录
├── fetch.py          # 抓取启动脚本
├── models.py         # 数据库表定义
├── Pipfile           # pipenv 配置文件
├── renren_bak.db     # 抓取后的本地存储 db
├── requirements.txt  # pip 需求文件
├── static            # 静态文件目录
│   ├── img               # 图片目录，抓到本地的图片存这里
│   ├── lock_red.gif      # 留言板悄悄话图标
│   ├── men_tiny.gif      # 默认头像
│   ├── mobile.gif        # 留言板手机评论图标
│   ├── scripts.js        # 展示页面脚本
│   └── styles.css        # 展示页面样式文件
├── templates         # flask-jinja 模板目录
│   ├── album.html        # 单个相册页
│   ├── album_list.html   # 相册列表页
│   ├── blog.html         # 日志详情页
│   ├── blog_list.html    # 日志列表页
│   ├── gossip_list.html  # 留言板
│   ├── index.html        # 首页
│   ├── layout.html       # 模板框架
│   ├── photo.html        # 照片详情页
│   └── status_list.html  # 状态页
└── web.py            # flask 展示脚本
```

## 未尽事宜

本来还想把分享抓下来，不过看了下请求，分享页面只有 HTTP 拿回来的 HTML，并没有 json 好拿，而且格式太多，有 日志、视频、相册、照片、链接 等，解析和展示都不方便

另外分享的本地评论不多，但全站评论抓起来规模就非常可观，特别是某些热门的内容（如果跳过抓头像，应该也还好？）

鉴于很多分享的原始内容也打不开了，就不管这个了（其实是懒加烦）
