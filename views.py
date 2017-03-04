from flask import render_template, request, url_for, redirect, g, abort
from leancloud import LeanCloudError

from app import app
from helpers import allowed_file, protected, markdown
from models import Post, Author, Attachment


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
    current_page = request.args.get('page')
    current_page = 1 if not current_page else int(current_page)
    has_prev = has_next = False
    skip = (current_page - 1) * 10
    posts = Post.query.add_descending('createdAt').equal_to('trashed', False).skip(skip).limit(11).find()
    if current_page > 1:
        has_prev = True
    if len(posts) == 11:
        has_next = True
    if len(posts) == 0:
        posts = None
    return render_template("post_list.html", posts=posts, has_prev=has_prev, has_next=has_next, current_page=current_page)


@app.route("/posts/<string:post_id>")
def show_post(post_id):
    try:
        post = Post.query.get(post_id)
    except LeanCloudError as e:
        if e.code == 101:
            abort(404)
        else:
            raise e
    return render_template("post.html", post=post)


@app.route("/login")
def login_form():
    return render_template("user_login.html")


@app.route("/login", methods=["POST"])
def login():
    credentials = ['username', 'password']
    user_data = {x:request.form[x] for x in credentials}
    author = Author()
    try:
        author.login(**user_data)
    except LeanCloudError as e:
        abort(400)
    return redirect(url_for('post_list'))


@app.route("/logout")
@protected
def logout():
    current_user = Author.get_current()
    if current_user:
        current_user.logout()
    return redirect(url_for('post_list'))


@app.route("/posts/new")
@protected
def create_post_form():
    return render_template("create_post_form.html")


@app.route("/posts/new", methods=["POST"])
@protected
def create_post():

    post_data = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'marked_content': markdown(request.form.get('content'))
    }
    post = Post()
    post.set(post_data)

    upload_image = request.files['featured_image']
    if upload_image.filename != '' and allowed_file(upload_image.filename):
        f = Attachment(upload_image.filename, data=upload_image.stream)
        post.set('featured_image', f)

    post.save()

    return redirect(url_for('show_post', post_id=post.id))


@app.route("/posts/<string:post_id>/edit")
@protected
def update_post_form(post_id):
    post=Post.create_without_data(post_id)
    post.fetch()
    return render_template("update_post_form.html", post=post)


@app.route("/posts/<string:post_id>/edit", methods=["POST"])
@protected
def update_post(post_id):

    post_data = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'marked_content': markdown(request.form.get('content'))
    }
    post=Post.create_without_data(post_id)
    post.set(post_data)

    upload_image = request.files['featured_image']

    if upload_image.filename != '' and allowed_file(upload_image.filename):
        f = Attachment(upload_image.filename, data=upload_image.stream)
        post.set('featured_image', f)

    post.save()

    return redirect(url_for('show_post', post_id=post.id))


@app.route("/posts/<string:post_id>/delete")
@protected
def delete_post(post_id):
    post = Post.create_without_data(post_id)
    post.set('trashed', True)
    post.save()
    return redirect(url_for('post_list'))
