# renrenBackup

A backup tool for renren.com


# 人人网信息备份工具

## 基本配置

理论上 Python 2.7+ 和 Python 3.6+ 都可以用（已经移除了 f-string，不过我是在 Python 3.6.5 下抓的，2.7.15 可以展示）

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
* `-u` 要抓的人的人人 uid

```bash
$ python fetch.py --help
usage: fetch.py [-h] [-s] [-g] [-a] [-b] [-u FETCH_UID] email password

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
  -u FETCH_UID, --fetch-uid FETCH_UID
                        user to fetch, or the login user by default

$ python fetch.py email@renren.com passwordAtRenren -s -g -a -b
```

> 注意：因为当前版本还不支持同时展示多人的抓取记录，请抓别人的时候换一下 `config.py` 里的 DATABASE 文件地址

## 展示

直接运行如下命令，即可在本机浏览器打开 `localhost:5000` 看到展示

```bash
python web.py
```

## TODO

- [ ] 纯静态输出，不用启 flask 也能查看（把评论点赞数据也输出到页面，js 只控制是否展示）
- [ ] 纯动态输出，学习用 Vue.js
- [x] 可以抓别人的记录
- [ ] 同时展示多人记录
