# coding: utf-8

import getpass
import glob
import logging
import logging.config
import os
import shutil
import subprocess
import zipfile

from flask_script import Manager

from config import config

from crawl.crawler import Crawler
from fetch import prepare_db, fetch_user, update_fetch_info
from web import app
from export import export_all


logging.config.dictConfig(config.LOGGING_CONF)
logger = logging.getLogger(__name__)
manager = Manager(app)


@manager.command
def fetch(email='', password='',
          status=False, gossip=False, album=False, blog=False,
          refresh_count=False, uid=0):
    # if not email:
    #     email = input("Input renren account email (aka. username@renren.com): ")
    # if not password:
    #     password = getpass.getpass("Input renren password (will not show): ")

    prepare_db()

    config.crawler = Crawler(email, password, Crawler.load_cookie())

    config.crawler.login()

    uid = uid or config.crawler.uid

    fetched = fetch_user(uid, fetch_status=status, fetch_gossip=gossip, fetch_album=album, fetch_blog=blog)

    if not fetched:
        logger.info('nothing need to fetch, just test login')

    if fetched or refresh_count:
        update_fetch_info(uid)


@manager.command
def export(filename=config.BAK_OUTPUT_TAR):
    client_app = app.test_client()
    export_all(filename, client_app)


@manager.command
def lint():
    subprocess.run(['flake8', '.'])
    subprocess.run(['pylint', 'crawl', 'config.py', 'export.py', 'fetch.py', 'manage.py', 'models.py', 'web.py'])


@manager.command
def release(release_name='renrenBackup'):
    clean()

    logger.info('package manager.py with pyinstaller')
    subprocess.run(['pyinstaller', '-F', 'manage.py', '-n', 'renrenBackup'])

    logger.info('copy templates and static files')
    shutil.copytree('./templates', './dist/templates')
    os.mkdir('./dist/static')
    shutil.copytree('./static/themes', './dist/static/themes')
    for ext in ['js', 'css', 'gif']:
        for f in glob.glob('./static/*.' + ext):
            shutil.copy(f, './dist/static/')

    logger.info('init log directory')
    os.mkdir('./dist/log')

    with zipfile.ZipFile(release_name + '.zip', 'w') as fp:
        os.rename('./dist', release_name)
        for f in glob.glob(release_name + "/**/*", recursive=True):
            fp.write(f)
        os.rename(release_name, './dist')


@manager.command
def clean():
    # temp file
    for f in glob.glob("./**/.pyc", recursive=True):
        logger.info('remove temp file %s', f)
        os.remove(f)
    for f in glob.glob("./**/.pyo", recursive=True):
        logger.info('remove temp file %s', f)
        os.remove(f)
    for f in glob.glob("./**/*~", recursive=True):
        logger.info('remove temp file %s', f)
        shutil.rmtree(f)
    for f in glob.glob("./**/__pycache__", recursive=True):
        logger.info('remove temp file %s', f)
        shutil.rmtree(f)

    # release
    logger.info('remove release build')
    shutil.rmtree('build', ignore_errors=True)

    logger.info('remove release dist')
    shutil.rmtree('dist', ignore_errors=True)

    for f in glob.glob("./**/*.spec", recursive=True):
        logger.info('remove release spec file %s', f)
        os.remove(f)


if __name__ == "__main__":
    manager.run()
