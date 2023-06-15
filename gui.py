# coding: utf-8

import json
import logging
import logging.config
import threading
import urllib.parse

import PySimpleGUI as sg

from config import config

from crawl.crawler import Crawler
from fetch import prepare_db, fetch_user, update_fetch_info
from web import app


OUTPUT_COLUMNS = 80
OUTPUT_ROWS = 40


logging.config.dictConfig(config.LOGGING_CONF)
logger = logging.getLogger(__name__)


class GUILoggingHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self)

    def emit(self, record):
        global buffer  # pylint: disable=W0603
        format_msg = self.format(record)
        msg = f'{record.asctime} [{record.levelname}] {format_msg}'
        if buffer:
            buffer = buffer[1-OUTPUT_ROWS:]
            buffer.append(msg)
        else:
            buffer = [msg]
        try:
            window['-LOUT-'].update(value='\n'.join(buffer))
        except NameError:
            # GUI window not inited, just pass
            pass


buffer = []
ch = GUILoggingHandler()
ch.setLevel(logging.INFO)

logging.getLogger("").addHandler(ch)


def run_server():
    app.run()


cookie = Crawler.load_cookie()
fetched_info = {}
if cookie:
    cookie_str = cookie.values()[0]
    cookie_json = json.loads(urllib.parse.unquote(cookie_str))
    fetched_info = update_fetch_info(cookie_json['userId'])


form_column = [
    [sg.Text("人人网账号"), sg.Input("", size=(24, 1), key="-INPUT-EMAIL-")],
    [sg.Text("人人网密码"), sg.Input("", size=(24, 1), key="-INPUT-PASSWORD-", password_char="*")],
    [
        sg.Checkbox("状态", key="-FETCH-STATUS-"),
        sg.Checkbox("日志", key="-FETCH-BLOG-"),
        sg.Checkbox("相册", key="-FETCH-ALBUM-"),
        sg.Checkbox("留言", key="-FETCH-GOSSIP-")
    ],
    [sg.Button("开始获取", key="-FETCH-")],
    [sg.Button("开启服务", key="-START-")]
]

log_column = [
    [sg.Text(fetched_info.get('name', 'unknown'), size=(OUTPUT_COLUMNS, OUTPUT_ROWS), key="-LOUT-")]
]

layout = [
    [
        sg.Column(form_column),
        sg.VSeparator(),
        sg.Column(log_column)
    ]
]

window = sg.Window("人人网备份小工具", layout, margins=(20, 20))
svr = None

while True:
    event, values = window.read()

    if event == "OK" or event == sg.WIN_CLOSED:
        if svr:
            logger.info('terminate web server')
        break

    if event == "-FETCH-":
        email = values['-INPUT-EMAIL-']
        password = values['-INPUT-PASSWORD-']

        fetch_status = values['-FETCH-STATUS-']
        fetch_blog = values['-FETCH-BLOG-']
        fetch_album = values['-FETCH-ALBUM-']
        fetch_gossip = values['-FETCH-GOSSIP-']

        prepare_db()

        config.crawler = Crawler(email, password, cookie)
        uid = config.crawler.uid

        fetched = fetch_user(
            uid,
            fetch_status=fetch_status,
            fetch_gossip=fetch_gossip,
            fetch_album=fetch_album,
            fetch_blog=fetch_blog
        )

        if not fetched:
            logger.info("nothing need to fetch, just test login")

        if fetched:
            update_fetch_info(uid)

    elif event == '-START-':
        svr = threading.Thread(target=run_server, args=(), daemon=True)
        svr.start()

window.close()
