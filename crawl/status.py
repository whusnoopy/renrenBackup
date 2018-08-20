# coding: utf8

from datetime import datetime
import json

from config import config
from models import Status

from .utils import get_comments, get_likes


crawler = config.crawler


def load_status_page(page, uid=crawler.uid):
    r = crawler.get_json(config.STATUS_URL, {'userId': uid, 'curpage': page})

    likes = r['likeInfoMap']
    for s in r['doingArray']:
        id = int(s['id'])
        # TODO: location，locationUrl
        status = {
            'id': id,
            'uid': uid,
            't': datetime.fromtimestamp(int(s['createTime'])/1000),
            'content': s['content'],                            # 内容
            'like': likes.get('status_{id}'.format(id=id), 0),               # 点赞
            'repeat': s['repeatCountTotal'],                    # 转发
            'comment': s['comment_count'],                      # 评论
            'rootContent': s.get('rootContent', ''),            # 如果是转发，转发的原文
            'rootUid': s.get('rootDoingUserId', 0),             # 转发原 uid
            'rootUname': s.get('rootDoingUserName', ''),        # 转发原 username
        }
        Status.insert(**status).on_conflict('replace').execute()

        if status['comment']:
            get_comments(id, 'status', owner=uid)
        if status['like']:
            get_likes(id, 'status', owner=uid)

    print('  on page {page}, {parsed} parsed'.format(page=page, parsed=len(r['doingArray'])))

    return r['count']


def get_status(uid=crawler.uid):
    cur_page = 0
    total = config.ITEMS_PER_PAGE
    while cur_page*config.ITEMS_PER_PAGE < total:
        print('start crawl status page {cur_page}'.format(cur_page=cur_page))
        total = load_status_page(cur_page, uid)
        cur_page += 1

    return total
