# coding: utf-8

from flask import Flask

# Required for LeanEngine
from leancloud import Engine
from leancloud import LeanEngineError


app = Flask(__name__)

# Required for LeanEngine
engine = Engine(app)

@app.route('/')
def index():
    return "There you have it, INDEX!"
