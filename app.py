# coding: utf-8

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

# Required for LeanEngine
from leancloud import Engine
from leancloud import LeanEngineError

from models import Post


app = Flask(__name__)

# Required for LeanEngine
engine = Engine(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def new_post():
    post_title = request.form['title']
    post_content = request.form['content']
    post = Post()
    post.set('title', post_title)
    post.set('content', post_content)
    post.save()
    return redirect(url_for('index'))
