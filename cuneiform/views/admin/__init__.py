from flask import Blueprint
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import g
from flask import abort
from leancloud import LeanCloudError

from cuneiform.models import Post
from cuneiform.models import Author
from cuneiform.models import Attachment
from cuneiform.manager.helper import allowed_file
from cuneiform.manager.helper import protected
from cuneiform.manager.helper import redirect_url
from cuneiform.manager.helper import pinyinify
from cuneiform.manager.post import markdown
from cuneiform.manager.tag import split_tag_names
from cuneiform.manager.tag import get_tag_by_name
from cuneiform.manager.tag import get_tags_by_post
from cuneiform.manager.tag import map_tags_to_post
from cuneiform.manager.tag import remove_all_tags_from_post


admin = Blueprint('admin', __name__, template_folder="templates")

@admin.route("/login")
def login_form():
    return render_template("admin/user_login.html", next=request.referrer)


@admin.route("/login", methods=["POST"])
def login():
    credentials = ['username', 'password']
    user_data = {x:request.form[x] for x in credentials}
    author = Author()
    try:
        author.login(**user_data)
    except LeanCloudError as e:
        abort(400)
    return redirect(redirect_url())


@admin.route("/logout")
@protected
def logout():
    current_user = Author.get_current()
    if current_user:
        current_user.logout()
    return redirect(redirect_url())


@admin.route("/posts/new")
@protected
def create_post_form():
    return render_template("admin/create_post_form.html")


@admin.route("/posts/new", methods=["POST"])
@protected
def create_post():

    post_data = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'slug': pinyinify(request.form.get('title')),
    }
    post = Post()
    post.set(post_data)
    post = markdown(post)

    upload_image = request.files.get('featured_image')
    if upload_image.filename != '' and allowed_file(upload_image.filename):
        f = Attachment(upload_image.filename, data=upload_image.stream)
        post.set('featured_image', f)

    post.save()

    tag_names = request.form.get('tags').lower().strip()
    tags = [get_tag_by_name(x) for x in split_tag_names(tag_names)]
    map_tags_to_post(tags, post)

    return redirect(url_for('show_post', post_id=post.id))


@admin.route("/posts/<string:post_id>/edit")
@protected
def update_post_form(post_id):
    post = Post.create_without_data(post_id)
    tag_names = ','.join([x.get('name') for x in get_tags_by_post(post)])
    post.fetch()
    return render_template("admin/update_post_form.html", post=post, tag_names=tag_names)


@admin.route("/posts/<string:post_id>/edit", methods=["POST"])
@protected
def update_post(post_id):

    post_data = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'slug': pinyinify(request.form.get('title')),
    }
    post = Post.create_without_data(post_id)
    post.set(post_data)
    post = markdown(post)

    upload_image = request.files['featured_image']

    if upload_image.filename != '' and allowed_file(upload_image.filename):
        f = Attachment(upload_image.filename, data=upload_image.stream)
        post.set('featured_image', f)

    old_tag_names = [x.get('name') for x in get_tags_by_post(post)]
    new_tag_names = split_tag_names(request.form.get('tags').lower().strip())
    if len(new_tag_names) != len(old_tag_names):
        if len(old_tag_names) > 0:
            remove_all_tags_from_post(post)
        if len(new_tag_names) > 0:
            map_tags_to_post([get_tag_by_name(x) for x in new_tag_names], post)

    post.save()

    return redirect(url_for('show_post', post_id=post.id))


@admin.route("/posts/<string:post_id>/delete")
@protected
def delete_post(post_id):
    post = Post.create_without_data(post_id)
    post.set('trashed', True)
    post.save()
    return redirect(url_for('post_list'))
