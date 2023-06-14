# coding: utf-8

import logging
import logging.config

import PySimpleGUI as sg

from config import config

from crawl.crawler import Crawler


class GUILoggingHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self)

    def emit(self, record):
        global buffer  # pylint: disable=W0603
        record = f'{record.asctime} [{record.levelname}] {record.msg}'
        buffer = f'{buffer}\n{record}'.strip()  # pylint: disable=E0601
        window['-LOUT-'].update(value=buffer)


buffer = ''
ch = GUILoggingHandler()
ch.setLevel(logging.INFO)

logging.config.dictConfig(config.LOGGING_CONF)
logger = logging.getLogger(__name__)
logging.getLogger("").addHandler(ch)

form_column = [
    [sg.Text("人人网账号"), sg.Input("", size=(24, 1), key="-INPUT-EMAIL-")],
    [sg.Text("人人网密码"), sg.Input("", size=(24, 1), key="-INPUT-PASSWORD-", password_char="*")],
    [sg.Button("开始获取", key="-START-")]
]

log_column = [
    [sg.Text("log output here", size=(80, 24), key="-LOUT-")]
]

layout = [
    [
        sg.Column(form_column),
        sg.VSeparator(),
        sg.Column(log_column)
    ]
]

window = sg.Window("人人网备份小工具", layout, margins=(20, 20))

while True:
    event, values = window.read()

    if event == "OK" or event == sg.WIN_CLOSED:
        break

    if event == "-START-":
        cookie = Crawler.load_cookie()
        if not cookie:
            logger.info("no cookie")

        email = values['-INPUT-EMAIL-']
        password = values['-INPUT-PASSWORD-']
        if not cookie or email or password:
            logger.info("login manually")
            config.crawler = Crawler(email, password, cookie)


window.close()
