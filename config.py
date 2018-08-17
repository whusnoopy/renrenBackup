# coding: utf8

import sys


class LocalConfig(object):
    py3 = sys.version_info[0] >= 3

    crawler = None
    DATABASE = 'renren_bak.db'

    COOKIE_FILE = "./.cookies"

    ITEMS_PER_PAGE = 20
    TIMEOUT = 15
    RETRY_TIMES = 5

    ENCRYPT_KEY_URL = "http://login.renren.com/ajax/getEncryptKey"
    LOGIN_URL = "http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp={ts}"
    ICODE_URL = "http://icode.renren.com/getcode.do?t=web_login&rnd={rnd}"
    ICODE_FILEPATH = "./static/img/icode.jpg"

    COMMENT_URL = "http://comment.renren.com/comment/xoa2"
    GLOBAL_COMMENT_URL = "http://comment.renren.com/comment/xoa2/global"
    LIKE_URL = "http://like.renren.com/showlikedetail"

    STATUS_URL = "http://status.renren.com/GetSomeomeDoingList.do"

    GOSSIP_PAGE_URL = "http://gossip.renren.com/list/{uid}"
    GOSSIP_URL = "http://gossip.renren.com/ajaxgossiplist.do"

    ALBUM_LIST_URL = "http://photo.renren.com/photo/{uid}/albumlist/v7"
    ALBUM_SUMMARY_URL = "http://photo.renren.com/photo/{uid}/album-{album_id}/v7"
    PHOTO_INFO_URL = "http://photo.renren.com/photo/{uid}/photo-{photo_id}/layer"

    BLOG_LIST_URL = "http://blog.renren.com/blog/{uid}/blogs"
    BLOGS_PER_PAGE = 10
    BLOG_DETAIL_URL = "http://blog.renren.com/blog/{uid}/{blog_id}"


config = LocalConfig
