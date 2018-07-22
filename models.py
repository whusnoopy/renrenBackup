# coding: utf8

from peewee import SqliteDatabase, Model, IntegerField, DateTimeField, CharField

from config import config


database = SqliteDatabase(config.DATABASE)


class BaseModel(Model):
    class Meta:
        database = database


class Status(BaseModel):
    id = IntegerField(unique=True)
    t = DateTimeField(index=True)
    content = CharField(default="")
    like = IntegerField(default=0)
    repeat = IntegerField(default=0)
    comment = IntegerField(default=0)
    rootContent = CharField(default="")
    rootUid = IntegerField(default=0)
    rootUname = CharField(default="")
