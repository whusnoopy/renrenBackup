# coding: utf8

import json

from .crawler import crawler
from config import config


def load_status_page(page):
    status_list = list()
    resp = crawler.get_url(config.STATUS_URL, {'uid': config.COOKIES['id'], 'curpage': page})
    r = json.loads(resp.text)

    likes = r['likeInfoMap']
    for s in r['doingArray']:
        status = {
            'id': s['id'],
            't': int(s['createTime'])/1000,
            'content': s['content'],                            # 内容
            'like': likes.get('status_{}'.format(s['id']), 0),  # 点赞
            'repeat': s['repeatCountTotal'],                    # 转发
            'comment': s['comment_count'],                      # 评论
            'rootContent': s.get('rootContent', ''),            # 如果是转发，转发的原文
            'rootUid': s.get('rootDoingUserId', ''),            # 转发原 uid
            'rootUname': s.get('rootDoingUserName', ''),        # 转发原 username
        }
        status_list.append(status)

    return r['count'], status_list

def get_status():
    status_list = list()
    cur_page = 0
    total = 20
    while cur_page*20 < total:
        print(f'start crawl status page {cur_page}')
        total, cur_page_status = load_status_page(cur_page)
        status_list.extend(cur_page_status)
        print(f'{len(cur_page_status)} fetched, {len(status_list)}/{total}')
        cur_page += 1

    return status_list
