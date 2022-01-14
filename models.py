# coding: utf8

from peewee import SqliteDatabase, Model, BooleanField, IntegerField, DateTimeField, CharField
from playhouse.shortcuts import model_to_dict

from config import config


database = SqliteDatabase(config.DATABASE)


class BaseModel(Model):
    class Meta:
        database = database

    @classmethod
    def create_or_update(cls, data):
        ex_data = cls.get_or_none(**data)
        if ex_data:
            ex_data = model_to_dict(ex_data)
            ex_data.update(data)
        else:
            ex_data = data

        cls.insert(**ex_data).on_conflict_replace().execute()

        return cls.get_or_none(**ex_data)


class FetchedUser(BaseModel):
    uid = IntegerField(unique=True, primary_key=True)
    name = CharField()
    headPic = CharField()
    status = IntegerField()
    gossip = IntegerField()
    album = IntegerField()
    photo = IntegerField()
    blog = IntegerField()


class User(BaseModel):
    uid = IntegerField(unique=True, primary_key=True)
    name = CharField()
    headPic = CharField()


class Comment(BaseModel):
    id = IntegerField(unique=True, primary_key=True)
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
    id = IntegerField(unique=True, primary_key=True)
    uid = IntegerField(index=True)
    t = DateTimeField(index=True)
    content = CharField(default="")
    headPic = CharField(default="")
    like = IntegerField(default=0)
    repeat = IntegerField(default=0)
    comment = IntegerField(default=0)
    rootContent = CharField(default="")
    rootPic = CharField(default="")
    rootUid = IntegerField(default=0)
    rootUname = CharField(default="")
    location = CharField(default="")
    locationUrl = CharField(default="")


class Gossip(BaseModel):
    id = IntegerField(unique=True, primary_key=True)
    uid = IntegerField(index=True)
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


class Blog(BaseModel):
    id = IntegerField(unique=True, primary_key=True)
    uid = IntegerField(index=True)
    t = DateTimeField(index=True)
    category = CharField()
    title = CharField()
    summary = CharField()
    content = CharField()
    comment = IntegerField()
    share = IntegerField()
    like = IntegerField()
    read = IntegerField()


class Album(BaseModel):
    id = IntegerField(unique=True, primary_key=True)
    uid = IntegerField(index=True)
    name = CharField()
    desc = CharField()
    cover = CharField()
    count = IntegerField()
    comment = IntegerField()
    share = IntegerField()
    like = IntegerField()


class Photo(BaseModel):
    id = IntegerField(unique=True, primary_key=True)
    uid = IntegerField(index=True)
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
