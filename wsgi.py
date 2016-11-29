# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()

import os

import leancloud

from app import app
from app import engine

APP_ID = os.environ['LEANCLOUD_APP_ID']
APP_KEY = os.environ['LEANCLOUD_APP_KEY']
MASTER_KEY = os.environ['LEANCLOUD_APP_MASTER_KEY']
PORT = int(os.environ['LEANCLOUD_APP_PORT'])
try:
    # Make sure you have configured your SECRET_KEY in LeanCloud console.
    SECRET_KEY = os.environ['FLASK_SECRET_KEY']
except KeyError:
    # If the app failed to get a SECRET_KEY from os.environ, use dev key instead
    # And boy it's dangerous on production servers, take care.
    SECRET_KEY = 'dev'

leancloud.init(APP_ID, app_key=APP_KEY, master_key=MASTER_KEY)
# Using master key is like granting root access in Linux. Use it wisely.
leancloud.use_master_key(False)

application = engine


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
