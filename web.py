# coding: utf8

import math

from flask import Flask 
from flask import abort, jsonify, render_template, redirect, request, url_for
from playhouse.shortcuts import model_to_dict

from models import User, Comment, Like, Status, Blog, Album, Photo, Gossip

from config import config


app = Flask(__name__)


@app.route("/")
def index_page():
    return render_template("index.html")


@app.route('/comments/<int:entry_id>')
def entry_comments_api(entry_id=0):
    comments = list(Comment.select().where(Comment.entry_id==entry_id).order_by(Comment.t).dicts())
    likes = list(Like.select().where(Like.entry_id==entry_id).dicts())

    uids = list(set([c['authorId'] for c in comments] + [l['uid'] for l in likes]))
    users = dict([(u['uid'], {'name': u['name'], 'headPic': u['headPic']}) for u in User.select().where(User.uid.in_(uids)).dicts()])

    for like in likes:
        like['name'] = users.get(like['uid'], {}).get('name', '')
        like['headPic'] = users.get(like['uid'], {}).get('headPic', '')

    for comment in comments:
        comment['headPic'] = users.get(comment['authorId'], {}).get('headPic', '')

    ret = dict(comments=comments, likes=likes, users=users)
    if request.path.split('/')[1] == 'comments':
        return jsonify(ret)
    return ret


@app.route('/status/page/<int:page>')
def status_list_page(page=0):
    if page <= 0:
        abort(404)
    total = Status.select().count()
    total_page = int(math.ceil(total*1.0 / config.ITEMS_PER_PAGE))
    status_list = Status.select().order_by(Status.t.desc()).paginate(page, config.ITEMS_PER_PAGE)
    return render_template("status_list.html", page=page, total_page=total_page, status_list=status_list)


@app.route('/blog/page/<int:page>')
def blog_list_page(page=0):
    if page <= 0:
        abort(404)
    
    total = Blog.select().count()
    total_page = int(math.ceil(total*1.0 / config.ITEMS_PER_PAGE))
    blog_list = Blog.select().order_by(Blog.id.desc()).paginate(page, config.ITEMS_PER_PAGE)
    return render_template("blog_list.html", page=page, total_page=total_page, blog_list=blog_list)


@app.route('/blog/<int:blog_id>')
def blog_detail_page(blog_id=0):
    blog = model_to_dict(Blog.get(Blog.id==blog_id))
    if not blog:
        abort(404)

    extra = entry_comments_api(entry_id=blog_id)

    return render_template("blog.html", blog=blog, **extra)


@app.route('/album/page/<int:page>')
def album_list_page(page=0):
    if page <= 0:
        abort(404)
    total = Album.select().count()
    total_page = int(math.ceil(total*1.0 / config.ITEMS_PER_PAGE))
    album_list = Album.select().order_by(Album.id.desc()).paginate(page, config.ITEMS_PER_PAGE)
    return render_template("album_list.html", page=page, total_page=total_page, album_list=album_list)


@app.route('/album/<int:album_id>')
def album_detail_entry(album_id=0):
    return redirect(url_for('album_detail_page', album_id=album_id, page=1))


@app.route('/album/<int:album_id>/page/<int:page>')
def album_detail_page(album_id=0, page=0):
    if page <= 0:
        abort(404)

    album = model_to_dict(Album.get(Album.id==album_id))
    if not album:
        abort(404)
    total_page = int(math.ceil(album['count']*1.0 / config.ITEMS_PER_PAGE))

    extra = entry_comments_api(entry_id=album_id)

    photos = list(Photo.select().where(Photo.album_id==album_id).order_by(Photo.pos).paginate(page, config.ITEMS_PER_PAGE).dicts())
    return render_template("album.html", album=album, page=page, total_page=total_page, photos=photos, **extra)


@app.route('/photo/<int:photo_id>')
def photo_detail_page(photo_id=0):
    photo = model_to_dict(Photo.get(Photo.id==photo_id))
    if not photo:
        abort(404)

    extra = entry_comments_api(entry_id=photo_id)

    return render_template("photo.html", photo=photo, **extra)


@app.route('/gossip/page/<int:page>')
def gossip_list_page(page=0):
    if page <= 0:
        abort(404)
    total = Gossip.select().count()
    total_page = int(math.ceil(total*1.0 / config.ITEMS_PER_PAGE))
    gossip_list = Gossip.select().order_by(Gossip.t.desc(), Gossip.id.desc()).paginate(page, config.ITEMS_PER_PAGE)
    return render_template("gossip_list.html", page=page, total_page=total_page, gossip_list=gossip_list)


@app.route('/gossip/<int:gossip_id>')
def gossip_detail_page(gossip_id=0):
    return render_template("gossip_detail.html")


if __name__ == '__main__':
    app.run(debug=True)
