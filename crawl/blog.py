# coding: utf8

from datetime import datetime
import json

from config import crawl_config as config
from models import Blog

from .crawler import crawler
from .utils import get_comments, get_likes


def load_blog_content(blog_id):
    raw_html = crawler.get_url(config.BLOG_DETAIL_URL.format(uid=config.UID, blog_id=blog_id))
    st = raw_html.text.find('<div id="blogContent" class="blogDetail-content"')
    st = raw_html.text.find('\n', st)
    ed = raw_html.text.find('</div>\r', st)

    return raw_html.text[st:ed].strip()


def load_blog_list(page):
    r = crawler.get_json(config.BLOG_LIST_URL.format(uid=config.UID), {'curpage': page})

    for b in r['data']:
        id = int(b['id'])
        blog = {
            'id': id,
            't': datetime.strptime(b['createTime'], "%y-%m-%d %H:%M:%S"),
            'category': b['category'],
            'title': b['title'],
            'summary': b['summary'],
            'comment': b['commentCount'],
            'share': b['shareCount'],
            'like': b['likeCount'],
            'read': b['readCount']
        }

        blog['content'] = load_blog_content(id)

        Blog.insert(**blog).on_conflict('replace').execute()

        total_comment = 0
        if blog['comment']:
            get_comments(id, 'blog')
        if blog['comment'] or blog['share']:
            total_comment = get_comments(id, 'blog', global_comment=True)
        if blog['like']:
            get_likes(id, 'blog')

        print(f'  crawled blog {id} {blog["title"]} with {blog["comment"]}/{blog["share"]}/'
              f'{blog["like"]}/{blog["read"]}, and {total_comment}')

    return r['count']

def get_blogs():
    cur_page = 0
    total = config.BLOGS_PER_PAGE
    while cur_page*config.BLOGS_PER_PAGE < total:
        print(f'start crawl blog list page {cur_page}')
        total = load_blog_list(cur_page)
        cur_page += 1

    return total
