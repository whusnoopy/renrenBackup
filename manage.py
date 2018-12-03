# coding: utf8

import getpass
import logging
import logging.config

from flask_script import Manager

from config import config

from crawl.crawler import Crawler
from fetch import prepare_db, fetch_user, update_fetch_info
from web import app
from export import export_all


logging.config.dictConfig(config.LOGGING_CONF)
logger = logging.getLogger(__name__)
manager = Manager(app)


@manager.command
def fetch(email='', password='',
          status=False, gossip=False, album=False, blog=False,
          refresh_count=False, uid=0):
    if not email:
        email = input("Input renren account email (aka. username@renren.com): ")
    if not password:
        password = getpass.getpass("Input renren password (will not show): ")

    prepare_db()

    config.crawler = Crawler(email, password, Crawler.load_cookie())
    uid = uid or config.crawler.uid

    fetched = fetch_user(uid, fetch_status=status, fetch_gossip=gossip, fetch_album=album, fetch_blog=blog)

    if not fetched:
        logger.info('nothing need to fetch, just test login')

    if fetched or refresh_count:
        update_fetch_info(uid)


@manager.command
def export(filename=config.BAK_OUTPUT_TAR):
    client_app = app.test_client()
    export_all(filename, client_app)


if __name__ == "__main__":
    manager.run()
