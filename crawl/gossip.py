# coding: utf8

from datetime import datetime
import logging
import re

from config import config
from models import Gossip

from .utils import get_image, get_payload, add_signature


logger = logging.getLogger(__name__)
crawler = config.crawler

normal_pattern = re.compile(r'<span style="color:#[0-9a-fA-F]*">(.*)</span>')
total_pattern = r'<input id="gossipCount" type="hidden" name="" value="(\d+)" />'


def get_gossip_payload(uid=crawler.uid, offset=0):
    payload = get_payload(uid)
    del payload['app_ver']
    del payload['count']
    del payload['product_id']
    payload['limit'] = 10
    payload['offset'] = offset
    payload['ownerId'] = payload.pop('uid')
    del payload['home_id']
    del payload['sig']
    add_signature(payload)
    return payload


def load_gossip_page(uid=crawler.uid, offset=0):
    r = crawler.get_json(config.GOSSIP_URL, json_=get_gossip_payload(uid, offset), method='POST')

    for c in r['data']['gossipList']:
        local_pic = get_image(c.get('senderHeadUrl', config.DEFAULT_HEAD_PIC))

        gossip = {
            'id': c['id'],
            'uid': uid,
            't': datetime.fromtimestamp(datetime.strptime(c['time'], "%Y-%m-%dT%H:%M:%S.%f%z").timestamp()), # for some reason, a conversion is needed
            'guestId': c['sender'],
            'guestName': c['senderName'],
            'headPic': local_pic,    # 居然保存的是当时的头像，这里不能往 User 表里塞了
            'attachSnap': get_image(c.get('headUrl', '')),
            'attachPic': get_image(c.get('largeUrl', '')),
            'whisper': 'xiaonei_only_to_me' in c['body'],
            'wap': False, # c['wap'] == 'true',
            'gift': '', # c['giftImg'] if c['gift'] == 'true' else '',
            'content': ''
        }

        body = c['body']
        # remove gift
        body = re.sub(r'<xiaonei_gift img="http:[\.a-z0-9/]*"/>', '', body)
        # remove xiaonei_only_to_me
        body = re.sub(r'<xiaonei_only_to_me/><Toid/>\d+$', '', body)

        gossip['content'] = body

        Gossip.insert(**gossip).on_conflict('replace').execute()

    count = len(r["data"]['gossipList'])
    logger.info('  crawled {count} gossip on page {page}'.format(
        count=count, page=offset // 10
    ))
    if offset + count == r['data']['count']:
        return count, -1
    return count, offset + count


def get_gossip(uid=crawler.uid):
    cur_page = 0
    crawled_total = 0
    offset = 0
    while True:
        logger.info('start crawl gossip page {cur_page}'.format(cur_page=cur_page))
        count, offset = load_gossip_page(uid, offset)
        crawled_total += count
        if offset == -1:
            break
        cur_page += 1

    return crawled_total
