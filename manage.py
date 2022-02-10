# coding: utf-8

import getpass
import glob
import logging
import logging.config
import os
import shutil
import subprocess
import zipfile

import click

from config import config

from crawl.crawler import Crawler
from fetch import prepare_db, fetch_user, update_fetch_info
from web import app
from export import export_all


logging.config.dictConfig(config.LOGGING_CONF)
logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@cli.command()
@click.option("-e", "--email", default="")
@click.option("-p", "--password", default="")
@click.option("-s", "--status", default=False, is_flag=True)
@click.option("-g", "--gossip", default=False, is_flag=True)
@click.option("-a", "--album", default=False, is_flag=True)
@click.option("-b", "--blog", default=False, is_flag=True)
@click.option("-r", "--refresh_count", default=False, is_flag=True)
@click.option("-u", "--uid", default=0)
def fetch(
    email, password, status, gossip, album, blog, refresh_count, uid
):  # pylint: disable=R0913
    if not email:
        email = input("Input renren account email (aka. username@renren.com): ")
    if not password:
        password = getpass.getpass("Input renren password (will not show): ")

    prepare_db()

    config.crawler = Crawler(email, password, Crawler.load_cookie())
    uid = uid or config.crawler.uid

    fetched = fetch_user(
        uid,
        fetch_status=status,
        fetch_gossip=gossip,
        fetch_album=album,
        fetch_blog=blog,
    )

    if not fetched:
        logger.info("nothing need to fetch, just test login")

    if fetched or refresh_count:
        update_fetch_info(uid)


@cli.command()
@click.option("-f", "--filename", default=config.BAK_OUTPUT_TAR)
def export(filename):
    client_app = app.test_client()
    export_all(filename, client_app)


@cli.command()
def lint():
    lint_files = [
        "crawl",
        "config.py",
        "export.py",
        "fetch.py",
        "manage.py",
        "models.py",
        "web.py",
    ]
    subprocess.run(["flake8"] + lint_files, check=True)
    subprocess.run(["pylint"] + lint_files, check=True)


def clean_env():
    # temp file
    for f in glob.glob("./**/.pyc", recursive=True):
        logger.info("remove temp file %s", f)
        os.remove(f)
    for f in glob.glob("./**/.pyo", recursive=True):
        logger.info("remove temp file %s", f)
        os.remove(f)
    for f in glob.glob("./**/*~", recursive=True):
        logger.info("remove temp file %s", f)
        shutil.rmtree(f)
    for f in glob.glob("./**/__pycache__", recursive=True):
        logger.info("remove temp file %s", f)
        shutil.rmtree(f)

    # release
    logger.info("remove release build")
    shutil.rmtree("build", ignore_errors=True)

    logger.info("remove release dist")
    shutil.rmtree("dist", ignore_errors=True)

    for f in glob.glob("./**/*.spec", recursive=True):
        logger.info("remove release spec file %s", f)
        os.remove(f)


@cli.command()
@click.option("-n", "--release_name", default="renrenBackup")
def release(release_name):
    clean_env()

    logger.info("package manager.py with pyinstaller")
    subprocess.run(["pyinstaller", "-F", "manage.py", "-n", "renrenBackup"], check=True)

    logger.info("copy templates and static files")
    shutil.copytree("./templates", "./dist/templates")
    os.mkdir("./dist/static")
    shutil.copytree("./static/css", "./dist/static/css")
    shutil.copytree("./static/js", "./dist/static/js")
    shutil.copytree("./static/gif", "./dist/static/gif")

    logger.info("init log directory")
    os.mkdir("./dist/log")

    logger.info("copy README to dist")
    shutil.copy("./README.md", "./dist/")

    with zipfile.ZipFile(release_name + ".zip", "w") as fp:
        os.rename("./dist", release_name)
        for f in glob.glob(release_name + "/**/*", recursive=True):
            fp.write(f)
        os.rename(release_name, "./dist")


@cli.command()
def clean():
    clean_env()


@cli.command()
def runserver():
    app.run()


if __name__ == "__main__":
    cli()
