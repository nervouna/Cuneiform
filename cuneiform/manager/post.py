from flask import Markup
from markdown import markdown as m


def markdown(text):
    return m(text, extensions=['fenced_code'])


def markup(post):
    post.set('marked_content', Markup(post.get('marked_content')))
    return post