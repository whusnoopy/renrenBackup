# 展示

一开始只是保证能展示出来，先用自己比较熟悉的 Flask 弄，前端也懒得写样式，之前自己用 Bootstrap 比较多，这次想换个口味，用 semantic-ui 试试看

期望的结果是可以用 Flask 输出可本地跳转的页面，最后把页面都吐到一个目录，加上 `static` 目录一起打包就可以脱离 Python 环境直接查看

另外个人想做的事情是把数据都用 RESTful 吐，前端用 Vue.js 做，不过这个没那么重要，更多的当个人爱好做


## Flask 框架

把页面结构想好，路由表一搭就出来了

```shell
/index                          # 首页，已抓取用户列表
├── /<uid>/status/page/<page>       # 用户 uid 的状态 page 列表页
├── /<uid>/blog/page/<page>         # 用户 uid 的日志 page 列表页
│   └── /blog/<blog_id>                 # blog_id 日志详情页
├── /<uid>/album/page/<page>        # 用户 uid 的相册 page 列表页
│   └── /album/<album_id>               # album_id 相册详情页
│       └── /photo/<photo_id>y              # photo_id 照片详情页
├── /<uid>/gossip/page/<page>       # 用户 uid 的留言板 page 列表页
├── /comments/<entry_id>            # 实体 entry_id 的评论和点赞信息
```

一开始没考虑抓多人的问题，后面有了抓多人和展示多人的需求后，怎么识别当前要加载的用户就有很多搞法了。一是在 URL 里强行加 uid 信息，但这个在照片详情页不好加，做起来也比较丑；二是用 Session 维护一下，这个麻溜的用 `app.before_request` 搞起来就是了

把展示时的翻页逻辑整合成了一个 Jinja 的 macro，也不用到处复制粘贴重复代码


## 评论和点赞信息展示

对于评论和点赞信息，大部分页面是有详情页可以承载的，这个在最后吐详情页时一并吐出，方便直接在 flask 的 jinja 模板引擎直接输出

对于没有详情页的状态列表，采用 xhr 请求去拿的方式去实时获取，并用 popover 的方式展示。如果想实现纯静态输出，这个地方也考虑先 jinja 输出，只是隐藏显示，前端用 js 只控制展示与否

对于有详情页但是还有上一级列表页的相册和日志，在列表页也采用了跟状态一样的处理方式。纯静态输出下这个可以只展示数字而不展示详情，反正也要点进去才可以看

留言板每个实体没有额外的评论和点赞信息，没有这个烦恼


## semantic-ui

之前都用 Bootstrap，换 semantic-ui 其实还是有挺多不适应，也跟自己没深入使用有关。主要用到了里面的

* `menu` 导航
* `feed` 各种状态、对话列表
* `list-pagination` 各处翻页
* `popover` 弹出框，展示状态的评论

其他 `divider` 和 `segment` 等排版组件就看着用了

有部分组件的样式有诡异默认设定，需要强行覆盖一下


## RESTful + Vue.js

从学习和炫技的角度出发，还是可以搞前后端分离，也去学下 Vue.js 。不过暂时先跳过这个，回头有空再说
