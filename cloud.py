from leancloud import Engine
from markdown import markdown
from datetime import datetime, timedelta, timezone

from models import Post
from app import app


engine = Engine(app)


@engine.after_save('Post')
def after_post_save(post):
    content = post.get('content')
    post.set('marked_content', markdown(content))
    post.save()


@engine.define
def delete_trashed_posts():
    today = datetime.now(timezone(timedelta(hours=8)))
    recycle_time = timedelta(30)
    trashed_posts = Post.query.equal_to('trashed', True).find()
    for post in trashed_posts:
        if post.get('updatedAt') < today - recycle_time:
            post.destroy()


