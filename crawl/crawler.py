# coding: utf8

from datetime import datetime
import json
import re
import time

import requests
from requests.exceptions import ConnectionError

from config import config


def encryptedString(enc, mo, s):
    b = 0
    pos = 0
    for ch in s:
        b += (ord(ch) << pos)
        pos += 8

    crypt = pow(b, enc, mo)

    return f'{crypt:x}'


class Crawler(object):
    DEFAULT_HEADER = {
        'Accept': 'text/html, application/xhtml+xml, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Cache-Control': 'no-cache'
    }

    def __init__(self):
        self.uid = ''
        self.session = requests.session()
        self.login()

    def get_url(self, url, params=dict(), method='GET', retry=0):
        if not self.uid:
            self.login()

        if retry >= config.RETRY_TIMES:
            raise Exception("network error, exceed max retry time")
        try:
            if method == 'POST':
                resp = self.session.post(url, params=params, headers=Crawler.DEFAULT_HEADER, timeout=config.TIMEOUT)
            else:
                resp = self.session.get(url, params=params, headers=Crawler.DEFAULT_HEADER, timeout=config.TIMEOUT)
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

    def login(self, retry=0):
        if retry >= config.RETRY_TIMES:
            raise Exception("Cannot login")

        print(f'prepare login encryt info')
        enc_resp = self.session.get(config.ENCRYPT_KEY_URL, headers=Crawler.DEFAULT_HEADER, timeout=config.TIMEOUT)
        r = json.loads(enc_resp.text)
        param = {
            'email': config.EMAIL,
            'password': encryptedString(int(r['e'], 16), int(r['n'], 16), config.PASSWORD),
            'rkey': r['rkey'],
            'key_id': 1,
            'captcha_type': 'web_login',
            'icode': ''
        }

        now = datetime.now()
        ts = f'{now.year}{now.month-1}{(now.weekday()+1)%7}{now.hour}{now.second}{int(now.microsecond/1000)}'

        print(f'prepare post login request')
        login_resp = self.session.post(config.LOGIN_URL.format(ts=ts), params=param, timeout=config.TIMEOUT)
        set_cookie = login_resp.headers.get('Set-Cookie', '')
        uid = re.findall(r' id=(\d+)', set_cookie)
        if not uid:
            print(f'can not get login info')
            retry += 1
            time.sleep(retry)
            return self.login(retry)

        self.uid = uid[0]
        print(f'login success with {config.EMAIL} as {uid[0]}')
        return True


crawler = Crawler()
