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


class User(Object):
    pass


class Attachment(File):
    pass
