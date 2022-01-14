# coding: utf8

from datetime import datetime
import logging

from config import config
from models import Status

from .utils import get_image, get_common_payload


logger = logging.getLogger(__name__)
crawler = config.crawler


def load_status_page(uid=crawler.uid, after=None):
    r = crawler.get_json(config.STATUS_URL, json_=get_common_payload(uid, after), method='POST')

    if 'count' not in r:
        return 0, None

    for s in r['data']:
        sid = int(s['id'])
        if 'content' not in s['body']:
            continue
        status = {
            'id': sid,
            'uid': uid,
            't': datetime.fromtimestamp(int(s['publish_time'])/1000),
            'content': s['body']['content'],                                                # 内容
            'headPic': get_image(s['body'].get('head_image', '')),                          # 附件图片
            'like': s['like_count'],                                                        # 点赞
            'repeat': 0, # s['repeatCountTotal'],                                           # 转发
            'comment': s['comment_count'],                                                  # 评论
            'rootContent': s.get('from', {}).get('body', {}).get('content', ''),            # 如果是转发，转发的原文
            'rootPic': get_image(s.get('from', {}).get('body', {}).get('head_image', '')),  # 如果是转发，转发的原文的附件图片
            'rootUid': s.get('from', {}).get('publisher', {}).get('id', 0),                 # 转发原 uid
            'rootUname': s.get('from', {}).get('publisher', {}).get('nickname', ''),        # 转发原 username
            'location': s.get('lbs', {}).get('position', ''),                               # 带地理位置的地名
            'locationUrl': '', # s.get('locationUrl', ''),                                  # 地理位置的人人地点
        }
        Status.insert(**status).on_conflict('replace').execute()

    logger.info('{parsed} parsed'.format(parsed=len(r['data'])))

    return r['count'], r['tail_id']


def get_status(uid=crawler.uid):
    cur_page = 0
    total = 0
    after = None
    while True:
        logger.info('start crawl status page {cur_page}'.format(cur_page=cur_page))
        count, after = load_status_page(uid, after)
        if count == 0:
            break
        total += count
        cur_page += 1

    return total
