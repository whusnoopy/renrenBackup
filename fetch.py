# coding: utf8 

from workaround import status as crawl_status
from workaround import gossip as crawl_gossip
from config import config

from models import database, User, Status, StatusComment, StatusLike, Gossip

with database:
    database.create_tables([User, Status, StatusComment, StatusLike, Gossip])
    # status_count = crawl_status.get_status()
    gossip_count = crawl_gossip.get_gossip()
