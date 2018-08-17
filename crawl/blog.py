# coding: utf8

from datetime import datetime
import json

from config import config
from models import Blog

from .utils import get_comments, get_likes


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
        id = int(b['id'])
        blog = {
            'id': id,
            'uid': uid,
            't': datetime.strptime(b['createTime'], "%y-%m-%d %H:%M:%S"),
            'category': b['category'],
            'title': b['title'],
            'summary': b['summary'],
            'comment': b['commentCount'],
            'share': b['shareCount'],
            'like': b['likeCount'],
            'read': b['readCount']
        }

        blog['content'] = load_blog_content(id, uid)

        Blog.insert(**blog).on_conflict('replace').execute()

        total_comment = 0
        if blog['comment']:
            get_comments(id, 'blog', owner=uid)
        if blog['comment'] or blog['share']:
            total_comment = get_comments(id, 'blog', global_comment=True, owner=uid)
        if blog['like']:
            get_likes(id, 'blog')

        print(u'  crawled blog {id} {title} with {comment}/{share}/{like}/{read}, and {total_comment}'.format(
            id=id,
            title=blog['title'],
            comment=blog['comment'],
            share=blog['share'],
            like=blog['like'],
            read=blog['read'],
            total_comment=total_comment
        ))

    return r['count']


def get_blogs(uid=crawler.uid):
    cur_page = 0
    total = config.BLOGS_PER_PAGE
    while cur_page*config.BLOGS_PER_PAGE < total:
        print('start crawl blog list page {cur_page}'.format(cur_page=cur_page))
        total = load_blog_list(cur_page, uid)
        cur_page += 1

    return total
