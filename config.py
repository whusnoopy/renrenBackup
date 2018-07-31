# coding: utf8

class LocalConfig(object):
    # TODO: 填写要抓取账号的登录邮箱，登录密码。注意不要把个人信息提交到 git 里
    EMAIL = ''
    PASSWORD = ''

    DATABASE = 'renren_bak.db'

    ITEMS_PER_PAGE = 20
    TIMEOUT = 15
    RETRY_TIMES = 5

    ENCRYPT_KEY_URL = "http://login.renren.com/ajax/getEncryptKey"
    LOGIN_URL = "http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp={ts}"

    COMMENT_URL = "http://comment.renren.com/comment/xoa2"
    GLOBAL_COMMENT_URL = "http://comment.renren.com/comment/xoa2/global"
    LIKE_URL = "http://like.renren.com/showlikedetail"

    STATUS_URL = "http://status.renren.com/GetSomeomeDoingList.do"

    GOSSIP_URL = "http://gossip.renren.com/ajaxgossiplist.do"

    ALBUM_LIST_URL = "http://photo.renren.com/photo/{uid}/albumlist/v7"
    ALBUM_SUMMARY_URL = "http://photo.renren.com/photo/{uid}/album-{album_id}/v7"
    PHOTO_INFO_URL = "http://photo.renren.com/photo/{uid}/photo-{photo_id}/layer"

    BLOG_LIST_URL = "http://blog.renren.com/blog/{uid}/blogs"
    BLOGS_PER_PAGE = 10
    BLOG_DETAIL_URL = "http://blog.renren.com/blog/{uid}/{blog_id}"


config = LocalConfig
