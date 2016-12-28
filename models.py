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
    def marked_content(self):
        return self.get('marked_content')

    @marked_content.setter
    def marked_content(self, marked_content):
        self.set('marked_content', marked_content)

    @property
    def featured_image(self):
        return self.get('featured_image')

    @featured_image.setter
    def featured_image(self, featured_image):
        self.set('featured_image', featured_image)

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
    def get_by_name(cls, name):
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
    def get_tags_by_post(cls, post):
        tags = [x.tag for x in self.query.equal_to('post', post).include('tag').find()]
        if len(tags) == 0:
            return None
        return tags


class User(Object):
    pass


class Attachment(File):
    pass


class Page(Query):
    def __init__(self, post_per_page, current_page, tag=None):
        self._post_per_page = post_per_page
        self._current_page = current_page
        if tag is None:
            Query.__init__(self, Post)
            self.limit(post_per_page + 1)
            self.add_descending('createdAt')
            self._is_tag_index = False
        elif isinstance(tag, Tag):
            Query.__init__(self, TagPostMap)
            self.limit(post_per_page + 1)
            self.add_descending('createdAt')
            self.equal_to('tag', tag)
            self.include('post')
            self._is_tag_index = True
        else:
            raise TypeError('tag should be `None` or instance of `Tag`')

    def posts(self):
        self.has_next = False
        if self._current_page > 1:
            self.skip((self._current_page - 1) * self._post_per_page)
        if self._is_tag_index:
            items = [x.post for x in self.find()]
        else:
            items = self.find()
        if len(items) - self._post_per_page == 1:
            self.has_next = True
            return items[:-1]
        return items
