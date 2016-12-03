# coding: utf-8

from leancloud import Query
from leancloud import LeanCloudError

from markdown import markdown

from models import Post
from models import User
from models import Attachment


def get_post_list(post_per_page=10, current_page=1):
    '''Return the post list.

    Keyword arguments:
    post_per_page -- posts per page (default 10)
    current_page -- page number (default 1)
    '''
    post_query = Query(Post)
    post_query.limit(post_per_page)
    post_query.add_descending('createdAt')
    if current_page > 1: post_query.skip((current_page - 1) * post_per_page)
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

def create_new_post(title, content):
    '''Create a new post, return ``post_id`` for the created post.

    Arguments:
    title -- title for the new post
    content -- content for the new post, multi-line text
    '''
    new_post = Post()
    new_post.title = title
    new_post.content = content
    new_post.markedContent = markdown(content)
    new_post.save()
    return new_post
