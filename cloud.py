from datetime import datetime
from datetime import timedelta

from leancloud import Engine
from leancloud import HttpsRedirectMiddleware

from cuneiform import app
from cuneiform.models import Post
from cuneiform.models import TagPostMap


engine = Engine(HttpsRedirectMiddleware(app))


@engine.after_update('Post')
def after_post_update(post):
    post.set('is_updated', True)
    post.save()
    print('帖子已更新:', post.get('title'))


@engine.define
def purge_trashed_tag_post_maps():
	start_date = datetime.today() - timedelta(1)
	trashed = TagPostMap.query.greater_than('updatedAt', start_date).equal_to('trashed', True).find()
	if trashed:
		print("正在清理 %i 个已删除的标签关系" % len(trashed))
		for trashed_map in trashed:
			trashed_map.destroy()
		print("清理完毕")
	else:
		print("过去一天没有标签关系被删除")
