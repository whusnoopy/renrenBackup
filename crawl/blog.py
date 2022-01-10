# coding: utf8

from datetime import datetime
import logging

from config import config
from models import Blog

from .utils import get_comments, get_likes, get_payload


logger = logging.getLogger(__name__)
crawler = config.crawler


def load_blog_content(blog_id, uid=crawler.uid):
    page = crawler.get_url(f'https://renren.com/feed/{blog_id}/{uid}')

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page.content, 'html.parser')

    blog_content = soup.find_all('div', class_='blog-content')[0]
    div_text = blog_content.find_all('div', class_='text')[0]
    return str(div_text.findChild())


def load_blog_list(uid=crawler.uid, after=None):
    r = crawler.get_json(config.BLOG_LIST_API, json_=get_payload(uid, after), method='POST')
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

        total_comment = 0
        # if blog['comment']:
        #     get_comments(bid, 'blog', owner=uid)
        # if blog['comment'] or blog['share']:
        #     total_comment = get_comments(bid, 'blog', global_comment=True, owner=uid)
        # if blog['like']:
        #     get_likes(bid, 'blog')

        try:
            logger.info(u'  crawled blog {bid} {title} with 评{comment}/分{share}/赞{like}/读{read}'.format(
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

        logger.info('      and total comments {total_comment}'.format(total_comment=total_comment))

    return r['count'], r['tail_id']


def get_blogs(uid=crawler.uid):
    cur_page = 0
    total = 0
    after = None
    while True:
        logger.info('start crawl blog list page {cur_page}'.format(cur_page=cur_page))
        count, after = load_blog_list(uid, after)
        if count == 0:
            break
        total += count
        cur_page += 1

    return total
