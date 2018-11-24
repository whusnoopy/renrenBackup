# coding: utf8

from datetime import datetime
import logging

from config import config
from models import Blog

from .utils import get_comments, get_likes


logger = logging.getLogger(__name__)
crawler = config.crawler


def load_blog_content(blog_id, uid=crawler.uid):
    raw_html = crawler.get_url(config.BLOG_DETAIL_URL.format(uid=uid, blog_id=blog_id))
    st = raw_html.text.find('<div id="blogContent" class="blogDetail-content"')
    st = raw_html.text.find('\n', st)
    ed = raw_html.text.find('</div>\r', st)

    return raw_html.text[st:ed].strip()


def load_blog_list(page, uid=crawler.uid):
    r = crawler.get_json(config.BLOG_LIST_URL.format(uid=uid), {'curpage': page})

    for b in r['data']:
        bid = int(b['id'])
        blog = {
            'id': bid,
            'uid': uid,
            't': datetime.strptime(b['createTime'], "%y-%m-%d %H:%M:%S"),
            'category': b.get('category', '默认分类'),
            'title': b['title'],
            'summary': b['summary'],
            'comment': b['commentCount'],
            'share': b['shareCount'],
            'like': b['likeCount'],
            'read': b['readCount']
        }

        blog['content'] = load_blog_content(bid, uid)

        Blog.insert(**blog).on_conflict('replace').execute()

        total_comment = 0
        if blog['comment']:
            get_comments(bid, 'blog', owner=uid)
        if blog['comment'] or blog['share']:
            total_comment = get_comments(bid, 'blog', global_comment=True, owner=uid)
        if blog['like']:
            get_likes(bid, 'blog')

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

    return r['count']


def get_blogs(uid=crawler.uid):
    cur_page = 0
    total = config.BLOGS_PER_PAGE
    while cur_page*config.BLOGS_PER_PAGE < total:
        logger.info('start crawl blog list page {cur_page}'.format(cur_page=cur_page))
        total = load_blog_list(cur_page, uid)
        cur_page += 1

    return total
