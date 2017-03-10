import re

from leancloud import LeanCloudError

from cuneiform.models import Tag
from cuneiform.models import TagPostMap


def split_tag_names(tag_name_string):
    splitters = ','
    tag_names = set([x.strip() for x in re.split(splitters, tag_name_string)])
    try:
        tag_names.remove('')
    except KeyError:
        pass
    return tag_names


def get_tag_by_name(tag_name, auto_create=True):
    try:
        tag = Tag.query.equal_to('name', tag_name).first()
    except LeanCloudError as e:
        if e.code == 101:
            if auto_create == True:
                tag = Tag()
                tag.set('name', tag_name)
                tag.save()
            else:
                tag = None
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


def remove_all_tags_from_post(post):
    tag_post_maps = TagPostMap.query.equal_to('post', post).equal_to('trashed', False).find()
    for tag_post_map in tag_post_maps:
        tag_post_map.set('trashed', True)
        tag_post_map.save()
