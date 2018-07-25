# coding: utf8

import time
import json

import requests
from requests.exceptions import ConnectionError

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

    def get_url(self, url, params=dict(), method='GET', retry=0):
        if retry >= config.RETRY_TIMES:
            raise Exception("network error, exceed max retry time")
        try:
            if method == 'POST':
                resp = self.session.post(url, params=params, headers=Crawler.DEFAULT_HEADER, cookies=config.COOKIES, timeout=config.TIMEOUT)
            else:
                resp = self.session.get(url, params=params, headers=Crawler.DEFAULT_HEADER, cookies=config.COOKIES, timeout=config.TIMEOUT)
        except ConnectionError:
            retry += 1
            time.sleep(retry)
            return self.get_url(url, params, method, retry)

        return resp

    def get_json(self, url, params=dict(), method='GET', retry=0):
        resp = self.get_url(url, params, method)
        r = json.loads(resp.text)

        if int(r.get('code', 0)):
            if retry >= config.RETRY_TIMES:
                raise Exception("network error, exceed max retry time")

            retry += 1
            time.sleep(retry)
            return self.get_json(url, params, method, retry)

        return r


crawler = Crawler()
