# coding: utf8

from datetime import datetime
import json
import os
import random
import time
import webbrowser

import requests
import requests.utils
from requests.exceptions import ConnectionError, ReadTimeout  # pylint: disable=W0622

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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      + '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Cache-Control': 'no-cache'
    }

    def __init__(self, email=None, password=None, cookies=None):
        self.uid = ''
        self.email = email
        self.password = password
        self.session = requests.session()
        self.session.headers = Crawler.DEFAULT_HEADER

        if cookies and cookies.get('ln_uact') == email:
            self.uid = int(cookies['id'])
            self.session.cookies.update(cookies)

        self.check_login()

    @classmethod
    def load_cookie(cls):
        cookies = None

        if os.path.exists(config.COOKIE_FILE):
            with open(config.COOKIE_FILE) as fp:
                try:
                    cookies = requests.utils.cookiejar_from_dict(json.load(fp))
                    print('load cookies from {filename}'.format(filename=config.COOKIE_FILE))
                except json.decoder.JSONDecodeError:
                    cookies = None

        return cookies

    def dump_cookie(self):
        cookies = self.session.cookies
        for cookie in cookies:
            if cookie.name == 't' and cookie.path != '/':
                cookies.clear(cookie.domain, cookie.path, cookie.name)
        with open(config.COOKIE_FILE, 'w') as fp:
            json.dump(requests.utils.dict_from_cookiejar(cookies), fp)

    def get_url(self, url, params=None, method='GET', retry=0, ignore_login=False):
        if not ignore_login and not self.uid:
            print("need login")
            self.login()

        if params is None:
            params = dict()

        if retry >= config.RETRY_TIMES:
            raise Exception("network error, exceed max retry time")
        try:
            request_args = {
                'url': url,
                'params': params,
                'timeout': config.TIMEOUT,
                'allow_redirects': False
            }
            if method == 'POST':
                resp = self.session.post(**request_args)
            else:
                resp = self.session.get(**request_args)
        except (ConnectionError, ReadTimeout) as e:
            time.sleep(2 ** retry)
            retry += 1
            return self.get_url(url, params, method, retry)

        if resp.status_code == 302 and resp.headers['Location'].find('Login') >= 0:
            print('login expired, re-login')
            self.login()
            return self.get_url(url, params, method, retry+1)

        if resp.cookies.get_dict():
            self.session.cookies.update(resp.cookies)

        return resp

    def get_json(self, url, params=None, method='GET', retry=0):
        if params is None:
            params = dict()

        resp = self.get_url(url, params, method)
        r = json.loads(resp.text.replace(',}','}'))

        if int(r.get('code', 0)):
            if retry >= config.RETRY_TIMES:
                raise Exception("network error, exceed max retry time")

            retry += 1
            time.sleep(retry)
            return self.get_json(url, params, method, retry)

        return r

    def check_login(self):
        print('  check login, and get homepage for cookie')
        self.get_url("http://www.renren.com/{uid}".format(uid=self.uid))
        print('    login valid')

        self.dump_cookie()

    def login(self, retry=0, icode=''):
        if retry >= config.RETRY_TIMES:
            raise Exception("Cannot login")

        if not retry:
            self.session.cookies.clear()

        print('prepare login encryt info')
        self.get_url(config.ICODE_URL.format(rnd=random.random()), ignore_login=True)
        enc_resp = self.get_url(config.ENCRYPT_KEY_URL, ignore_login=True)
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
            'weekday': (now.weekday()+1) % 7,
            'hour': now.hour,
            'second': now.second,
            'ms': int(now.microsecond/1000)
        })

        print('prepare post login request')
        self.get_url(config.LOGIN_URL.format(ts=ts), params=param, method='POST', ignore_login=True)
        cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
        if 'id' not in cookies:
            print('can not get login info, needs icode')

            icode_url = config.ICODE_URL.format(rnd=random.random())
            icode_resp = self.get_url(icode_url, ignore_login=True)
            print('get icode image, output to {filepath}'.format(filepath=config.ICODE_FILEPATH))
            with open(config.ICODE_FILEPATH, 'wb') as fp:
                fp.write(icode_resp.content)
                icode_filepath = os.path.abspath(config.ICODE_FILEPATH)
                webbrowser.open('file:///{filepath}'.format(filepath=icode_filepath))

            icode = input("Input text on Captcha icode image: ")
            retry += 1
            time.sleep(retry)
            return self.login(retry, icode)

        self.uid = int(cookies['id'])
        print('login success with {email} as {uid}'.format(email=self.email, uid=self.uid))

        self.check_login()
        return True
