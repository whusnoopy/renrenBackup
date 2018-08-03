# 处理登录

试图直接从 Chrome 里拷 Cookie 出来用，没用成功，还是走一遍 login 好了。之前找的那几个都是用明文登录的方式，似乎现在都不行了，抓了下请求包，还没完全搞明白官方是怎么加密的，但是在浏览器里把 ajaxLogin 那个请求的 form data 扒出来，直接提交后就可以获取到正确的 requests.session

研究了半天现在登录的加密，混淆过的 js 读的脑仁疼，先跑通再说，直接从 Chrome 的请求里把加密后的 `password` 和 `rkey` 拿出来，就可以登录得到可用的 session 了

重新爬的时候发现调登录可能会遇上要输入验证码，不如直接从 Chrome 里把 cookie 拿出来更方便

抓图的时候偶尔可能会 ConnectionError，果断把超时和重试机制给加上

不死心，还是想搞定登录，其实这个应该就是用某个第三方库做了下 AES 之类的加密，爬一下请求过程吧

把 http://s.xnimg.cn/a89037/nx/apps/login/login.js 给拿下来并做格式化并分析

1. 第一步是在 865 行，DOM ready 后调 554 行的 `Window.getKeys`，向 "key.jsp?generateKeypair=true" 发一个请求申请服务端生成 key
2. 然后调 389 行的 `cryption.getKeys`，向 http://login.renren.com/ajax/getEncryptKey 发请求获得一个 json
3. 把里面的 `rkey` 保留下来，回头真正登录时要带上这个参数。用里面的 `e`, `n`, `maxdigits` 几个参数生成一个 rsa_key `T`。基本可以参考 http://aiddroid.com/javascript-rsa-encryption/ 里的代码 797 行，对应的 `.e` 是里面的 `factor`，`.n` 是里面的 `key`
4. 最终触发登录操作的是 560 行的 `onsubmit`，里面的 u 对应的是前面拿到的 rkey，所以必然会执行后面的两个 encrypt，对应的调用时 410 行，把输入的 `e` 跟之前生成的 rsa_key `T` 一起去加密，分别是把邮箱和密码加密，然而最后的提交 507 行的 `s()` 里只用了 `c`，也就是密码加密后的串

看了一下就是用的上面 aiddroid 里的那个算法，把加密部分看懂了后，密码不会超长，所以直接就是把密码按字节从左到右映射到大数 x 上，然后做 x**e % n 再转成 16 进制就是要的加密密码了

另外吐槽下登录的 URL，参数里带了个时间戳，但是这个戳不是用的实际任何一种语言的 timestamp，而是自己构建了一套，并且中间有些字段是缺失的（比如没有 `day_of_month` 但有 `day_of_week`，也没有分钟数），也不保证等长（上午 9 点就是 9，晚上九点就是 21），还好现在 Py3.6+ 有模板字符串可以直接填

把抓取的入口优化了下，用户名密码在抓的时候再输，免得要去改 config 还可能不小心提交到 git 上去