# -*- coding: utf-8 -*-

import os

import leancloud

from cuneiform import app
from cloud import engine


APP_ID = os.environ["LEANCLOUD_APP_ID"]
APP_KEY = os.environ["LEANCLOUD_APP_KEY"]
MASTER_KEY = os.environ["LEANCLOUD_APP_MASTER_KEY"]
PORT = int(os.environ["LEANCLOUD_APP_PORT"])
FLASK_SECRET_KEY = bytes(os.environ["FLASK_SECRET_KEY"], "utf-8")

leancloud.init(APP_ID, app_key=APP_KEY, master_key=MASTER_KEY)
leancloud.use_master_key(False)

application = leancloud.engine.CookieSessionMiddleware(engine, secret=FLASK_SECRET_KEY)


if __name__ == "__main__":
    from werkzeug.serving import run_simple
    application.debug = True
    run_simple("0.0.0.0", 3000, application, use_reloader=True, use_debugger=True)
