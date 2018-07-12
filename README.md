# renrenBackup

A backup tool for renren.com

# 人人网信息备份工具

## Log

#### 2018-07-12

试图直接从 Chrome 里拷 Cookie 出来用，没用成功，还是走一遍 login 好了。之前找的那几个都是用明文登录的方式，似乎现在都不行了，抓了下请求包，还没完全搞明白官方是怎么加密的，但是在浏览器里把 ajaxLogin 那个请求的 form data 扒出来，直接提交后就可以获取到正确的 requests.session

#### 2018-07-11

想起来自己的人人账号也好久没用了，说不定这个站哪天都不在了，等官方有导出工具还是别想了，自己来吧

找了一圈找到了如下几个备份工具，不过看说明从 2018 年某刻后都不能用了，自己学着改改看

* https://github.com/xinyu3ru/renren-bak
* https://github.com/threegirl2014/RenRenDownload
* https://github.com/kngxscn/backup-renren-status
