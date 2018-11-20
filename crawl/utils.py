# coding: utf8

from datetime import datetime
import os
import re

from config import config
from models import User, Comment, Like


crawler = config.crawler


def get_image(img_url):
    if not img_url:
        return ''

    last_loc_http = img_url.rfind('http:')
    # when there are more than one occurences of http:
    # We will crop the str and leave the last one
    if last_loc_http > 0:
        img_url = img_url[last_loc_http:]

    path = img_url.split('/')
    path[0] = 'static'
    path[1] = 'img'
    path[2] = path[2].replace('.', '_')

    filename = '/'.join(path)
    filepath = '/'.join(path[:-1])

    if os.path.exists(filename):
        return '/{filename}'.format(filename=filename)

    if not os.path.exists(filepath):
        os.makedirs(filepath)

    resp = crawler.get_url(img_url)
    with open(filename, 'wb') as fp:
        fp.write(resp.content)

    print('        get image {img_url} to local'.format(img_url=img_url))
    return '/{filename}'.format(filename=filename)


def save_user(uid, name, pic=None):
    user = {
        'uid': uid,
        'name': name,
        'headPic': get_image(pic) if pic else config.DEFAULT_HEAD_PIC,
    }
    User.insert(**user).on_conflict('replace').execute()

    return uid


def get_user(uid):
    resp = crawler.get_url(config.HOMEPAGE_URL.format(uid=uid))

    name = re.findall(r"var	profileOwnerName = '(.*)';", resp.text)[0]
    pic = re.findall(r'<img width="177" src="(.*)" id="userpic" />', resp.text)[0]
    pic = pic.replace('main_', 'tiny_')

    try:
        print(u'    get user {uid} {name} with {pic}'.format(uid=uid, name=name, pic=pic))
    except UnicodeEncodeError:
        print('    get user {uid} with {pic}'.format(uid=uid, pic=pic))
    return save_user(uid, name, pic)


def get_comments(entry_id, entry_type, global_comment=False, owner=crawler.uid):
    comment_url = config.GLOBAL_COMMENT_URL if global_comment else config.COMMENT_URL
    save_type = 'share' if global_comment else entry_type
    param = {
        "entryOwnerId": owner,
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
            authorId = c.get('authorId', 0)
            authorName = c.get('authorName', '已注销用户')

            save_user(authorId, authorName, c.get('authorHeadUrl', None))

            comment = {
                'id': c['id'],
                't': datetime.fromtimestamp(int(c['createTimeMillis'])/1000),
                'entry_id': entry_id,
                'entry_type': save_type,
                'authorId': authorId,
                'authorName': authorName,
                'content': c['content']
            }
            Comment.insert(**comment).on_conflict('replace').execute()

        offset += config.ITEMS_PER_PAGE

    print('        crawled {total}{is_global} comments on {entry_type} {entry_id}'.format(
        total=total,
        is_global=" global" if global_comment else "",
        entry_type=entry_type,
        entry_id=entry_id
    ))
    return total


def get_likes(entry_id, entry_type, owner=crawler.uid):
    param = {
        "stype": entry_type,
        "sourceId": entry_id,
        "owner": owner,
        "gid": '{entry_type}_{entry_id}'.format(entry_type=entry_type, entry_id=entry_id),
        "uid": crawler.uid
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

    print('        crawled {count} likes on {entry_type} {entry_id}'.format(
        count=len(r['likeList']),
        entry_type=entry_type,
        entry_id=entry_id
    ))
    return r['likeCount']
