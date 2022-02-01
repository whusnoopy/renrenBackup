# coding: utf8

from datetime import datetime
import logging

from config import config
from models import Blog

from .utils import get_common_payload


logger = logging.getLogger(__name__)
crawler = config.crawler


def load_blog_content(blog_id, uid=crawler.uid):
    raw_html = crawler.get_url(config.BLOG_DETAIL_URL.format(uid=uid, blog_id=blog_id))

    st = raw_html.text.find('<div class="blog-content">')
    st = raw_html.text.find('<label>', st)
    ed = raw_html.text.find('</div>', st)
    return raw_html.text[st:ed].strip()


def load_blog_list(uid=crawler.uid, after=None):
    r = crawler.get_json(config.BLOG_LIST_URL, json_=get_common_payload(uid, after), method='POST')

    if 'count' not in r:
        return 0, None

    for b in r['data']:
        bid = int(b['id'])
        blog = {
            'id': bid,
            'uid': b['publisher']['id'],
            't': datetime.fromtimestamp(b['publish_time'] // 1000),
            'category': b.get('category', '默认分类'),
            'title': b['body']['title'],
            'summary': b['body'].get('summary', ''),
            'comment': b['comment_count'],
            'share': b['forward_count'],
            'like': b['like_count'],
            'read': 0,
        }

        blog['content'] = load_blog_content(bid, uid)

        Blog.insert(**blog).on_conflict('replace').execute()

        try:
            logger.info('  crawled blog {bid} {title} with 评{comment}/分{share}/赞{like}/读{read}'.format(
                bid=bid,
                title=blog['title'],
                comment=blog['comment'],
                share=blog['share'],
                like=blog['like'],
                read=blog['read']
            ))
        except UnicodeEncodeError:
            logger.info('  crawled blog {bid} comment{comment}/share{share}/like{like}/read{read}'.format(
                bid=bid,
                comment=blog['comment'],
                share=blog['share'],
                like=blog['like'],
                read=blog['read']
            ))

    return r['count'], r['tail_id']


def get_blogs(uid=crawler.uid):
    cur_page = 0
    total_blogs = 0
    after = None
    while True:
        logger.info('start crawl blog list page {cur_page}'.format(cur_page=cur_page))
        count, after = load_blog_list(uid, after)
        if count == 0:
            break
        total_blogs += count
        cur_page += 1

    return total_blogs
