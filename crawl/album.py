# coding: utf8

from datetime import datetime
import logging

from config import config
from models import Album, Photo

from .utils import get_image, get_common_payload


logger = logging.getLogger(__name__)
crawler = config.crawler


def get_album_payload(uid, aid, after=None):
    payload = crawler.get_payload()
    payload.update({
        "app_ver": "1.0.0",
        "count": 10,
        "product_id": 2080928,
        "uid": uid,
        "after": after or '',
        "album_id": aid,
        }
    )
    crawler.add_payload_signature(payload)
    return payload


def get_album_summary(album_id, uid=crawler.uid):
    album_data = crawler.get_json(config.ALBUM_SUMMARY_URL, json_=get_album_payload(uid, album_id), method='POST')
    photo_list = album_data['data']

    album = {
        'id': album_id,
        'uid': uid,
        'name': album_data['album']['name'],
        'desc': '',  # album['album']['description'],
        'cover': get_image(album_data['album']['thumb_url']),
        'count': album_data['album']['size'],
        'comment': 0,  # layer['album']['commentcount'],
        'share': 0,  # layer['album']['shareCount'],
        'like': 0,  # get_likes(album_id, 'album')
    }
    Album.insert(**album).on_conflict('replace').execute()

    try:
        logger.info('    fetch album {album_id} {name} ({desc}), 评{comment}/分{share}/赞{like}'.format(
            album_id=album_id,
            name=album['name'],
            desc=album['desc'],
            comment=album['comment'],
            share=album['share'],
            like=album['like']
        ))
    except UnicodeEncodeError:
        logger.info('    fetch album {album_id}, comment{comment}/share{share}/like{like}'.format(
            album_id=album_id,
            comment=album['comment'],
            share=album['share'],
            like=album['like']
        ))

    while True:
        album_data = crawler.get_json(
            config.ALBUM_SUMMARY_URL,
            json_=get_album_payload(uid, album_id, after=album_data['tail_id']),
            method='POST'
        )
        if 'count' not in album_data:
            break
        photo_list.extend(album_data['data'])

    # There are invalid urls that missing domain names.
    def maybe_fix_url(url):
        if url.startswith('//'):
            return 'http://fmn.rrfmn.com/' + url
        return url

    photo_count = len(photo_list)
    for idx, p in enumerate(photo_list):
        pid = int(p['id'])
        photo = {
            'id': pid,
            'uid': uid,
            'album_id': album_id,
            'pos': idx,
            'prev': int(photo_list[idx-1]['id']),
            'next': int(photo_list[idx-photo_count+1]['id']),
            't': datetime.fromtimestamp(p['create_time'] // 1000),
            'title': '',  # p['title'],
            'src': get_image(maybe_fix_url(p['large_url'])),
            'comment': 0,  # p['commentCount'],
            'share': 0,  # p['shareCount'],
            'like': 0,  # get_likes(pid, 'photo'),
            'view': 0,  # p['viewCount']
        }
        Photo.insert(**photo).on_conflict('replace').execute()

        try:
            logger.info('      photo {pid}: {title}, 评{comment}/分{share}/赞{like}/看{view}'.format(
                pid=pid,
                title=photo['title'][:24],
                comment=photo['comment'],
                share=photo['share'],
                like=photo['like'],
                view=photo['view']
            ))
        except UnicodeEncodeError:
            logger.info('      photo {pid}, comment{comment}/share{share}/like{like}/view{view}'.format(
                pid=pid,
                comment=photo['comment'],
                share=photo['share'],
                like=photo['like'],
                view=photo['view']
            ))

    return photo_count


def get_album_list_page(uid=crawler.uid, after=None):
    albums = crawler.get_json(config.ALBUM_LIST_URL, json_=get_common_payload(uid, after), method='POST')
    if 'count' not in albums:
        return 0, None
    for a in albums['data']:
        aid = int(a['id'])
        try:
            logger.info('    album {aid}: {name}, has {count} photos'.format(
                aid=aid,
                name=a['name'],
                count=a['size']
            ))
        except UnicodeEncodeError:
            logger.info('    album {aid}, has {count} photos'.format(
                aid=aid,
                count=a['size']
            ))

        if a["size"]:
            get_album_summary(aid, uid)
    return albums['count'], albums['tail_id']


def get_albums(uid=crawler.uid):
    cur_page = 0
    total_albums = 0
    after = None
    while True:
        logger.info('start crawl album list page {cur_page}'.format(cur_page=cur_page))
        count, after = get_album_list_page(uid, after)
        if count == 0:
            break
        total_albums += count
        cur_page += 1

    return total_albums
