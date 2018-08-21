# 处理登录

抓取使用 `requests` 这个库，既然要抓，就会涉及到权限，怎么获取一个正常可用的会话来抓


## 绕行法

在 Chrome （其他浏览器也可以）里拿自己账号登录人人，然后看 `renren.com` 域名下的请求，把请求头里的 Cookie 拷贝出来，转化成 Python 的 dict，再传给 `requests` 用，直接可用

直接登录的话，在 2017 年某个时间点之前是明文账号密码登录的，后面改了，但是直接把 `ajaxLogin` 这个请求的 form data 拷出来，主要是加密后的 `password` 和 `rkey` 这两个参数，用自己的 `requests.session` 重放一次也是可以得到可用的会话


## 破解加密模拟登陆

摸 Cookie 还是太麻烦了，而且对使用者的知识要求有点高，还是走模拟登陆的方法

这里就是各种混淆 js 的反向工程了，找 `ajaxLogin` 这个请求是哪里发出来的，摸回去摸到 http://s.xnimg.cn/a89037/nx/apps/login/login.js 给拿下来，做格式化并分析

1. 第一步是在 865 行，DOM ready 后调 554 行的 `Window.getKeys`，向 `key.jsp?generateKeypair=true` 发一个请求申请服务端生成 key
2. 然后调 389 行的 `cryption.getKeys`，向 http://login.renren.com/ajax/getEncryptKey 发请求获得一个 json
3. 把里面的 `rkey` 保留下来，回头真正登录时要带上这个参数。用里面的 `e`, `n`, `maxdigits` 几个参数生成一个 rsa_key `T`
4. 最终触发登录操作的是 560 行的 `onsubmit`，里面的 u 对应的是前面拿到的 rkey，所以必然会执行后面的两个 encrypt，对应的调用时 410 行，把输入的 `e` 跟之前生成的 rsa_key `T` 一起去加密，分别是把邮箱和密码加密，然而最后的提交 507 行的 `s()` 里只用了 `c`，也就是密码加密后的串，用户名并没有用

这里找到是 RSA 加密也是各种试，先去搜前端登录表单加密一般怎么加，找到的都是说用 AES 或 RSA 加密。期间找到代码 http://aiddroid.com/javascript-rsa-encryption/ ，对比看了下应该就是这个加了混淆， 人人代码里生成 rsa_key 的部分对应这里代码 797 行，参数映射人人的 `.e` 是这里的 `factor`，`.n` 是这里的 `key`

搞明白了加密算法，就想着在 Python 里怎么复现。一开始想用库，但是不知道怎么把这些参数映射上去，感觉 Python 库都不是这么用的。然后想本地跑 js 源码，看了下要在 Python 里跑 js 又要引入一堆依赖，不如直接自己实现。先按源码去挨个抄，后来看这就是个标准 RSA 算法啊，aiddroid 上面那么多行代码，第一块是个 js 实现的高精度计算库，第二块是怎么基于高精度做快速的幂模等计算，第三块很少一点才是 RSA。而且人人的 maxdigits 限制了宽度，就只有一个 block 需要计算

用简洁的语言描述，就是把密码按字节从左到右映射到大数 x 上，然后做 (x^e)%n 再转成 16 进制就是要的加密密码了。Python 原生支持高精度计算，而且像这种幂模操作都有特定的函数，写起来不要太爽，一句话 `crypt = pow(pass, enc, mod)` 就搞定了

另外吐槽下登录的 URL，参数里带了个时间戳，但是这个戳不是用的实际任何一种语言的 timestamp，而是自己构建了一套，并且中间有些字段是缺失的（比如没有 `day_of_month` 但有 `day_of_week`，也没有分钟数），也不保证等长（上午 9 点就是 9，晚上九点就是 21），还好现在 Py3.6+ 有模板字符串可以直接填，不过为了兼容 py2，还是用 str.format 去填了


## 验证码

如果短时间登录过于频繁，会被要求输验证码

人人用的是四个汉字的验证码，懒得去新引入 OCR 库，直接在需要验证码的时候，把验证码图片保存到本地，然后提示人工输入好了

这里有个小坑是怎么在命令行运行时让用系统查看工具打开这个图，如果是在 Windows 下用 WSL 似乎就没办法，如果是机器自带的命令行（如 Windows 的 cmd 或 PowerShell，或 macOS 的 Terminal，加壳的 Cmder 和 iTerm 本质还是系统自带的，一样），可以用 `webbrowser.open(filepath)` 唤起系统默认的图片查看器来打开


## 超时或连接错误

抓图的时候偶尔可能会 ConnectionError，果断把超时和重试机制给加上，加了超时和重试机制后就没再出类似问题了


## Cookie 导出和导入

一开始按各种教程，用 `requests.utils` 下的 `dict_from_cookiejar` 和 `cookiejar_from_dict` 做 Cookie 到 dict 转换，然后用 `json.dump` 和 `json.load` 去保存读取，但每次读进来都要重新登录

后面怀疑是不是 json 中间丢了信息（比如数字精度），但 Cookie 导出来的都是字符串有什么好丢的，换用 `pickle` 做序列化和读取，还是不行

再仔细研究了下导出前和读取后的数据，发现 json 和 pickle 是没问题的，问题出在 `dict_from_cookiejar` 和 `cookiejar_from_dict` 这个转换过程中。Cookie 每个值是有作用域的，不同作用域下可以有同名的 Cookie，在转换过程中遇到同名的就后面覆盖前面了，如果拿的不是该拿的作用域的那个值，人人就会报错，会跳登录

所以在保存 Cookie 前要做一个特殊的处理，把那个不用的 Cookie 去掉再导出，这样也可以用 json 做序列化


## 数据安全

一开始把用户名密码写到 config 里，后面想了下还是抓的时候输，免得每次都要去改 config，万一忘改回来还可能不小心提交到 git 上去

本地保存的 Cookie 文件就直接加 .gitignore 里了
