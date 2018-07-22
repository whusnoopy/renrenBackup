# coding: utf8 

from workaround import status as crawl_status
from config import config

from models import database, Status

with database:
    database.create_tables([Status])
    status_list = crawl_status.get_status()
    for s in status_list:
        Status.create(**s)

    for s in Status.select():
        print(s)
