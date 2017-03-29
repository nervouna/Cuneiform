from functools import wraps
import sys
import re
import unicodedata
import time

from flask import abort
from flask import request
from flask import url_for
import pinyin

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


def pinyinify(string):
    # TODO: Use static file instead of constructing table in real time
    table = dict()
    for i in range(sys.maxunicode):
        if re.match('P|S|Z|C', unicodedata.category(chr(i))) is not None:
            table[i] = '-'
    string = string.translate(table)
    for char in [x for x in string if unicodedata.name(x).startswith('CJK')]:
        string = string.replace(char, pinyin.get(char, format='strip') + '-')
    string = re.sub('\-+', '-', string).strip('-')
    return pinyin.get(string, delimiter='', format='strip').lower()