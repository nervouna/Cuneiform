# -*- coding: utf-8 -*-

import os
import leancloud
from app import app
from app import engine
from leancloud.engine.cookie_session import CookieSessionMiddleware

from gevent import monkey
monkey.patch_all()


APP_ID = os.environ['LEANCLOUD_APP_ID']
APP_KEY = os.environ['LEANCLOUD_APP_KEY']
MASTER_KEY = os.environ['LEANCLOUD_APP_MASTER_KEY']
PORT = int(os.environ['LEANCLOUD_APP_PORT'])
try:
    # Make sure you have configured your SECRET_KEY in LeanCloud console.
    SECRET_KEY = bytes(os.environ['FLASK_SECRET_KEY'], 'utf-8')
except KeyError:
    # If the app fails to get a SECRET_KEY from os.environ, use dev key instead
    # And boy it's dangerous on production servers, take care.
    SECRET_KEY = b'dev'

app.secret_key = SECRET_KEY

leancloud.init(APP_ID, app_key=APP_KEY, master_key=MASTER_KEY)
# Using master key is like granting root access in Linux. Use it wisely.
leancloud.use_master_key(False)

application = CookieSessionMiddleware(engine, secret=app.secret_key)


if __name__ == '__main__':
    # Following code is only excuted when debugging on localhost.
    from gevent.pywsgi import WSGIServer
    from geventwebsocket.handler import WebSocketHandler
    from werkzeug.serving import run_with_reloader
    from werkzeug.debug import DebuggedApplication

    @run_with_reloader
    def run():
        global application
        app.debug = True
        application = DebuggedApplication(application, evalex=True)
        server = WSGIServer(('localhost', PORT), application)
        server.serve_forever()

    run()
