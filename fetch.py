# coding: utf8

import argparse

from config import config


parser = argparse.ArgumentParser(description="fetch renren data to backup")
parser.add_argument('email', help="your renren email for login")
parser.add_argument('password', help="your renren password for login")
parser.add_argument('-s', '--fetch-status', help="fetch status or not", action="store_true")
parser.add_argument('-g', '--fetch-gossip', help="fetch gossip or not", action="store_true")
parser.add_argument('-a', '--fetch-album', help="fetch album or not", action="store_true")
parser.add_argument('-b', '--fetch-blog', help="fetch blog or not", action="store_true")
args = parser.parse_args()


from crawl.crawler import Crawler

config.crawler = Crawler(args.email, args.password)


if not (args.fetch_status or args.fetch_gossip or args.fetch_album or args.fetch_blog):
    print('nothing need to fetch, just test login')


from models import database, User, Comment, Like
with database:
    database.create_tables([User, Comment, Like])

    if args.fetch_status:
        print('prepare to fetch status')
        from models import Status
        from crawl import status as crawl_status

        database.create_tables([Status])
        status_count = crawl_status.get_status()
        print(f'fetched {status_count} status')

    if args.fetch_gossip:
        print('prepare to fetch gossip')
        from models import Gossip
        from crawl import gossip as crawl_gossip

        database.create_tables([Gossip])
        gossip_count = crawl_gossip.get_gossip()
        print(f'fetched {gossip_count} gossips')

    if args.fetch_album:
        print('prepare to fetch albums')
        from models import Album, Photo
        from crawl import album as crawl_album

        database.create_tables([Album, Photo])
        album_count = crawl_album.get_albums()
        print(f'fetched {album_count} albums')

    if args.fetch_blog:
        print('prepare to fetch blogs')
        from models import Blog
        from crawl import blog as crawl_blog

        database.create_tables([Blog])
        blog_count = crawl_blog.get_blogs()
        print(f'fetched {blog_count} blogs')
