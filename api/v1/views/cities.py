#!/usr/bin/python3
""" Module for index route of the api to handle index requests  for cities
This module handles the HTTP requests that are sent to the api
for getting the cities objects from the storage engine

Methods:
    all_city_objs - Returns a JSON response to an HTTP request
    delete_city_obj - Deletes a city object for a given city id
    create_city_obj - Creates a city object
    update_city_obj - Updates a city object for a given city id
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from flask import request


@app_views.route('/states/<state_id>/cities')
@app_views.route('/states/<state_id>/cities/<city_id>', methods=['GET'])
def all_city_objs(state_id=None, city_id=None):
    """ Returns a JSON response to an HTTP request"""
    cities_list = []
    if state_id and city_id:
        cities = storage.all(City)
        for city in cities.values():
            if city.id == city_id and city.state_id == state_id:
                cities_list.append(city.to_dict())
                break
    elif state_id:
        cities = storage.all(City)
        for city in cities.values():
            if city.state_id == state_id:
                cities_list.append(city.to_dict())
    else:
        cities = storage.all(City)
        for city in cities.values():
            cities_list.append(city.to_dict())
    if cities_list == []:
        return jsonify({"error": "Not found"}), 404
    return jsonify(cities_list)


# @app_views.route('/cities/<city_id>', methods=['DELETE'])
# def delete_city_o