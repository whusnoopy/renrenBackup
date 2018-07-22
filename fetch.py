# coding: utf8 

from workaround import status as crawl_status
from config import config

from models import database, User, Status, StatusComment, StatusLike

with database:
    database.create_tables([User, Status, StatusComment, StatusLike])
    status_list = crawl_status.get_status()
