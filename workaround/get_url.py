# coding: utf8

from datetime import datetime
import re

import requests

from config import config


class Crawler(object):
    DEFAULT_HEADER = {
        'Accept': 'text/html, application/xhtml+xml, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Cache-Control': 'no-cache'
    }

    def __init__(self):
        self.is_login = False
        self.session = requests.session()
        self.rtk = 'TODO'
        self.requestToken = 'TODO'

    def login(self):
        params = {
            "email": "TODO",
            "icode": "",
            "origURL": "http://www.renren.com/home",
            "domain": "renren.com",
            "key_id": "1",
            "captcha_type": "web_login",
            "password": "TODO",
            "rkey": "TODO",
        }

        now = datetime.now()
        ts_dict = {
            'year': now.year,
            'month': now.month - 1,
            'isoweekday': now.isoweekday(),
            'hour': now.hour,
            'second': now.second,
            'utcms': now.microsecond / 1000
        }

        timestamp = config.LOGIN_TIMESTAMP.format(**ts_dict)
        login_url = config.LOGIN_URL.format(timestamp=timestamp)

        resp = self.session.post(login_url, headers=Crawler.DEFAULT_HEADER, params=params)
        print resp

        return resp

    def get_url(self, url, params=dict()):
        resp = self.session.get(url, params=params, headers=Crawler.DEFAULT_HEADER)
        print url, params
        print resp
        print resp.content
        return resp

    def get_index_page(self):
        resp = self.get_url("http://www.renren.com/30314/profile")
        index_content = resp.content.decode('utf8')
        
        find_requestToken = re.findall(r"requestToken\s:\s'(-*\d+)'", index_content)
        find_rtk = re.findall(r"_rtk\s:\s'(\w+)'", index_content)

        print find_requestToken, find_rtk


crawler = Crawler()
