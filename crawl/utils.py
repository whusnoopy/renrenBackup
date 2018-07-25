# coding: utf8

from datetime import datetime
import json
import os

from config import crawl_config as config
from models import User, Comment, Like

from .crawler import crawler


def get_image(img_url):
    if not img_url:
        return ''

    path = img_url.split('/')
    path[0] = 'static'
    path[1] = 'img'
    path[2] = path[2].replace('.', '_')

    filename = '/'.join(path)
    filepath = '/'.join(path[:-1])

    if os.path.exists(filename):
        return f'/{filename}'

    if not os.path.exists(filepath):
        os.makedirs(filepath)

    resp = crawler.get_url(img_url)
    with open(filename, 'wb') as fp:
        fp.write(resp.content)

    print(f'        get {img_url} to {filename}')
    return f'/{filename}'


def save_user(uid, name, pic):
    user = {
        'uid': uid,
        'name': name,
        'headPic': get_image(pic),
    }
    User.insert(**user).on_conflict('replace').execute()

    return uid


def get_comments(entry_id, entry_type, global_comment=False):
    comment_url = config.GLOBAL_COMMENT_URL if global_comment else config.COMMENT_URL
    save_type = 'share' if global_comment else entry_type
    param = {
        "entryOwnerId": config.UID,
        'entryId': entry_id,
        'type': entry_type,
        'replaceUBBLarge': 'true',
        'limit': config.ITEMS_PER_PAGE,
        'offset': 0
    }
    offset = 0
    total = config.ITEMS_PER_PAGE
    while offset < total:
        param['offset'] = offset
        resp_json = crawler.get_json(comment_url, params=param)

        total = resp_json['commentTotalCount']
        if not total:
            break

        for c in resp_json['comments']:
            save_user(c['authorId'], c['authorName'], c['authorHeadUrl'])

            comment = {
                'id': c['id'],
                't': datetime.fromtimestamp(int(c['createTimeMillis'])/1000),
                'entry_id': entry_id,
                'entry_type': save_type,
                'authorId': c['authorId'],
                'authorName': c['authorName'],
                'content': c['content']
            }
            Comment.insert(**comment).on_conflict('replace').execute()

        offset += config.ITEMS_PER_PAGE

    print(f'        crawled {total}{" global" if global_comment else ""} comments on {entry_type} {entry_id}')
    return total


def get_likes(entry_id, entry_type):
    param = {
        "stype": entry_type,
        "sourceId": entry_id, 
        "owner": config.UID,
        "gid": f'{entry_type}_{entry_id}',
        "uid": config.UID
    }

    r = crawler.get_json(config.LIKE_URL, param)

    for l in r['likeList']:
        save_user(l['id'], l['name'], l['headUrl'])

        like = {
            'entry_id': entry_id,
            'entry_type': entry_type,
            'uid': l['id']
        }
        Like.insert(**like).on_conflict('replace').execute()

    print(f'        crawled {r["likeCount"]} likes on {entry_type} {entry_id}')
    return r['likeCount']
