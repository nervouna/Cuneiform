# coding: utf-8

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import abort

from markdown import markdown

# Required for LeanEngine
from leancloud import Engine
from leancloud import LeanEngineError

from leancloud import LeanCloudError

from models import User
from models import Attachment

from utils import get_posts
from utils import get_single_post
from utils import create_new_post
from utils import parse_tag_names
from utils import get_tag_by_name
from utils import set_tag_by_name
from utils import map_tags_to_post
from utils import get_tags_by_post
from utils import allowed_file


app = Flask(__name__)

# Required for LeanEngine
engine = Engine(app)


@app.route('/')
def index(post_per_page=10):
    current_page = 1
    if 'page' in request.args.keys():
        current_page = int(request.args.get('page'))
    try:
        posts, more = get_posts(post_per_page, current_page)
    except LeanCloudError as e:
        if e.code == 101:
            posts, more = None, False
        else:
            raise e
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
    tag_names = parse_tag_names(request.form['tags'])
    f = request.files['featuredImage']
    if f.filename == '':
        featuredImage = None
    else:
        featuredImage = Attachment(f.filename, data=f.stream)
    if featuredImage and not allowed_file(featuredImage.extension):
        flash('warning', 'Upload a proper image.')
        return redirect(url_for('post_form'))
    post = create_new_post(title, content, author, featuredImage)
    tags = [set_tag_by_name(x) for x in tag_names]
    map_tags_to_post(tags, post)
    return redirect(url_for('show_post', post_id=post.id))


@app.route('/post/<post_id>')
def show_post(post_id):
    post = get_single_post(post_id)
    if not post:
        abort(404)
    post.author.fetch()
    tags = get_tags_by_post(post)
    return render_template('single-post.html', post=post, tags=tags)


@app.route('/tag/<tag_name>')
def tag_index(tag_name, post_per_page=10):
    current_page = 1
    if 'page' in request.args.keys():
        current_page = int(request.args.get('page'))
    try:
        tag = get_tag_by_name(tag_name)
        posts, more = get_posts(post_per_page, current_page, tag)
    except LeanCloudError as e:
        if e.code == 101:
            tag, posts, more = None, None, False
        else:
            raise e
    return render_template('index.html', tag=tag, posts=posts, more=more, page=current_page)


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
    current_user = User.get_current()
    # Won't actually log out due to a bug of the LeanCloud Python SDK.
    # https://github.com/leancloud/python-sdk/issues/280
    current_user.logout()
    flash('info', 'Logged out.')
    return redirect(url_for('index'))
