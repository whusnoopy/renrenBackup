# renrenBackup

A backup tool for renren.com


# 人人网信息备份工具


## Windows 系统无 Python 环境直接运行

1. 在 https://github.com/whusnoopy/renrenBackup/releases/latest 发布页面下载最新的 `renrenBackup_x.x.zip` 压缩文件，解压到一个单独的目录
2. 在命令提示符进入该目录，执行 `fetch.exe email password -s -g -a -b` 来抓取账号为 `email` 密码是 `password` 的用户信息（详细参数可见下方 Python 环境运行方式）
3. 抓取后，在命令提示符下执行 `web.exe` 后，可以在浏览器里打开 `localhost:5000` 来查看
4. 抓取后，在命令提示符下执行 `web.exe export backup.tar`，可以生成 `backup.tar` 这个打包文件，解压后无需任何环境直接用浏览器打开 `index.html` 即可浏览备份好的信息

> 注意：目前的 pre-release 版本并未经过严格测试和兼容性确认，只在 Windows 10 x64 1809 版本上简单确认可用，其他系统（Linux/macOS）或版本（非 Win10x64）都可能无法运行，欢迎协助更新


## Python 环境使用和修改

### 基本配置

理论上 Python 2.7+ 和 Python 3.6+ 都可以用
（我是在 Windows 10 + Python 3.7.0 的环境下测试的）

用 pipenv 构建虚拟环境

```bash
pipenv --python 3.7.0
pipenv install
pipenv shell
```

或者用 virtualenv 构建

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

### 抓取

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

如果遇到要登录验证码的情况，在终端提示时输入自动打开的图片上的四个汉字即可。如果没有自动打开验证码图片，可到项目的 `/static/icode.jpg` 找到，自行打开并输入验证码

### 展示

直接运行如下命令，即可在本机浏览器打开 `localhost:5000` 看到展示

```bash
python web.py
```

### 打包备份

将抓取的页面和静态文件统一打包，将打包文件解压后可以不启动 flask 也能查看

```bash
python web.py export backup.tar
```

### 版本发布

目前在 Windows 平台下使用 pyinstaller + pywin32 来做版本发布，希望给没有 Python 环境的朋友提供帮助

下述操作均在 Windows 的命令提示符（cmd）下完成，PowerShell 和 WSL 可能出现奇怪的问题（我还不确定问题原因）

```cmd
# 安装依赖
pip install pyinstaller pywin32

# 打包抓取，会在 dist 目录下生成 fetch.exe
pyinstaller -F fetch.py

# 打包展示，会在 dist 目录下生成 web.exe
pyinstaller -F web.py
```

生成对应 exe 后把初始的 `static` 和 `templates` 两个目录也拷贝到 `dist` 目录下，然后 `dist` 目录就可以单独打成一个压缩包发布了


## TODO

- [x] 纯静态输出，不用启 flask 也能查看（把评论点赞数据也输出到页面，js 只控制是否展示）
- [x] 备份打包
- [x] 可以抓别人的记录
- [x] 同时展示多人记录
- [ ] 参数交互输入，更好满足非 Python 环境下的可用性
- [ ] 强制重抓之前抓挂的图（还挂就替换成默认图）
- [ ] 断点续传，抓到一半挂了后，重启跳过已抓取的内容（或根据 DB 已有数据来优化抓取量）#13
- [x] 用 Python 的日志系统替代 print 输出

## 新功能需求

- [ ] 纯动态输出，学习用 Vue.js
- [ ] 搜索功能 #21
