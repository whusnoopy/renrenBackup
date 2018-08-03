# renrenBackup

A backup tool for renren.com


# 人人网信息备份工具

## 基本配置

依赖 Python 3.6.5+（其他版本我没测试过，因为用了 f-string，所以应该是要这个版本起跳）

用 pipenv 构建虚拟环境

```bash
pipenv --python 3.6.5
pipenv install
pipenv shell
```

或者用 virtualenv 构建

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

## 抓取

直接运行 `fetch.py` 即可，相关参数见下，不输入用户名密码是不会抓取的，不带各种抓取参数就是只登陆不抓取

* `-s` 状态
* `-g` 留言板
* `-a` 相册
* `-b` 日志

```bash
$ python fetch.py --help
usage: fetch.py [-h] [-s] [-g] [-a] [-b] email password

fetch renren data to backup

positional arguments:
  email               your renren email for login
  password            your renren password for login

optional arguments:
  -h, --help          show this help message and exit
  -s, --fetch-status  fetch status or not
  -g, --fetch-gossip  fetch gossip or not
  -a, --fetch-album   fetch album or not
  -b, --fetch-blog    fetch blog or not

$ python fetch.py email@renren.com passwordAtRenren -s -g -a -b
```


## 展示

直接运行如下命令，即可在本机浏览器打开 `localhost:5000` 看到展示

```bash
python web.py
```

## TODO

- [ ] 纯静态输出，不用启 flask 也能查看（把评论点赞数据也输出到页面，js 只控制是否展示）
- [ ] 纯动态输出，学习用 Vue.js
- [ ] 可以抓别人的记录
