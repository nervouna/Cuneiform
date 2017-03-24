from flask import Flask


app = Flask(__name__)
app.config.update(dict(
  PREFERRED_URL_SCHEME = 'https'
))

import cuneiform.views
