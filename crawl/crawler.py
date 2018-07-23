# coding: utf8

import re

import requests
import requests_html

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
        self.html_session = requests_html.HTMLSession()

    def get_url(self, url, params=dict()):
        resp = self.session.get(url, params=params, headers=Crawler.DEFAULT_HEADER, cookies=config.COOKIES)
        return resp

    def post_for_json(self, url, params=dict()):
        resp = self.session.post(url, params=params, headers=Crawler.DEFAULT_HEADER, cookies=config.COOKIES)
        return resp

    def get_html(self, url, params=dict()):
        resp = self.html_session.get(url, params=params, headers=Crawler.DEFAULT_HEADER, cookies=config.COOKIES)
        return resp

    def get_index_page(self):
        resp = self.get_url(f"http://www.renren.com/{config.UID}/profile")
        index_content = resp.content.decode('utf8')
        
        find_requestToken = re.findall(r"requestToken\s:\s'(-*\d+)'", index_content)
        find_rtk = re.findall(r"_rtk\s:\s'(\w+)'", index_content)

        print(find_requestToken, find_rtk)


crawler = Crawler()
