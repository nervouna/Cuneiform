import re
from functools import wraps
from flask import abort
from models import Author


def protected(func):
    @wraps(func)
    def secret_view(*args, **kwargs):
        current_user = Author.get_current()
        if not current_user:
            abort(401)
        elif not current_user.is_authenticated():
            abort(403)
        else:
            return func(*args, **kwargs)
    return secret_view


def parse_tag_names(tag_string):
    tag_string = tag_string.strip()
    if len(tag_string) == 0:
        return None
    else:
        return set(x.strip() for x in re.split('[,，;；、]', tag_string) if len(x) > 0)


def allowed_file(ext):
    allowed_ext = ['jpg', 'jpeg', 'png', 'svg', 'gif', 'bmp']
    return ext.lower() in allowed_ext
