# coding: utf8

from datetime import datetime
import re

from config import config
from models import Gossip

from .utils import get_image


crawler = config.crawler
normal_pattern = re.compile(r'<span style="color:#[0-9a-fA-F]*">(.*)</span>')

total_pattern = r'<input id="gossipCount" type="hidden" name="" value="(\d+)" />'


def load_gossip_page(page, uid=crawler.uid):
    param = {
        "id": uid,
        "page": page,
        "guest": crawler.uid,
    }
    r = crawler.get_json(config.GOSSIP_URL, params=param, method='POST')

    for c in r['array']:
        local_pic = get_image(c['tinyUrl']) if 'tinyUrl' in c else config.DEFAULT_HEAD_PIC

        gossip = {
            'id': c['id'],
            'uid': uid,
            't': datetime.strptime(c['time'], "%Y-%m-%d %H:%M"),
            'guestId': c['guestId'],
            'guestName': c['guestName'],
            'headPic': local_pic,    # 居然保存的是当时的头像，这里不能往 User 表里塞了
            'attachSnap': get_image(c.get('headUrl', '')),
            'attachPic': get_image(c.get('largeUrl', '')),
            'whisper': c['whisper'] == 'true',
            'wap': c['wap'] == 'true',
            'gift': c['giftImg'] if c['gift'] == 'true' else '',
            'content': ''
        }

        # 内容出现在好几个地方，body, filterdBody, filterOriginBody
        # filterOriginBody 是连表情都没转义的
        # filterdBody 加了表情转义，但也加了那个坑爹的 <span style="color:#000000">
        #     还有手机发布的 <xiaonei_wap/>，和送礼物带的 <xiaonei_gift />

        body = c['filterdBody'].replace('\n', '<br>').replace('<xiaonei_wap/>', '')
        if gossip['gift']:
            body = re.sub(r'<xiaonei_gift img="http:[\.a-z0-9/]*"/>', '', body)
        patt = normal_pattern.findall(body)
        if not patt:
            try:
                print(u'ERROR on parsing gossip body:\n  {body}'.format(body=c["filterdBody"]))
            except UnicodeEncodeError:
                print('ERROR on parsing gossip body, check origin filterBody')
        else:
            gossip['content'] = patt[0]

        Gossip.insert(**gossip).on_conflict('replace').execute()

    count = len(r["array"])
    print('  crawled {count} gossip on page {page}'.format(
        count=count,
        page=page
    ))
    return count


def get_gossip(uid=crawler.uid):
    resp = crawler.get_url(config.GOSSIP_PAGE_URL.format(uid=uid))

    try:
        total = int(re.findall(total_pattern, resp.text)[0])
    except IndexError:
        print("Don't have permission to read {uid}'s gossip page".format(uid=uid))
        return 0

    cur_page = 0
    crawled_total = 0
    while cur_page*config.ITEMS_PER_PAGE < total:
        print('start crawl gossip page {cur_page}'.format(cur_page=cur_page))
        crawled_total += load_gossip_page(cur_page, uid)
        cur_page += 1

    return crawled_total
