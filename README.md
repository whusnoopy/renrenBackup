# renrenBackup

A backup tool for renren.com

# 人人网信息备份工具

## Log

TODO:
1. 存储带转发的状态
2. 获取状态评论
3. 状态评论可能翻页
4. 构建可读的状态页


#### 2018-07-22

数据爬下来了怎么存也是个问题，打算用 sqlite，因为数据量也不大，但是裸操作 sqlite 还是太麻烦，搜了下 ORM，找到 peewee 这个库，研究了下怎么用


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
