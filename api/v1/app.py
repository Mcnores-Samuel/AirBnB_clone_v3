#!/usr/bin/python3
""" Module for app.py and its routes"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.url_map.strict_slashes = False

HBNB_API_HOST = os.environ.get('HBNB_API_HOST', '0.0.0.0')
HBNB_API_PORT = os.environ.get('HBNB_API_PORT', '5000')

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(error):
    """Closes storage session after each request"""
    storage.close()


if __name__ == "__main__":
    app.run(host=HBNB_API_HOST, port=int(HBNB_API_PORT),
            threaded=True)
