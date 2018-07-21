# coding: utf8 

import sqlite3

from workaround import status as crawl_status
from config import config


class Database(object):
    def __init__(self):
        pass

    def __enter__(self):
        self.conn = sqlite3.connect("user{}.db".format(config.COOKIES['id']))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def init_db(self):
        c = self.conn.cursor()
        # status
        try:
            c.execute('''CREATE TABLE status
                        (id INTEGER, t INTEGER, content TEXT,
                        like INTEGER, repeat INTEGER, comment INTEGER)''')
        except sqlite3.OperationalError as oe:
            print(oe)

        c.close()
        self.conn.commit()


with Database() as db:
    status_list = crawl_status.get_status()

    insert_list = [(s['id'], s['t'], s['content'], s['like'], s['repeat'], s['comment']) for s in status_list]
    db.init_db()
    c = db.conn.cursor()
    c.executemany('INSERT INTO status (id, t, content, like, repeat, comment) VALUES (?, ?, ?, ?, ?, ?)', insert_list)
    c.close()
    db.conn.commit()
