from leancloud import Object
from leancloud import File
from leancloud import LeanCloudError

from datetime import datetime


class Post(Object):

    @property
    def title(self):
        return self.get('title')

    @title.setter
    def title(self, title):
        if title == '' or title is None:
            title = datetime.now().strftime('Post On %Y-%m-%d %H:%M')
        return self.set('title', title)

    @property
    def content(self):
        return self.get('content')

    @content.setter
    def content(self, content):
        return self.set('content', content)

    @property
    def markedContent(self):
        return self.get('markedContent')

    @markedContent.setter
    def markedContent(self, markedContent):
        return self.set('markedContent', markedContent)

    @property
    def featuredImage(self):
        return self.get('featuredImage')

    @featuredImage.setter
    def featuredImage(self, featuredImage):
        assert isinstance(featuredImage, Attachment)
        return self.set('featuredImage', featuredImage)

    @property
    def author(self):
        return self.get('author')

    @author.setter
    def author(self, author):
        assert isinstance(author, User)
        return self.set('author', author)


class Tag(Object):
    @property
    def name(self):
        return self.get('name')

    @name.setter
    def name(self, name):
        return self.set('name', name)

    @property
    def post_count(self):
        return self.post_count

    @post_count.setter
    def post_count(self, count=1):
        assert type(count) is int
        return self.increment('post_count', count)


class TagPostMap(Object):
    @property
    def tag(self):
        return self.get('tag')

    @tag.setter
    def tag(self, tag):
        assert isinstance(tag, Tag)
        return self.set('tag', tag)

    @property
    def post(self):
        return self.get('post')

    @post.setter
    def post(self, post):
        assert isinstance(post, Post)
        return self.set('post', post)


class User(Object):
    pass


class Attachment(File):
    pass
