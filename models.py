from leancloud import Object
from leancloud import File
from leancloud import Query
from leancloud import LeanCloudError

class Post(Object):
    pass

class Attachment(File):
    pass

class User(Object):
    pass

def get_post_list(limit=10, page=1):
    '''Return the post list.

    Keyword arguments:
    limit -- posts per page (default 10)
    page -- page number (default 1)
    '''
    post_query = Query(Post)
    post_query.limit(limit)
    if page > 1: post_query.skip((page - 1) * limit)
    post_query.add_descending('createdAt')
    post_list = post_query.find()
    return post_list

def get_single_post(post_id):
    '''Return a single post.

    Argument:
    post_id -- LeanCloud Object ID (default None)
    '''
    post_query = Query(Post)
    single_post = post_query.get(post_id)
    return single_post

def create_new_post(title, content):
    '''Create a new post, return ``post_id`` for the created post.

    Argument:
    title -- title for the new post
    content -- content for the new post, multi-line text
    '''
    new_post = Post()
    new_post.set('title', title)
    new_post.set('content', content)
    new_post.save()
    post_id = new_post.id
    return post_id
