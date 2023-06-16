# coding: utf8
# pylint: disable=C0415

import logging
import logging.config

from playhouse.shortcuts import model_to_dict

from config import config


logging.config.dictConfig(config.LOGGING_CONF)
logger = logging.getLogger(__name__)


def prepare_db():
    from models import database, FetchedUser, User, Comment, Like
    from models import Status, Gossip, Album, Photo, Blog

    with database:
        database.create_tables([FetchedUser, User, Comment, Like])
        database.create_tables([Status, Gossip, Album, Photo, Blog])


def update_fetch_info(uid):
    from models import database, FetchedUser, User, Status, Gossip, Album, Photo, Blog

    with database:
        user = User.get_or_none(User.uid == uid)
        if not user:
            raise KeyError("no such user")

        fetched_info = model_to_dict(user)
        fetched_info.update(
            status=Status.select().where(Status.uid == uid).count(),
            gossip=Gossip.select().where(Gossip.uid == uid).count(),
            album=Album.select().where(Album.uid == uid).count(),
            photo=Photo.select().where(Photo.uid == uid).count(),
            blog=Blog.select().where(Blog.uid == uid).count(),
        )

        FetchedUser.insert(**fetched_info).on_conflict("replace").execute()

        logger.info(
            "update fetched info {fetched_info}".format(fetched_info=fetched_info)
        )

        return fetched_info


def fetch_status(uid):
    logger.info("prepare to fetch status")
    from crawl import status as crawl_status

    status_count = crawl_status.get_status(uid)
    logger.info("fetched {status_count} status".format(status_count=status_count))


def fetch_gossip(uid):
    logger.info("prepare to fetch gossip")
    from crawl import gossip as crawl_gossip

    gossip_count = crawl_gossip.get_gossip(uid)
    logger.info("fetched {gossip_count} gossips".format(gossip_count=gossip_count))


def fetch_album(uid):
    logger.info("prepare to fetch albums")
    from crawl import album as crawl_album

    album_count = crawl_album.get_albums(uid)
    logger.info("fetched {album_count} albums".format(album_count=album_count))


def fetch_blog(uid):
    logger.info("prepare to fetch blogs")
    from crawl import blog as crawl_blog

    blog_count = crawl_blog.get_blogs(uid)
    logger.info("fetched {blog_count} blogs".format(blog_count=blog_count))


def fetch_user(uid, **kwargs):
    fetched_flag = False

    from crawl.utils import get_user

    get_user(uid)

    if kwargs.get("fetch_status"):
        fetch_status(uid)
        fetched_flag = True

    if kwargs.get("fetch_gossip"):
        fetch_gossip(uid)
        fetched_flag = True

    if kwargs.get("fetch_album"):
        fetch_album(uid)
        fetched_flag = True

    if kwargs.get("fetch_blog"):
        fetch_blog(uid)
        fetched_flag = True

    return fetched_flag
