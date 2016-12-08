# coding: utf-8

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from markdown import markdown

# Required for LeanEngine
from leancloud import Engine
from leancloud import LeanEngineError

from models import User
from models import Attachment
from utils import *


app = Flask(__name__)

# Required for LeanEngine
engine = Engine(app)


@app.route('/')
def index(post_per_page=10):
    if 'page' in request.args.keys():
        current_page = int(request.args['page'])
    else:
        current_page = 1
    posts, post_count = get_post_list(post_per_page, current_page)
    more = has_more_posts(current_page, post_count, post_per_page)
    return render_template('index.html', posts=posts, more=more, page=current_page)


@app.route('/new_post')
def post_form():
    current_user = User.get_current()
    if not current_user:
        flash('info', 'You have to login to see the good stuff.')
        return redirect(url_for('login'))
    current_user.fetch()
    return render_template('editor.html', current_user=current_user)


@app.route('/new_post', methods=['POST'])
def new_post():
    author = User.get_current()
    title, content = request.form['title'], request.form['content']
    f = request.files['featuredImage']
    if f.filename == '':
        featuredImage = None
    else:
        featuredImage = Attachment(f.filename, data=f.stream)
    if featuredImage and not allowed_file(featuredImage.extension):
        flash('warning', 'Upload a proper image.')
        return redirect(url_for('post_form'))
    new_post = create_new_post(title, content, author, featuredImage)
    return redirect(url_for('show_post', post_id=new_post.id))


@app.route('/post/<post_id>')
def show_post(post_id):
    post = get_single_post(post_id)
    post.author.fetch()
    return render_template('single-post.html', post=post)


@app.route('/user/login')
def login_form():
    return render_template('login.html')


@app.route('/user/login', methods=['POST'])
def login():
    username, password = request.form['username'], request.form['password']
    user = User()
    user.login(username, password)
    if 'next' in request.args.keys():
        return redirect(request.args.get('next'))
    else:
        return redirect('index')


@app.route('/user/logout')
def logout():
    user = User.get_current()
    user.logout()
    return redirect(url_for('index'))
