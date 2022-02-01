# coding: utf8

import math
import os
import sys

from flask import Flask
from flask import abort, g, jsonify, redirect, request, session, url_for
from flask import render_template as flask_render
from playhouse.shortcuts import model_to_dict

from models import FetchedUser, User, Comment, Like, Status, Blog, Album, Photo, Gossip

from config import config


if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    template_folder = os.path.join(application_path, 'templates')
    static_folder = os.path.join(application_path, 'static')
    app = Flask('__main__', template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask('__main__')
app.secret_key = '5e3d7125660f4793bfe15a87f59e23c1'


def render_template(template_name, **kwargs):
    if request.accept_mimetypes.best == 'application/json':
        return jsonify(success=1, **kwargs)

    return flask_render(template_name, **kwargs)


@app.before_request
def handle_session():
    uid = 0
    paths = request.path.split('/')
    if len(paths) > 1 and paths[1].isdigit():
        uid = int(paths[1])

    if 'user' in session and ((not uid) or (uid and session['user']['uid'] == uid)):
        g.user = session['user']
    elif uid:
        user = FetchedUser.get_or_none(FetchedUser.uid == uid)
        if not user:
            abort(404, "no such user")

        session['user'] = model_to_dict(user)
        g.user = session['user']
    else:
        g.user = None


@app.route("/")
@app.route("/index")
def index_page():
    users = list(FetchedUser.select().dicts())
    return render_template("index.html", users=users)


@app.route('/user/<int:uid>')
def switch_user(uid=0):
    return redirect(url_for('status_list_page', uid=uid, page=1))


@app.route('/comments/<int:entry_id>')
def entry_comments_api(entry_id=0):
    comments = list(Comment.select().where(Comment.entry_id == entry_id)
                    .order_by(Comment.t).dicts())
    likes = list(Like.select().where(Like.entry_id == entry_id).dicts())

    uids = list(set([c['authorId'] for c in comments] + [like['uid'] for like in likes]))
    users = {}

    u_start = 0
    u_size = 64
    while u_start < len(uids):
        for u in User.select().where(User.uid.in_(uids[u_start:u_start+u_size])).dicts():
            users[u['uid']] = {'name': u['name'], 'headPic': u['headPic']}
        u_start += u_size

    for like in likes:
        like['name'] = users.get(like['uid'], {}).get('name', '')
        like['headPic'] = users.get(like['uid'], {}).get('headPic', '')

    for comment in comments:
        comment['headPic'] = users.get(comment['authorId'], {}).get('headPic', '')

    ret = dict(comments=comments, likes=likes, users=users)
    if request.path.split('/')[1] == 'comments':
        return jsonify(ret)
    return ret


@app.route('/<int:uid>/status/page/<int:page>')
def status_list_page(uid, page=1):
    if page <= 0:
        abort(404)
    total_page = int(math.ceil(g.user['status']*1.0 / config.ITEMS_PER_PAGE))
    status_list = list(Status.select().where(Status.uid == uid)
                       .order_by(Status.t.desc()).paginate(page, config.ITEMS_PER_PAGE).dicts())

    for status in status_list:
        extra = entry_comments_api(entry_id=status['id'])
        status.update(**extra)

    return render_template("status_list.html", page=page, total_page=total_page,
                           status_list=status_list)


@app.route('/<int:uid>/blog/page/<int:page>')
def blog_list_page(uid, page=1):
    if page <= 0:
        abort(404)

    total_page = int(math.ceil(g.user['blog']*1.0 / config.ITEMS_PER_PAGE))
    blog_list = list(Blog.select().where(Blog.uid == uid)
                     .order_by(Blog.id.desc()).paginate(page, config.ITEMS_PER_PAGE).dicts())
    return render_template("blog_list.html", page=page, total_page=total_page,
                           blog_list=blog_list)


@app.route('/blog/<int:blog_id>')
def blog_detail_page(blog_id=0):
    blog = model_to_dict(Blog.get(Blog.id == blog_id))
    if not blog:
        abort(404)

    extra = entry_comments_api(entry_id=blog_id)

    return render_template("blog.html", blog=blog, **extra)


@app.route('/<int:uid>/album/page/<int:page>')
def album_list_page(uid, page=1):
    if page <= 0:
        abort(404)
    total_page = int(math.ceil(g.user['album']*1.0 / config.ITEMS_PER_PAGE))
    album_list = list(Album.select().where(Album.uid == uid)
                      .order_by(Album.id.desc()).paginate(page, config.ITEMS_PER_PAGE).dicts())
    return render_template("album_list.html", page=page, total_page=total_page,
                           album_list=album_list)


@app.route('/album/<int:album_id>/page/<int:page>')
def album_detail_page(album_id=0, page=0):
    if page <= 0:
        abort(404)

    album = model_to_dict(Album.get(Album.id == album_id))
    if not album:
        abort(404)
    total_page = int(math.ceil(album['count']*1.0 / config.ITEMS_PER_PAGE))

    extra = entry_comments_api(entry_id=album_id)

    photos = list(Photo.select().where(Photo.album_id == album_id)
                  .order_by(Photo.pos).paginate(page, config.ITEMS_PER_PAGE).dicts())
    return render_template("album.html", album=album, page=page, total_page=total_page,
                           photos=photos, **extra)


@app.route('/photo/<int:photo_id>')
def photo_detail_page(photo_id=0):
    photo = model_to_dict(Photo.get(Photo.id == photo_id))
    if not photo:
        abort(404)

    extra = entry_comments_api(entry_id=photo_id)

    return render_template("photo.html", photo=photo, **extra)


@app.route('/<int:uid>/gossip/page/<int:page>')
def gossip_list_page(uid, page=1):
    if page <= 0:
        abort(404)
    total_page = int(math.ceil(g.user['gossip']*1.0 / config.ITEMS_PER_PAGE))
    gossip_list = list(Gossip.select().where(Gossip.uid == uid)
                       .order_by(Gossip.t.desc(), Gossip.id.desc())
                       .paginate(page, config.ITEMS_PER_PAGE).dicts())
    return render_template("gossip_list.html", page=page, total_page=total_page,
                           gossip_list=gossip_list)
