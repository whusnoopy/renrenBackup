# coding: utf8


class LocalConfig(object):
    STATUS_URL = "http://status.renren.com/GetSomeomeDoingList.do"

    COOKIE_STR = "COPY FROM CHROME"
    COOKIES = dict()
    for s in COOKIE_STR.split(';'):
        kv = s.strip().split('=')
        COOKIES[kv[0]] = kv[1]


config = LocalConfig
