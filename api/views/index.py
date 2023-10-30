#!/usr/bin/python3
""" Module for index route of the api to handle index requests """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """ Returns a JSON response to an HTTP request"""
    return jsonify({"status": "OK"})