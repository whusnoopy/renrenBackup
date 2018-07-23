# coding: utf8

from datetime import datetime
import json

from peewee import IntegrityError

from config import crawl_config as config
from models import Status, StatusComment, StatusLike, User

from .crawler import crawler


def load_status_comments_offset(status_id, offset):
    param = {
        "limit": 20,
        "desc": "true",
        "offset": offset,
        "replaceUBBLarge": "true",
        "type": "status",
        "entryId": status_id,
        "entryOwnerId": config.UID,
    }

    resp = crawler.get_url(config.STATUS_COMMENT_URL, param)
    r = json.loads(resp.text)

    for c in r['comments']:
        user = {
            'uid': c['authorId'],
            'name': c['authorName'],
            'headPic': c['authorHeadUrl'],
        }
        User.insert(**user).on_conflict('replace').execute()

        comment = {
            'id': c['id'],
            'status_id': status_id,
            't': datetime.fromtimestamp(int(c['createTimeMillis'])/1000),
            'authorId': c['authorId'],
            'authorName': c['authorName'],
            'content': c['content']
        }
        StatusComment.insert(**comment).on_conflict('replace').execute()

    return r['commentTotalCount']


def get_status_comments(status_id):
    offset = 0
    total = config.STATUS_PER_PAGE
    while offset + config.STATUS_PER_PAGE <= total:
        total = load_status_comments_offset(status_id, offset)
        offset += config.STATUS_PER_PAGE

    print(f'    crawled {total} comments on {status_id}')

    return total


def get_status_likes(status_id):
    param = {
        "stype": "status",
        "sourceId": status_id, 
        "owner": config.UID,
        "gid": f'status_{status_id}',
        "uid": config.UID
    }

    resp = crawler.get_url(config.STATUS_LIKE_URL, param)
    r = json.loads(resp.text)

    for l in r['likeList']:
        user = {
            'uid': l['id'],
            'name': l['name'],
            'headPic': l['headUrl'],
        }
        User.insert(**user).on_conflict('replace').execute()

        like = {
            'status_id': status_id,
            'uid': l['id']
        }
        StatusLike.insert(**like).on_conflict('replace').execute()

    count = r['likeCount']
    print(f'    crawled {count} likes on {status_id}')

    return count


def load_status_page(page):
    resp = crawler.get_url(config.STATUS_URL, {'uid': config.COOKIES['id'], 'curpage': page})
    r = json.loads(resp.text)

    likes = r['likeInfoMap']
    for s in r['doingArray']:
        id = int(s['id'])
        status = {
            'id': id,
            't': datetime.fromtimestamp(int(s['createTime'])/1000),
            'content': s['content'],                            # 内容
            'like': likes.get(f'status_{id}', 0),               # 点赞
            'repeat': s['repeatCountTotal'],                    # 转发
            'comment': s['comment_count'],                      # 评论
            'rootContent': s.get('rootContent', ''),            # 如果是转发，转发的原文
            'rootUid': s.get('rootDoingUserId', 0),             # 转发原 uid
            'rootUname': s.get('rootDoingUserName', ''),        # 转发原 username
        }
        Status.insert(**status).on_conflict('replace').execute()

        if status['comment'] > 0:
            get_status_comments(id)
        if status['like'] > 0:
            get_status_likes(id)

    parsed = len(r['doingArray'])
    print(f'  on page {page}, {parsed} parsed')

    return r['count']


def get_status():
    cur_page = 0
    total = config.STATUS_PER_PAGE
    while cur_page*config.STATUS_PER_PAGE < total:
        print(f'start crawl status page {cur_page}')
        total = load_status_page(cur_page)
        cur_page += 1

    return total
