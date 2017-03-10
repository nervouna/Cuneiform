from leancloud import Object
from leancloud import User
from leancloud import File


class Post(Object):
    pass


class Author(User):
    pass


class Attachment(File):
    pass


class Tag(Object):
	pass


class TagPostMap(Object):
	pass