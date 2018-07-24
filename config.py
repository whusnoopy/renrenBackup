# coding: utf8

class LocalConfig(object):
    # TODO: YOUR UID HERE
    UID = ''
    DATABASE = f'user_{UID}.db'

    STATUS_PER_PAGE = 20


class CrawlConfig(LocalConfig):
    STATUS_URL = "http://status.renren.com/GetSomeomeDoingList.do"

    STATUS_COMMENT_URL = "http://comment.renren.com/comment/xoa2"
    STATUS_LIKE_URL = "http://like.renren.com/showlikedetail"

    GOSSIP_URL = "http://gossip.renren.com/ajaxgossiplist.do"

    ALBUM_LIST_URL = "http://photo.renren.com/photo/{uid}/albumlist/v7"
    ALBUM_SUMMARY_URL = "http://photo.renren.com/photo/{uid}/album-{album_id}/v7"
    PHOTO_INFO_URL = "http://photo.renren.com/photo/{uid}/photo-{photo_id}/layer"

    # TODO: COPY FROM CHROME
    COOKIE_STR = ""
    COOKIES = dict()
    for s in COOKIE_STR.split(';'):
        if s:
            kv = s.strip().split('=')
            COOKIES[kv[0]] = kv[1]


config = LocalConfig
crawl_config = CrawlConfig
