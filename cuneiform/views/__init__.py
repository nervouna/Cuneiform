from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import g
from flask import abort
from leancloud import LeanCloudError

from cuneiform import app
from cuneiform.models import Author
from cuneiform.models import Post
from cuneiform.models import TagPostMap
from cuneiform.manager.helper import paginate
from cuneiform.manager.post import markup
from cuneiform.manager.tag import get_tag_by_name
from cuneiform.manager.tag import get_tags_by_post
from cuneiform.views.admin import admin


app.register_blueprint(admin)

@app.before_request
def before_request():
    g.user = Author.get_current()


@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
def error_page(e):
    return render_template("error.html", error=e), e.code


@app.route("/")
@app.route("/posts/")
def post_list():
    _page = request.args.get('page')
    current_page = 1 if not _page else int(_page)
    query = Post.query.equal_to('trashed', False)
    paginate(query, current_page, limit=10)
    posts = query.find()
    has_prev = has_next = False
    if current_page > 1:
        has_prev = True
    if len(posts) == 11:
        has_next = True
        posts = posts[:-1]
    return render_template("post_list.html", posts=posts, has_prev=has_prev, has_next=has_next, current_page=current_page)


@app.route("/tags/<string:tag_name>")
def post_list_with_tag(tag_name):
    tag = get_tag_by_name(tag_name, auto_create=False)
    if not tag:
        abort(404)
    _page = request.args.get('page')
    current_page = 1 if not _page else int(_page)
    query = TagPostMap.query.equal_to('trashed', False).equal_to('tag', tag).include('post')
    paginate(query, current_page, limit=10)
    posts = [x.get('post') for x in query.find()]
    has_prev = has_next = False
    if current_page > 1:
        has_prev = True
    if len(posts) == 11:
        has_next = True
        posts = posts[:-1]
    return render_template("post_list.html", posts=posts, has_prev=has_prev, has_next=has_next, current_page=current_page, tag=tag)



@app.route("/posts/<string:post_id>")
def show_post(post_id):
    try:
        post = Post.query.get(post_id)
        tags = get_tags_by_post(post)
    except LeanCloudError as e:
        if e.code == 101:
            abort(404)
        else:
            raise e
    post = markup(post)
    return render_template("post.html", post=post, tags=tags)
