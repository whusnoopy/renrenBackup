# coding: utf8

from datetime import datetime
import json

from config import crawl_config as config
from models import User, Comment, Like

from .crawler import crawler


def get_comments(entry_id, entry_type):
    param = {
        "entryOwnerId": config.UID,
        'entryId': entry_id,
        'type': entry_type,
        'replaceUBBLarge': 'true',
        'limit': config.STATUS_PER_PAGE,
        'offset': 0
    }
    offset = 0
    total = config.STATUS_PER_PAGE
    while offset < total:
        param['offset'] = offset
        resp = crawler.get_url(config.STATUS_COMMENT_URL, params=param)
        resp_json = json.loads(resp.text)
        if int(resp_json['code']):
            # 抓太频繁了，重试一下
            continue

        total = resp_json['commentTotalCount']

        for c in resp_json['comments']:
            user = {
                'uid': c['authorId'],
                'name': c['authorName'],
                'headPic': c['authorHeadUrl'],
            }
            User.insert(**user).on_conflict('replace').execute()

            comment = {
                'id': c['id'],
                't': datetime.fromtimestamp(int(c['createTimeMillis'])/1000),
                'entry_id': entry_id,
                'entry_type': entry_type,
                'authorId': c['authorId'],
                'authorName': c['authorName'],
                'content': c['content']
            }
            Comment.insert(**comment).on_conflict('replace').execute()

        offset += config.STATUS_PER_PAGE

    print(f'        crawled {total} comments on {entry_type} {entry_id}')
    return total


def get_likes(entry_id, entry_type):
    param = {
        "stype": entry_type,
        "sourceId": entry_id, 
        "owner": config.UID,
        "gid": f'{entry_type}_{entry_id}',
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
            'entry_id': entry_id,
            'entry_type': entry_type,
            'uid': l['id']
        }
        Like.insert(**like).on_conflict('replace').execute()

    print(f'        crawled {r["likeCount"]} likes on {entry_type} {entry_id}')
    return r['likeCount']
