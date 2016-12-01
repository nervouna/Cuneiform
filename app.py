# coding: utf-8

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

# Required for LeanEngine
from leancloud import Engine
from leancloud import LeanEngineError

from models import Post
from models import User
from models import get_post_list
from models import has_more_posts
from models import create_new_post
from models import get_single_post


app = Flask(__name__)

# Required for LeanEngine
engine = Engine(app)

@app.route('/')
def index(post_per_page=10):
    try:
        current_page = int(request.args['page'])
    except KeyError:
        current_page = 1
    posts, post_count = get_post_list(post_per_page, current_page)
    more = has_more_posts(current_page, post_count, post_per_page)
    return render_template('index.html', posts=posts, more=more, page=current_page)

@app.route('/new_post')
def new_post_editor():
    current_user = User.get_current()
    if not current_user:
        flash('info', 'You have to login to see the good stuff.')
        return redirect(url_for('login'))
    return render_template('editor.html')

@app.route('/new_post', methods=['POST'])
def new_post():
    post_title, post_content = request.form['title'], request.form['content']
    post_id = create_new_post(title=post_title, content=post_content)
    return redirect(url_for('single_post', post_id=post_id))

@app.route('/post/<post_id>')
def single_post(post_id):
    post = get_single_post(post_id)
    return render_template('single-post.html', post=post)

@app.route('/user/login')
def login_form():
    return render_template('login.html')

@app.route('/user/login', methods=['POST'])
def login():
    username, password = request.form['username'], request.form['password']
    user = User()
    user.login(username, password)
    return redirect(url_for('index'))

@app.route('/user/logout')
def logout():
    user = User()
    user.logout()
    return redirect(url_for('index'))
