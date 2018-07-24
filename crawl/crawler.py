# coding: utf8

import re

import requests

from config import crawl_config as config


class Crawler(object):
    DEFAULT_HEADER = {
        'Accept': 'text/html, application/xhtml+xml, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Cache-Control': 'no-cache'
    }

    def __init__(self):
        self.session = requests.session()

    def get_url(self, url, params=dict()):
        resp = self.session.get(url, params=params, headers=Crawler.DEFAULT_HEADER, cookies=config.COOKIES)
        return resp

    def post_for_json(self, url, params=dict()):
        resp = self.session.post(url, params=params, headers=Crawler.DEFAULT_HEADER, cookies=config.COOKIES)
        return resp


crawler = Crawler()
