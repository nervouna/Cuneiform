import re
from functools import wraps
from flask import abort
from markdown import markdown as m
from leancloud import LeanCloudError

from models import Author, Tag, TagPostMap


def protected(func):
    @wraps(func)
    def secret_view(*args, **kwargs):
        current_user = Author.get_current()
        if not current_user:
            abort(401)
        elif not current_user.is_authenticated():
            abort(403)
        else:
            return func(*args, **kwargs)
    return secret_view


def allowed_file(filename):
    ext = filename.rsplit('.', 1)[-1]
    allowed_ext = ['jpg', 'jpeg', 'png', 'svg', 'gif', 'bmp']
    return ext.lower() in allowed_ext


def markdown(text):
    return m(text, extensions=['fenced_code'])


def split_tag_names(tag_name_string):
    splitters = ','
    tag_names = set([x.strip() for x in re.split(splitters, tag_name_string)])
    try:
        tag_names.remove('')
    except KeyError:
        pass
    return tag_names


def get_tag_names_from_map_list(tag_post_maps):
    tag_names = [x.get('tag').get('name') for x in tag_post_maps]
    return tag_names


def get_tag_by_name(tag_name):
    try:
        tag = Tag.query.equal_to('name', tag_name).first()
    except LeanCloudError as e:
        if e.code == 101:
            tag = None
        else:
            raise e
    return tag


def set_tag_by_name(tag_name):
    tag = Tag()
    tag.set('name', tag_name)
    tag.save()
    return tag


def map_tags_to_post(tags, post):
    for tag in tags:
        tag_post_map = TagPostMap()
        tag_post_map.set({'tag': tag, 'post': post})
        tag_post_map.save()
