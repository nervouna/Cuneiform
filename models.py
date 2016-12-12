from leancloud import Object
from leancloud import File
from leancloud import Query
from leancloud import LeanCloudError

from datetime import datetime


class Post(Object):

    @property
    def title(self):
        return self.get('title')

    @title.setter
    def title(self, title):
        self.set('title', title)

    @property
    def content(self):
        return self.get('content')

    @content.setter
    def content(self, content):
        self.set('content', content)

    @property
    def markedContent(self):
        return self.get('markedContent')

    @markedContent.setter
    def markedContent(self, markedContent):
        self.set('markedContent', markedContent)

    @property
    def featuredImage(self):
        return self.get('featuredImage')

    @featuredImage.setter
    def featuredImage(self, featuredImage):
        self.set('featuredImage', featuredImage)

    @property
    def author(self):
        return self.get('author')

    @author.setter
    def author(self, author):
        self.set('author', author)


class Tag(Object):
    @property
    def name(self):
        return self.get('name')

    @name.setter
    def name(self, name):
        self.set('name', name)

    @property
    def post_count(self):
        if self.get('post_count'):
            return self.get('post_count')
        else:
            return 0

    @classmethod
    def get_by_name(self, name):
        reg = '^' + name + '$'
        try:
            return self.query.matched('name', reg).first()
        except LeanCloudError as e:
            if e.code == 101:
                return None
            else:
                raise e


class TagPostMap(Object):
    @property
    def tag(self):
        return self.get('tag')

    @tag.setter
    def tag(self, tag):
        self.set('tag', tag)

    @property
    def post(self):
        return self.get('post')

    @post.setter
    def post(self, post):
        self.set('post', post)

    @classmethod
    def get_tags_by_post(self, post):
        tags = [x.tag for x in self.query.equal_to('post', post).include('tag').find()]
        if len(tags) == 0:
            return None
        return tags


class User(Object):
    pass


class Attachment(File):
    pass


class Page(Query):
    def __init__(self, post_per_page=10, current_page=1, tag=None):
        self.post_per_page = post_per_page
        self.current_page = current_page
        if not tag:
            Query.__init__(self, Post)
            self.limit(post_per_page + 1)
            self.add_descending('createdAt')
            self._is_tag_index = False
        else:
            Query.__init__(self, TagPostMap)
            self.limit(post_per_page + 1)
            self.add_descending('createdAt')
            self.equal_to('tag', tag)
            self.include('post')
            self._is_tag_index = True

    def posts(self):
        if self.current_page > 1:
            self.skip((self.current_page - 1) * self.post_per_page)
        if self._is_tag_index:
            items = {x.post for x in self.find()}
        else:
            items = self.find()
        return items
