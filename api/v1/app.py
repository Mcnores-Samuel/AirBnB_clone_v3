#!/usr/bin/python3
""" Module for app.py and its routes """
from flask import Flask
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False

@app.teardown_appcontext
def teardown_appcontext(error):
    """ Closes storage session after each request"""
    storage.close()

if __name__ == "__main__":
    HBNB_API_HOST = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    HBNB_API_PORT = os.environ.get('HBNB_API_PORT', '5000')
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)