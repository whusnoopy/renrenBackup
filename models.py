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
    entry_type = CharField()
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


class StatusComment(BaseModel):
    id = IntegerField(unique=True)
    status_id = IntegerField(index=True)
    t = DateTimeField(index=True)
    authorId = IntegerField()
    authorName = CharField()
    content = CharField()


class StatusLike(BaseModel):
    status_id = IntegerField(index=True)
    uid = IntegerField()

    class Meta:
        indexes = (
            (('uid', 'status_id'), True),
        )

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
    pass


class Share(BaseModel):
    pass
