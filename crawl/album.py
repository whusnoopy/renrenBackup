# coding: utf8

from datetime import datetime
import json
import re

from config import config
from models import Album, Photo

from .utils import get_image, get_comments, get_likes


crawler = config.crawler


def get_album_summary(album_id, uid=crawler.uid):
    resp = crawler.get_url(config.ALBUM_SUMMARY_URL.format(uid=uid, album_id=album_id))
    first_photo_id = re.findall(r'"photoId":"(\d+)",', resp.text)[0]

    layer = crawler.get_json(config.PHOTO_INFO_URL.format(uid=uid, photo_id=first_photo_id))

    cover = layer['album']['fullLargeUrl']
    if not cover or cover == "http://img.xiaonei.com/photos/0/0/large.jpg":
        cover = layer['list'][0]['large']

    album = {
        'id': album_id,
        'uid': uid,
        'name': layer['album']['name'],
        'desc': layer['album']['description'],
        'cover': get_image(cover),
        'count': layer['album']['photoCount'],
        'comment': layer['album']['commentcount'],
        'share': layer['album']['shareCount'],
        'like': get_likes(album_id, 'album')
    }
    Album.insert(**album).on_conflict('replace').execute()
    if album['comment']:
        get_comments(album_id, 'album', owner=uid)
    if album['comment'] or album['share']:
        get_comments(album_id, 'album', global_comment=True, owner=uid)

    print(u'    fetch album {album_id} {name} ({desc}), {comment}/{share}/{like}'.format(
        album_id=album_id,
        name=album['name'],
        desc=album['desc'],
        comment=album['comment'],
        share=album['share'],
        like=album['like']
    ))

    photo_list = layer['list']
    photo_count = len(photo_list)
    for idx, p in enumerate(photo_list):
        pid = int(p['id'])
        date_str = p['date'] if config.py3 else p['date'].encode('utf8')
        photo = {
            'id': pid,
            'uid': uid,
            'album_id': album_id,
            'pos': idx,
            'prev': int(photo_list[idx-1]['id']),
            'next': int(photo_list[idx-photo_count+1]['id']),
            't': datetime.strptime(date_str, '%Y年%m月%d日'),
            'title': p['title'],
            'src': get_image(p['large']),
            'comment': p['commentCount'],
            'share': p['shareCount'],
            'like': get_likes(pid, 'photo'),
            'view': p['viewCount']
        }
        Photo.insert(**photo).on_conflict('replace').execute()
        if photo['comment']:
            get_comments(pid, 'photo', owner=uid)
        if photo['comment'] or photo['share']:
            get_comments(pid, 'photo', global_comment=True, owner=uid)

        print(u'      photo {pid}: {title}, {comment}/{share}/{like}/{view}'.format(
            pid=pid,
            title=p['title'][:24],
            comment=photo['comment'],
            share=photo['share'],
            like=photo['like'],
            view=photo['view']
        ))

    return album['count']


def get_album_list_page(page, uid=crawler.uid):
    param = {
        'offset': page*config.ITEMS_PER_PAGE,
        'limit': config.ITEMS_PER_PAGE
    }
    resp = crawler.get_url(config.ALBUM_LIST_URL.format(uid=uid), param)
    albums = json.loads(re.findall(r"'albumList': (\[.*\]),", resp.text)[0])

    for a in albums:
        aid = int(a['albumId'])
        print(u'    album {aid}: {name}, has {count} photos'.format(
            aid=aid,
            name=a['albumName'],
            count=a['photoCount']
        ))
        if a["photoCount"]:
            get_album_summary(aid, uid)

    count = len(albums)
    print('  get {count} albums on list page {page}'.format(count=count, page=page))
    return count


def get_albums(uid=crawler.uid):
    cur_page = 0
    total = 1
    while cur_page*config.ITEMS_PER_PAGE < total:
        print('start crawl album list page {cur_page}'.format(cur_page=cur_page))
        total += get_album_list_page(cur_page, uid)
        cur_page += 1

    return total
