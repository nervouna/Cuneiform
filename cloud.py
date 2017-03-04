from leancloud import Engine
from datetime import datetime, timedelta, timezone

from models import Post
from app import app


engine = Engine(app)


@engine.define
def delete_trashed_posts():
    print('正在执行定时任务：删除回收站的帖子。')
    today = datetime.now(timezone(timedelta(hours=8)))
    recycle_time = timedelta(30)
    trashed_posts = Post.query.equal_to('trashed', True).find()
    if len(trashed_posts) == 0:
        print('回收站里没有帖子。')
    else:
        print('正在处理 %i 条帖子' % len(trashed_posts))
    for post in trashed_posts:
        if post.get('updatedAt') < today - recycle_time:
            print(post.get('title'))
            post.destroy()
            print('帖子已经被彻底删除。')


