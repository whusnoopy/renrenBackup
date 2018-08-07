# coding: utf8

from datetime import datetime
import json
import os
import random
import time
import webbrowser

import requests, requests.utils
from requests.exceptions import ConnectionError

from config import config


def encryptedString(enc, mo, s):
    b = 0
    pos = 0
    for ch in s:
        b += (ord(ch) << pos)
        pos += 8

    crypt = pow(b, enc, mo)

    return '{crypt:x}'.format(crypt=crypt)


class Crawler(object):
    DEFAULT_HEADER = {
        'Accept': 'text/html, application/xhtml+xml, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Cache-Control': 'no-cache'
    }

    def __init__(self, email=None, password=None):
        self.uid = ''
        self.email = email
        self.password = password
        self.session = requests.session()

        if os.path.exists(config.COOKIE_FILE):
            with open(config.COOKIE_FILE) as fp:
                cookies = json.load(fp)

                if 'id' in cookies:
                    self.uid = cookies['id']
                    for key, val in cookies.items():
                        self.session.cookies.set(key, val)
                else:
                    self.login()

    def get_url(self, url, params=dict(), method='GET', retry=0):
        if not self.uid:
            self.login()

        if retry >= config.RETRY_TIMES:
            raise Exception("network error, exceed max retry time")
        try:
            request_args = {
                'url': url,
                'params': params,
                'headers': Crawler.DEFAULT_HEADER,
                'timeout': config.TIMEOUT,
                'allow_redirects': False
            }
            if method == 'POST':
                resp = self.session.post(**request_args)
            else:
                resp = self.session.get(**request_args)
        except ConnectionError:
            retry += 1
            time.sleep(retry)
            return self.get_url(url, params, method, retry)

        if resp.status_code == 302 and resp.headers['Location'].find('Login') >= 0:
            print('login expired, re-login')
            self.login()
            return self.get_url(url, params, method, retry+1)

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

    def login(self, retry=0, icode=''):
        if retry >= config.RETRY_TIMES:
            raise Exception("Cannot login")

        if not retry:
            self.session.cookies.clear()

        print('prepare login encryt info')
        enc_resp = self.session.get(config.ENCRYPT_KEY_URL, headers=Crawler.DEFAULT_HEADER, timeout=config.TIMEOUT)
        r = json.loads(enc_resp.text)
        param = {
            'email': self.email,
            'password': encryptedString(int(r['e'], 16), int(r['n'], 16), self.password),
            'rkey': r['rkey'],
            'key_id': 1,
            'captcha_type': 'web_login',
            'icode': icode
        }

        now = datetime.now()
        ts = '{year}{month}{weekday}{hour}{second}{ms}'.format(**{
            'year': now.year,
            'month': now.month-1,
            'weekday': (now.weekday()+1)%7,
            'hour': now.hour,
            'second': now.second,
            'ms': int(now.microsecond/1000)
        })

        print('prepare post login request')
        self.session.post(config.LOGIN_URL.format(ts=ts), params=param, timeout=config.TIMEOUT)
        cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
        if 'id' not in cookies:
            print('can not get login info, needs icode')

            icode_resp = self.session.get(config.ICODE_URL.format(rnd=random.random()), timeout=config.TIMEOUT)
            print('get icode image, output to {filepath}'.format(filepath=config.ICODE_FILEPATH))
            with open(config.ICODE_FILEPATH, 'wb') as fp:
                fp.write(icode_resp.content)
                webbrowser.open('file:///{filepath}'.format(filepath=os.path.abspath(config.ICODE_FILEPATH)))

            icode = input("Input text on Captcha icode image: ")
            retry += 1
            time.sleep(retry)
            return self.login(retry, icode)

        with open(config.COOKIE_FILE, 'w') as fp:
            json.dump(cookies, fp)

        self.uid = cookies['id']
        print('login success with {email} as {uid}'.format(email=self.email, uid=self.uid))
        return True
