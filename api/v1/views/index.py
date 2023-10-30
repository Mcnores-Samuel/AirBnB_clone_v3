#!/usr/bin/python3
""" Module for index route of the api to handle index requests """
from api.v1.views import app_views
from flask import jsonify
import models
from models import storage
from models.base_model import BaseModel
from models.place import Place
from models.review import Review
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.state import State



@app_views.route('/status')
def status():
    """ Returns a JSON response to an HTTP request"""
    return jsonify({"status": "OK"})



@app_views.route('/stats')
def api_status():
    """checks the API stats of the classes"""
    classes = {"amenities": Amenity, "cities": City,
               "places": Place, "reviews": Review,
               "states": State, "users": User}
    for key in classes:
        classes[key] = storage.count(classes[key])
    return jsonify(classes)
