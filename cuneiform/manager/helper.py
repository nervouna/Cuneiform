from functools import wraps

from flask import abort
from flask import request
from flask import url_for

from cuneiform.models import Author


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


def allowed_file(filename):
    ext = filename.rsplit('.', 1)[-1]
    allowed_ext = ['jpg', 'jpeg', 'png', 'svg', 'gif', 'bmp']
    return ext.lower() in allowed_ext


def get_current_page(ctx):
    page = ctx.args.get('page')
    return 1 if not page else int(_page)


def paginate(query, current_page, limit):
    return query.add_descending('createdAt').limit(limit + 1).skip((current_page - 1) * limit)


def redirect_url(default='index'):
    return request.args.get('next') or request.referrer or url_for('default')