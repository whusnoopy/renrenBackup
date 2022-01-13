# coding: utf8

from datetime import datetime
import hashlib
import logging
import os
import re

from config import config
from models import User, Comment, Like


logger = logging.getLogger(__name__)
crawler = config.crawler


def is_bad_image(filename):
    with open(filename, 'rb') as fp:
        data = fp.read()
        md5 = hashlib.md5(data).hexdigest()
        return md5 == config.BAD_IMAGE_MD5


def get_image(img_url, retry=0):
    if not img_url:
        return ''

    path = img_url.split('/')
    path[0] = 'static'
    path[1] = 'img'
    path[2] = path[2].replace('.', '_')

    filename = '/'.join(path)
    filepath = '/'.join(path[:-1])

    if os.path.exists(filename) and not is_bad_image(filename):
        return '/{filename}'.format(filename=filename)

    if not os.path.exists(filepath):
        os.makedirs(filepath)

    try:
        resp = crawler.get_url(img_url)
    except TimeoutError:
        logger.fatal('get img {img_url} failed, use blank instead'.format(img_url=img_url))
        return config.DEFAULT_HEAD_PIC

    with open(filename, 'wb') as fp:
        fp.write(resp.content)

    logger.info('        get image {img_url} to local'.format(img_url=img_url))
    if is_bad_image(filename) and retry < config.RETRY_TIMES:
        return get_image(img_url, retry=retry + 1)    
    elif retry >= config.RETRY_TIMES:
        logger.fatal('get good img {img_url} failed, skip'.format(img_url=img_url))
    return '/{filename}'.format(filename=filename)


def save_user(uid, name, pic=None):
    logger.debug(u'try to save {uid}[{name}] with headPic {pic}'.format(uid=uid, name=name, pic=pic))

    if pic:
        # 对各种历史脏数据做清理

        last_loc_http = pic.rfind('http:')
        # when there are more than one occurences of http:
        # We will crop the str and leave the last one
        if last_loc_http > 0:
            pic = pic[last_loc_http:]

        # 整合老 kaixin.com 数据的错误，需要去除 subdomain 里的 kx 才可以抓
        if pic.find('http://kxhdn') == 0:
            pic = pic[:7] + pic[9:]

    user = {
        'uid': uid,
        'name': name,
        'headPic': get_image(pic) if pic else config.DEFAULT_HEAD_PIC,
    }
    User.insert(**user).on_conflict('replace').execute()

    logger.debug(u'saved {uid}[{name}] with headPic {pic}'.format(uid=uid, name=name, pic=user['headPic']))
    return uid


def get_user(uid):
    resp = crawler.get_url(config.HOMEPAGE_URL.format(uid=uid))

    name = re.findall(r'"usersBasicInfo":{"userInfo":{"id":.*?,"name":"","nickname":"(.*?)",', resp.text)[0]
    pic = eval('"' + re.findall(r'"largeUrl":"(.*?)",', resp.text)[0] + '"')

    try:
        logger.info(u'    get user {uid} {name} with {pic}'.format(uid=uid, name=name, pic=pic))
    except UnicodeEncodeError:
        logger.info('    get user {uid} with {pic}'.format(uid=uid, pic=pic))
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

    logger.info('        crawled {total}{is_global} comments on {entry_type} {entry_id}'.format(
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

    logger.info('        crawled {count} likes on {entry_type} {entry_id}'.format(
        count=len(r['likeList']),
        entry_type=entry_type,
        entry_id=entry_id
    ))
    return r['likeCount']


def get_common_payload(uid, after=None):
    payload = crawler.get_payload()
    payload.update({
        "app_ver": "1.0.0",
        "count": 20,
        "home_id": f"{crawler.uid}",
        "product_id": 2080928,
        "uid": uid,
        }
    )
    
    if after:
        payload['after'] = after

    crawler.add_payload_signature(payload)
    return payload


def check_login():
    if not crawler.uid:
        return False
    if crawler.get_json(config.STATUS_URL, json_=get_common_payload(crawler.uid), method='POST')['errorCode'] != 0:
        logger.fatal('  login expired, re-login')
        return False
    else:
        return True
