import re
from functools import wraps

from flask import abort
from markdown import markdown as m
from leancloud import LeanCloudError

from models import Author
from models import Tag
from models import TagPostMap


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


def get_tag_by_name(tag_name):
    try:
        tag = Tag.query.equal_to('name', tag_name).first()
    except LeanCloudError as e:
        if e.code == 101:
            tag = Tag()
            tag.set('name', tag_name)
            tag.save()
        else:
            raise e
    return tag


def get_tags_by_post(post):
    tag_post_maps = TagPostMap.query.equal_to('post', post).equal_to('trashed', False).include('tag').find()
    if tag_post_maps != []:
        tags = [x.get('tag') for x in tag_post_maps]
    else:
        tags = []
    return tags


def map_tags_to_post(tags, post):
    for tag in tags:
        tag_post_map = TagPostMap()
        tag_post_map.set({'tag': tag, 'post': post, 'trashed': False})
        tag_post_map.save()


def remove_tag_from_post(tag, post):
    tag_post_maps = TagPostMap.query.equal_to('tag', tag).equal_to('post', post).equal_to('trashed', False).find()
    for tag_post_map in tag_post_maps:
        tag_post_map.set('trashed', True)
        tag_post_map.save()
