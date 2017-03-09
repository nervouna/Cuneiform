from datetime import datetime
from datetime import timedelta
from datetime import timezone

from leancloud import Engine

from models import Post
from app import app


engine = Engine(app)


@engine.after_update('Post')
def after_post_update(post):
    post.set('is_updated', True)
    post.save()
    print('帖子已更新:', post.get('title'))