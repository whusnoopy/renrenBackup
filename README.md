# renrenBackup

A backup tool for renren.com


# 人人网信息备份工具

## 基本配置

依赖 Python 3.6.5+（其他版本我没测试过，因为用了 f-string，所以应该是要这个版本起跳）

```bash
pipenv --python 3.6.5
pipenv install
pipenv shell
```

在 `config.py` 里填入自己的人人 `uid`，后面抓取会用到，本地数据库也会用这个 id


## 抓取

自行登录人人后在 Chrome 调试工具里随便找个发往人人主站的请求，把 Cookie 弄下来填到 `COOKIE_STR` 里，然后执行命令即可自动抓取

```bash
python fetch.py
```


## 展示

直接运行命令，即可在 `localhost:5000` 上看到展示

```bash
python main.py
```


## Log

#### 2018-07-22

数据爬下来了怎么存也是个问题，打算用 sqlite，因为数据量也不大，但是裸操作 sqlite 还是太麻烦，搜了下 ORM，找到 peewee 这个库，研究了下怎么用

考虑爬取后的展示问题，打算用 flask 做服务，Vue.js 做前端，semantic-ui 做样式

把状态的获取都搞定了，包括

1. 所有状态信息。包括 点赞、分享、评论 数
2. 所有状态的前 8 个点赞人（人人只返回了前 8 个）
3. 所有状态的所有评论

并用 flask 做了展示，先没上 Vue.js，只是裸写了一顿，熟悉了下 semantic-ui 的逻辑


#### 2018-07-21

牙龈发炎折腾了快一周，拖稿了

研究了半天现在登录的加密，混淆过的 js 读的脑仁疼，先跑通再说，直接从 Chrome 的请求里把加密后的 `password` 和 `rkey` 拿出来，就可以登录得到可用的 session 了

第一步先拿状态列表

状态直接是通过 AJAX 请求拿回来一段 json，这个就方便很多了，看了下返回的数据结构，有用的大概如下（部分数据已模糊化）

```json
{
    "count": 999,           // 总共有多少条状态
    "doingArray": [         // 当前页的状态列表
        {
            "comment_count": 20,            // 评论数
            "content": "要的留邮箱",        // 内容
            "createTime": "1416289808000",  // 时间戳，后面还有个 dtime 用来显示，我们爬就不用了
            "id": 12345,                    // 编号，后续拿评论什么的都用的上
            "repeatCountTotal": 2,          // 转发数，还有个 repeatCount 不知道干嘛的（直接转发？）
            "rootContent": "谁有？",        // 转发原文（如果是转发，否则没这个和下面几个字段）
            "rootDoingUserId": 23456,       // 转发原用户 id
            "rootDoingUserName": "张三",    // 转发原用户名
        },
    ]
    "likeInfoMap": {        // 点赞信息，还有个 likeMap 不知道干嘛的，跟页面对比是这个有用
        "status_12345": 1,                  // 格式是 status_id，用上面的来找就行了
    }
}
```

每页 20 条，页码从 0 开始，所以最大页码就是 `Math.ceil(count/20) - 1`，一路翻过去就好

重新爬的时候发现调登录可能会遇上要输入验证码，不如直接从 Chrome 里把 cookie 拿出来更方便

#### 2018-07-12

试图直接从 Chrome 里拷 Cookie 出来用，没用成功，还是走一遍 login 好了。之前找的那几个都是用明文登录的方式，似乎现在都不行了，抓了下请求包，还没完全搞明白官方是怎么加密的，但是在浏览器里把 ajaxLogin 那个请求的 form data 扒出来，直接提交后就可以获取到正确的 requests.session

#### 2018-07-11

想起来自己的人人账号也好久没用了，说不定这个站哪天都不在了，等官方有导出工具还是别想了，自己来吧

找了一圈找到了如下几个备份工具，不过看说明从 2018 年某刻后都不能用了，自己学着改改看

* https://github.com/xinyu3ru/renren-bak
* https://github.com/threegirl2014/RenRenDownload
* https://github.com/kngxscn/backup-renren-status
