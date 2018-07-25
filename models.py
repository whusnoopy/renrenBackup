# coding: utf8

from peewee import SqliteDatabase, Model, BooleanField, IntegerField, DateTimeField, CharField

from config import config


database = SqliteDatabase(config.DATABASE)


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    uid = IntegerField(unindexed=True)
    name = CharField()
    headPic = CharField()


class Comment(BaseModel):
    id = IntegerField(unique=True)
    t = DateTimeField(index=True)
    entry_id = IntegerField(index=True)
    entry_type = CharField(index=True)
    authorId = IntegerField()
    authorName = CharField()
    content = CharField()


class Like(BaseModel):
    entry_id = IntegerField(index=True)
    entry_type = CharField()
    uid = IntegerField()

    class Meta:
        indexes = (
            (('entry_id', 'uid'), True),
        )


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


class Gossip(BaseModel):
    id = IntegerField(unique=True)
    t = DateTimeField(index=True)
    guestId = IntegerField(index=True)
    guestName = CharField()
    headPic = CharField()
    attachSnap = CharField()
    attachPic = CharField()
    whisper = BooleanField()
    wap = BooleanField()
    gift = CharField()
    content = CharField()


class Note(BaseModel):
    pass


class Album(BaseModel):
    id = IntegerField(unique=True)
    name = CharField()
    desc = CharField()
    cover = CharField()
    count = IntegerField()
    comment = IntegerField()
    share = IntegerField()
    like = IntegerField()


class Photo(BaseModel):
    id = IntegerField(unique=True)
    album_id = IntegerField(index=True)
    pos = IntegerField(index=True)
    prev = IntegerField()
    next = IntegerField()
    t = DateTimeField()
    title = CharField()
    src = CharField()
    comment = IntegerField()
    share = IntegerField()
    like = IntegerField()
    view = IntegerField()


class Share(BaseModel):
    pass
