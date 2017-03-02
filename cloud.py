from leancloud import Engine
from markdown import markdown

from app import app


engine = Engine(app)


@engine.after_save('Post')
def after_post_save(post):
    content = post.get('content')
    post.set('marked_content', markdown(content))
    post.save()


