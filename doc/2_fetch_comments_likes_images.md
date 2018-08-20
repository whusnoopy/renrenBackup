# 通用的抓取部分

人人的状态、日志等，每一个实体（entry）都可能有自己的评论（comment）、点赞（like）信息，而且都是从统一的出口走，那就做通用的处理好了


## 评论抓取

人人的评论获取接口是个标准的 xhr 请求，在浏览器里多翻几个页面试试看，搞明白参数变化就行了

请求参数

```python
param = {
    "entryOwnerId": owner,          # 实体所有者的 uid
    'entryId': entry_id,            # 实体 id
    'type': entry_type,             # 实体类型，status/album/photo/blog
    'replaceUBBLarge': 'true',
    'limit': config.ITEMS_PER_PAGE, # 单页条数
    'offset': 0                     # 偏移位置，从几条开始拿，开始是 0
}
```

拿回来的信息里有用的部分

```python
ret = {
    'commentTotalCount': 8,         # 该实体的评论总条数
    'comments': [
        {
            'authorId': xxx,        # 评论者 uid
            'authorName': xxx,      # 评论者的用户名
            'authorHeadUrl': xxx,   # 评论者头像图片地址
            'createTimeMills': xxx, # 评论时间戳，注意是 js 的时间戳，python 里用要 /1000
            'content': xxx,         # 评论内容
        }
    ]
}

```

人人的评论分当前评论和全站评论，当前评论就是当前实体下的，全站评论是原实体被转发分享后在转发的下面的评论。很多好玩的回复都在全站评论里，还是考虑抓个全站评论。看了下请求，就是换了个地址，其他参数什么的全一样，直接加个参数区分就好


## 点赞抓取

人人的点赞数在获取实体信息时在实体里有正确保存，通过 xhr 请求去拿对应的点赞名单时，当前只返回最近的最多 8 个人，这个问题我在 2013 年碰上改版时就吐槽过（详见 http://status.renren.com/status/v7/30314/4953969997 ），然而现在也并没有给出来

请求参数

```python
param = {
    "stype": entry_type,            # 实体类型，见上
    "sourceId": entry_id,           # 实体 id
    "owner": owner,                 # 实体所有者的 uid
    "gid": '{entry_type}_{entry_id}'.format(entry_type=entry_type, entry_id=entry_id),
    "uid": crawler.uid              # 当前浏览者的 uid
}
```

拿回来的信息里有用的部分

```python
ret = {
    'likeList': [
        {
            'id': uid,              # 点赞人的 uid
            'name': name,           # 点赞人的用户名
            'headUrl': url,         # 点赞人头像图片地址
        }
    ]
}
```

保存的时候就只要记录 `entry_id <-> uid` 的映射关系就好


## 图片抓取

处理展示的时候发现很多图片加载不出来，看了下应该是不允许跨域调用，还是得把有跨域限制的图片爬到本地来

排查发现会挂的图有这么几个来源

1. 留言板的头像
2. 留言板的附件
3. 评论和点赞的用户头像（其实跟 1 差不多，不过 1 里面是留言相关的，不是用户最新头像）
4. 相册封面（其实是相册里的某张照片）
5. 照片（有多个尺寸，取最大的在本地实时压缩展示好了）

域名也存在好几个，并没有发现什么规律

干脆都存到本地，并保持目录结构，映射规则就是 `http://xx.xxx.cn/aa/bb/cc/dd.gif` -> `/static/img/xx_xxx_cn/aa/bb/cc/dd.gif`，抓的时候去一下重，节省网络开销，然后把本地的展示直接替换就可以了

正文里的表情和留言板的礼物什么的看了下还不会被跨域封，替换起来比较麻烦，先不处理


## 用户头像

前面评论和点赞里都用到了用户名和用户头像，这部分数据可以提取出来公用，单独开了个 `User` 表来记录，并把用户头像替换成本地地址

```python
User = {
    'uid': uid,
    'name': name,
    'headUrl': url
}
```
