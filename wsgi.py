# -*- coding: utf-8 -*-

import os

import leancloud

from app import app


APP_ID = os.environ["LEANCLOUD_APP_ID"]
APP_KEY = os.environ["LEANCLOUD_APP_KEY"]
MASTER_KEY = os.environ["LEANCLOUD_APP_MASTER_KEY"]
PORT = int(os.environ["LEANCLOUD_APP_PORT"])
FLASK_SECRET_KEY = bytes(os.environ["FLASK_SECRET_KEY"], "utf-8")

leancloud.init(APP_ID, app_key=APP_KEY, master_key=MASTER_KEY)
leancloud.use_master_key(False)

app.secret_key = FLASK_SECRET_KEY
app = leancloud.engine.CookieSessionMiddleware(app, secret=app.secret_key)

application = app


if __name__ == "__main__":
    from werkzeug.serving import run_simple
    extra_dirs = ["templates", ]
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in os.walk(extra_dir):
            for filename in files:
                filename = os.path.join(dirname, filename)
                if os.path.isfile(filename):
                    extra_files.append(filename)
    application.debug = True
    run_simple("0.0.0.0", 3000, application, use_reloader=True, use_debugger=True, extra_files=extra_files)
