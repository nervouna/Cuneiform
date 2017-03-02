from leancloud import Object, File, User


class Post(Object):
    pass


class Author(User):
    pass


class Attachment(File):
    pass

