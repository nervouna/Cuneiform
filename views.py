from flask import render_template, request, url_for, redirect
from app import app
from helpers import validate_form_data, allowed_file
from models import Post, Author


@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
def error_page(e):
	return render_template("errors/%i.html" % e.code), e.code


@app.route("/")
def front_page():
	return render_template("index.html")


@app.route("/posts/")
def post_list():
	posts = Post.query.add_ascending('createdAt').equal_to('trashed', False).limit(10).find()
	return render_template("post_list.html", posts=posts)


@app.route("/posts/<string:post_id>")
def post(post_id):
	post = Post.query.get(post_id)
	return render_template("post.html", post=post)


@app.route("/login")
def login_form():
	return render_template("user_login.html")


@app.route("/login", methods=["POST"])
def login():
	credentials = ['username', 'password']
	user_data = {x:request.form[x] for x in credentials}
	author = Author()
	author.login(**user_data)
	return redirect(url_for('post_list'))


@app.route("/logout")
def logout():
	current_user = Author.get_current()
	if current_user:
		current_user.logout()
	return redirect(url_for('post_list'))


@app.route("/posts/new")
def post_editor():
	return render_template("post_editor.html")


@app.route("/posts/new", methods=["POST"])
def create_post():
	required_fields = ['title', 'content']
	post_data = {x:request.form[x] for x in required_fields}
	post = Post()
	post.set(post_data)
	post.save()
	return redirect(url_for('post', post_id=post.id))


@app.route("/posts/<string:post_id>", methods=["POST"])
def update_post(post_id):
	return render_template("post_editor.html")


@app.route("/posts/<string:post_id>/delete")
def delete_post(post_id):
	post = Post.create_without_data(post_id)
	post.set('trashed', True)
	post.save()
	return redirect(url_for('post_list'))
