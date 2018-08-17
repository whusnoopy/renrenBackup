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
* `-u` 要抓的人的人人 uid（仅能抓取当前登录账户可见的内容）
* `-r` 强制更新已抓取用户的统计信息

```bash
# 查看详细的命令参数
$ python fetch.py --help
usage: fetch.py [-h] [-s] [-g] [-a] [-b] [-u FETCH_UID] [-r] email password

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
  -r, --refresh-count   refresh fetched user count

# 抓取自己的所有信息
$ python fetch.py email@renren.com passwordAtRenren -s -g -a -b

# 指定抓取某人的状态
$ python fetch.py email@renren.com passwordAtRenren -s -u 30314

# 强制更新某人的抓取统计信息
$ python fetch.py email@renren.com passwordAtRenren -u 30314 -r
```

如果遇到要登录验证码的情况，在终端提示时输入自动打开的图片上的四个汉字即可。如果没有自动打开验证码图片，可到项目的 `/static/img/icode.jpg` 找到，自行打开并输入验证码

## 展示

直接运行如下命令，即可在本机浏览器打开 `localhost:5000` 看到展示

```bash
python web.py
```

## TODO

- [ ] 纯静态输出，不用启 flask 也能查看（把评论点赞数据也输出到页面，js 只控制是否展示）
- [ ] 纯动态输出，学习用 Vue.js
- [x] 可以抓别人的记录
- [x] 同时展示多人记录
- [ ] 强制重抓之前抓挂的图（还挂就替换成默认图）