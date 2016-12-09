# coding: utf-8

from leancloud import Query
from leancloud import LeanCloudError

from markdown import markdown

from models import Post
from models import User
from models import Attachment
from models import Tag
from models import TagPostMap

import re


def get_post_list(post_per_page=10, current_page=1):
    '''Return the post list.

    Keyword arguments:
    post_per_page -- posts per page (default 10)
    current_page -- page number (default 1)
    '''
    post_query = Query(Post)
    post_query.limit(post_per_page)
    post_query.add_descending('createdAt')
    if current_page > 1:
        post_query.skip((current_page - 1) * post_per_page)
    try:
        post_list = post_query.find()
        post_count = post_query.count()
    except LeanCloudError as e:
        if e.code == 101:
            post_count = 0
            post_list = []
        else:
            raise e
    return post_list, post_count


def has_more_posts(current_page, post_count, post_per_page):
    '''Return True if there are posts to show in the next page.'''
    return post_count > post_per_page * current_page


def get_single_post(post_id):
    '''Return a single post.

    Arguments:
    post_id -- LeanCloud Object ID (default None)
    '''
    post_query = Query(Post)
    single_post = post_query.get(post_id)
    return single_post


def create_new_post(title, content, author, featuredImage):
    '''Create a new post, return ``post_id`` for the created post.

    Arguments:
    title -- title for the new post
    content -- content for the new post, multi-line text
    '''
    new_post = Post()
    new_post.title = title
    new_post.content = content
    new_post.markedContent = markdown(content)
    new_post.author = author
    if featuredImage is not None:
        new_post.featuredImage = featuredImage
    new_post.save()
    return new_post


def parse_tag_names(tag_string):
    tag_string = tag_string.strip()
    if len(tag_string) == 0:
        return None
    else:
        return re.split('[,，;；、]', tag_string)


def get_tag_by_name(tag_name):
    tag_query = Query(Tag)
    tag_name_regex = '^' + tag_name + '$'
    try:
        tag = tag_query.matched('name', tag_name_regex).first()
    except LeanCloudError as e:
        if e.code == 101:
            return None
        else:
            raise e


def set_tag_by_name(tag_name):
    tag = get_tag_by_name(tag_name)
    if tag is not None:
        return tag
    new_tag = Tag()
    new_tag.name = tag_name
    return new_tag


def map_tags_to_post(tags, post):
    for tag in tags:
        tag_post_map = TagPostMap()
        tag_post_map.tag = tag
        tag_post_map.post = post
        tag.increment('post_count')
        tag_post_map.save()


def get_tags_by_post(post):
    map_query = Query(TagPostMap)
    map_query.equal_to('post', post)
    tag_post_maps = map_query.find()
    if len(tag_post_maps) == 0:
        return None
    for tag_post_map in tag_post_maps:
        tag_post_map.tag.fetch()
    return [tag_post_map.tag for tag_post_map in tag_post_maps]


def get_posts_by_tag(tag):
    map_query = Query(TagPostMap)
    map_query.equal_to('tag', tag)
    tag_post_maps = map_query.find()
    if len(tag_post_maps) == 0:
        return None
    for tag_post_map in tag_post_maps:
        tag_post_map.post.fetch()
    return [tag_post_map.post for tag_post_map in tag_post_maps]


def allowed_file(ext):
    allowed_ext = ['jpg', 'jpeg', 'png', 'svg', 'gif', 'bmp']
    return ext.lower() in allowed_ext
