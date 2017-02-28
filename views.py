from flask import render_template
from app import app
from helpers import protected
from models import Post


@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
def error_page(e):
	return render_template("errors/%i.html" % e.code), 400


@app.route("/")
def front_page():
	return render_template("index.html")


@app.route("/posts/")
def post_list():
	return render_template("post_list.html")


@app.route("/posts/<string:post_id>")
def post(post_id):
	post = Post.query.get(post_id)
	return render_template("post.html", post=post)


@app.route("/login")
def login_form():
	return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
	pass


@app.route("/logout")
def logout():
	pass


@app.route("/posts/new")
@protected
def post_editor():
	return render_template("post_editor.html")


@app.route("/posts/new", methods=["POST"])
@protected
def create_post():
	return render_template("post_editor.html")


@app.route("/posts/<string:post_id>", methods=["POST"])
@protected
def update_post(post_id):
	return render_template("post_editor.html")


@app.route("/posts/<string:post_id>/delete")
@protected
def delete_post(post_id):
	return render_template("post.html")
