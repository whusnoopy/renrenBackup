# coding: utf8


class LocalConfig(object):
    LOGIN_URL = "http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp={timestamp}"
    LOGIN_TIMESTAMP = "{year}{month}{isoweekday}{hour}{second}{utcms}"

config = LocalConfig
