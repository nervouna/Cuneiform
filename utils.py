# coding: utf-8

from leancloud import Query
from leancloud import LeanCloudError

from markdown import markdown

from models import Post
from models import User
from models import Attachment
from models import Tag
from models import TagPostMap

import re


def parse_tag_names(tag_string):
    tag_string = tag_string.strip()
    if len(tag_string) == 0:
        return None
    else:
        return set(x.strip() for x in re.split('[,，;；、]', tag_string) if len(x) > 0)


def allowed_file(ext):
    allowed_ext = ['jpg', 'jpeg', 'png', 'svg', 'gif', 'bmp']
    return ext.lower() in allowed_ext
