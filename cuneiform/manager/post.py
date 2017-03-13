from flask import Markup
from markdown import markdown as m


def markdown(post):
    post.set('marked_content', m(post.get('content'), extensions=['fenced_code']))
    return post


def markup(post):
    post.set('marked_content', Markup(post.get('marked_content')))
    return post