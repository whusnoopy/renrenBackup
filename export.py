# coding: utf8

import logging
import logging.config
import os
import re
import shutil
import tarfile

from config import config


logging.config.dictConfig(config.LOGGING_CONF)
logger = logging.getLogger(__name__)


abs_pattern = r'(src|href)="(\s*)/(.*?)(\s*)"'
abs_replace = r'\1="{rel_path}/\3"'
html_pattern = r'<a(.*?)href="({rel_path}.*?)"'
html_replace = r'<a\1href="\2.html"'


def get_json(client, url_path):
    resp = client.get(url_path, headers=[('X-Requested-With', 'XMLHttpRequest')])
    if resp.is_json:
        return resp.json

    return dict(success=0)


def trans_relative_path(content, rel_path):
    content = re.sub(abs_pattern, abs_replace.format(rel_path=rel_path), content,
                     flags=re.M | re.DOTALL)
    content = re.sub(html_pattern.format(rel_path=rel_path), html_replace, content,
                     flags=re.M | re.DOTALL)
    return content


def save_file(client, url_path):
    logger.debug('try to save {url}'.format(url=url_path))
    local_path = re.sub(r'(/\w*)', r'../', url_path)[:-4]
    if not local_path:
        local_path = '.'

    filename = '.{url_path}.html'.format(url_path=url_path)
    filepath = os.path.dirname(filename)

    resp = client.get(url_path)
    output_html = trans_relative_path(resp.data.decode("utf8"), local_path)

    if not os.path.exists(filepath):
        os.makedirs(filepath)

    with open(filename, 'wb') as fp:
        fp.write(output_html.encode('utf8'))

    return filename


def export_by_pattern(client, url_pattern, **kwargs):
    all_json = get_json(client, url_pattern.format(page=1, **kwargs))

    for page in range(all_json['total_page']):
        logger.info('    export {url}'.format(url=url_pattern.format(page=page, **kwargs)))
        save_file(client, url_pattern.format(page=page+1, **kwargs))

    return all_json['total_page']


def export_status(client, uid):
    status_pages = export_by_pattern(client, '/{uid}/status/page/{page}', uid=uid)

    logger.info('  export {} pages of status for user {uid}'.format(status_pages, uid=uid))
    return status_pages


def export_gossip(client, uid):
    gossip_pages = export_by_pattern(client, '/{uid}/gossip/page/{page}', uid=uid)

    logger.info('  export {} pages of gossip for user {uid}'.format(gossip_pages, uid=uid))
    return gossip_pages


def export_albums(client, uid):
    album_list_pattern = '/{uid}/album/page/{page}'
    album_list_pages = export_by_pattern(client, album_list_pattern, uid=uid)

    album_page_pattern = '/album/{album_id}/page/{page}'

    photo_cnt = 0
    album_cnt = 0
    for page in range(album_list_pages):
        album_list_json = get_json(client, album_list_pattern.format(uid=uid, page=page+1))
        album_cnt += len(album_list_json['album_list'])
        for album in album_list_json['album_list']:
            logger.info('  export album {album_id}'.format(album_id=album['id']))
            album_pages = export_by_pattern(client, album_page_pattern, album_id=album['id'])
            for album_page in range(album_pages):
                url = album_page_pattern.format(album_id=album['id'], page=album_page+1)
                album_json = get_json(client, url)
                photo_cnt += len(album_json['photos'])
                for photo in album_json['photos']:
                    save_file(client, '/photo/{photo_id}'.format(photo_id=photo['id']))

    logger.info("  export {} photos in {} albums for user {uid}".format(photo_cnt, album_cnt, uid=uid))
    return album_list_pages


def export_blogs(client, uid):
    blog_list_pattern = '/{uid}/blog/page/{page}'
    blog_pages = export_by_pattern(client, blog_list_pattern, uid=uid)

    cnt = 0
    for page in range(blog_pages):
        page_json = get_json(client, blog_list_pattern.format(uid=uid, page=page+1))
        cnt += len(page_json['blog_list'])
        for blog in page_json['blog_list']:
            save_file(client, '/blog/{blog_id}'.format(blog_id=blog['id']))

    logger.info("  export {} blogs in {} pages for user {uid}".format(cnt, blog_pages, uid=uid))
    return blog_pages


def add_to_tar(tar, directory):
    for root, _dirs, files in os.walk(directory):
        for filename in files:
            fullpath = os.path.join(root, filename)
            tar.add(fullpath)
    logger.info('add {} to backup tar'.format(directory))


def export_all(tar_name, client_app):
    tar = tarfile.open(tar_name, "w")

    save_file(client_app, '/index')
    index_json = get_json(client_app, '/index')
    tar.add("index.html")

    for user in index_json['users']:
        logger.info('start to export user {uid}'.format(uid=user['uid']))
        export_status(client_app, user['uid'])
        export_gossip(client_app, user['uid'])
        export_albums(client_app, user['uid'])
        export_blogs(client_app, user['uid'])
        add_to_tar(tar, '{uid}'.format(uid=user['uid']))

    add_to_tar(tar, 'album')
    add_to_tar(tar, 'photo')
    add_to_tar(tar, 'blog')

    add_to_tar(tar, 'static')
    tar.close()

    os.remove('index.html')
    for user in index_json['users']:
        shutil.rmtree(str(user['uid']))
    shutil.rmtree('album', ignore_errors=True)
    shutil.rmtree('photo', ignore_errors=True)
    shutil.rmtree('blog', ignore_errors=True)
