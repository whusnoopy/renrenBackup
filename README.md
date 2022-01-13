# renrenBackup

A backup tool for renren.com

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CodeFactor](https://www.codefactor.io/repository/github/whusnoopy/renrenbackup/badge/master)](https://www.codefactor.io/repository/github/whusnoopy/renrenbackup/overview/master)

# ruotianluo notes

支持人人新接口。（2021.1测试）

支持两种登陆方式，用户名密码登陆以及cookie登陆（Instruction视频指路：[url](https://www.bilibili.com/video/BV1vT4y1m7Pd/)）。

TODO:
- [x] cookie cache，无需每次登陆
- [x] 状态
- [ ] 状态加comments
- [x] 留言板
- [x] Windows release
- [x] 知乎文章
- [x] 更换login逻辑
- [ ] 整理代码，优化代码结构。
- [x] 添加CI
- [x] 状态加图片

# 人人网信息备份工具

> 特别说明：
> 
> <del>2021 年 5 月人人网 Web 端全面改版，之前的页面入口逻辑都不存在，本工具不可用</del>
>
> <del>2020 年 11 月开始人人网的状态功能出现异常，无法抓取，使用时请去掉 `-s` 参数跳过状态的抓取</del>
>
> <del>2019 年 8 月开始人人网的日志功能出现异常，无法抓取，使用时请去掉 `-b` 参数跳过日志的抓取</del>


## Windows 系统无 Python 环境直接运行

1. 在 https://github.com/ruotianluo/renrenBackup/releases/latest `renrenBackup_refs.tags.v0.7.zip` 压缩文件，解压到一个单独的目录
2. 在命令提示符进入该目录，执行 `renrenBackup.exe fetch -g -a` 来抓取账号为 `email` 密码是 `password` 的用户信息（详细参数可见下方 Python 环境运行方式）
3. 抓取后，在命令提示符下执行 `renrenBackup.exe runserver` 后，可以在浏览器里打开 http://localhost:5000 来查看抓取后的展示
4. 抓取后，在命令提示符下执行 `renrenBackup.exe export -f backup.tar`，可以生成 `backup.tar` 这个打包文件，解压后无需任何环境直接用浏览器打开 `index.html` 即可浏览备份好的信息

> <del>注意：目前的版本并未经过严格测试和兼容性确认，只在 <del>Windows 10 x64 1809 版本</del> macOS Monterey 和 Win10 上简单确认可用，其他系统（Linux/Windows）或版本（非 Win10x64）都可能无法运行，欢迎协助更新</del> 已添加CI test，在linux windows mac上均测试，且windows release也有测试。


## Python 环境使用和修改

### 基本配置

<del>理论上 Python 2.7+ 和 Python 3.6+ 都可以用
（我是在 Windows 10 + Python 3.7.0 的环境下测试的）</del>
我是在osx + python 3.7测试的。（Windows release也有简单测试。）

使用 virtualenv 构建运行所需虚拟环境

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

### 抓取

直接运行 `python manage.py fetch` 即可，相关参数见下，<del>不输入用户名密码是不会抓取的</del>，不输入用户名密码则会要求你复制node.js fetch的内容，不带各种抓取参数就是只登陆不抓取

* `-e email` 用户名（邮箱）
* `-p password` 密码
* `-s` 状态
* `-g` 留言板
* `-a` 相册
* `-b` 日志
* `-u` 要抓的人的人人 uid（仅能抓取当前登录账户可见的内容）
* `-r` 强制更新已抓取用户的统计信息

```bash
# 查看详细的命令参数
$ python manage.py fetch --help
usage: manage.py fetch [-?] [-e EMAIL] [-p PASSWORD] [-s] [-g] [-a] [-b] [-r]
                       [-u UID]

optional arguments:
  -?, --help            show this help message and exit
  -e EMAIL, --email EMAIL
  -p PASSWORD, --password PASSWORD
  -s, --status
  -g, --gossip
  -a, --album
  -b, --blog
  -r, --refresh_count
  -u UID, --uid UID

# 抓取自己的所有信息
$ python manage.py fetch -e email@renren.com -p passwordAtRenren -s -g -a -b
# 或者
$ python manage.py fetch -s -g -a -b


# 指定抓取某人的留言板 (目前版本不可用)
$ python manage.py fetch -g -u 30314

# 强制更新某人的抓取统计信息
$ python manage.py fetch -u 30314 -r
```

如果遇到要登录验证码的情况，在终端提示时输入自动打开的图片上的四个字母数字即可。如果没有自动打开验证码图片，可到项目的 `/static/icode.jpg` 找到，自行打开并输入验证码

### 展示

直接运行如下命令，即可在本机浏览器打开 http://localhost:5000 看到展示

```bash
python manage.py runserver
```

### 打包备份

将抓取的页面和静态文件统一打包，将打包文件解压后可以不启动 flask 也能查看

```bash
python manage.py export -f backup.tar
```

### 版本发布

目前在 Windows 平台下使用 pyinstaller + pywin32 来做版本发布，希望给没有 Python 环境的朋友提供帮助

下述操作均在 Windows 的命令提示符（cmd）下完成，PowerShell 和 WSL 可能出现奇怪的问题（我还不确定问题原因）

```cmd
# 安装依赖
pip install pyinstaller pywin32

# 打包发布，会在 dist 目录下生成 renrenBackup.exe，并把 static 和 templates 初始目录也放到 dist 下
python manage.py release
```

执行命令后将 `dist` 目录单独打成一个压缩包就可以发布了


## TODO

- [x] 纯静态输出，不用启 flask 也能查看（把评论点赞数据也输出到页面，js 只控制是否展示）
- [x] 备份打包
- [x] 可以抓别人的记录
- [x] 同时展示多人记录
- [x] 参数交互输入，更好满足非 Python 环境下的可用性
- [ ] 强制重抓之前抓挂的图（还挂就替换成默认图）
- [ ] 断点续传，抓到一半挂了后，重启跳过已抓取的内容（或根据 DB 已有数据来优化抓取量）#13
- [x] 用 Python 的日志系统替代 print 输出

## 新功能需求

- [ ] 纯动态输出，学习用 Vue.js
- [ ] 搜索功能 #21
