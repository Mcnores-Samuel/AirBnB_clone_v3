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
from models.state import State
from flask import request


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def all_city_objs(state_id=None, city_id=None):
    """ Returns a JSON response to an HTTP request"""
    cities_list = []
    if state_id:
        state = storage.get(State, state_id)
        if state:
            for city in state.cities:
                cities_list.append(city.to_dict())
            return jsonify(cities_list)
        else:
            return jsonify({"error": "Not found"}), 404
    if city_id:
        city = storage.get(City, city_id)
        if city:
            return jsonify(city.to_dict())
        else:
            return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Not found"}), 404


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city_obj(city_id=None):
    """ Deletes a city object for a given city id"""
    if city_id:
        cities = storage.get(City, city_id)
        if cities:
            storage.delete(cities)
            storage.save()
            return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city_obj(state_id=None):
    """ Creates a city object and returns a JSON response to an HTTP request"""
    if state_id:
        if request.is_json:
            city_json = request.get_json()
            if city_json.get("name") is None:
                return jsonify({"error": "Missing name"}), 400
            else:
                new_city = {}
                new_city = City(state_id=state_id,
                                name=city_json.get("name", None))
                new_city.save()
                return jsonify(new_city.to_dict()), 201
        else:
            return jsonify({"error": "Not a JSON"}), 400
    else:
        return jsonify({"error": "Not found"}), 404


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city_obj(city_id=None):
    """Updates a city object for a given city id and returns a JSON response"""
    if city_id:
        if request.is_json:
            city_json = request.get_json()
            cities = storage.all(City)
            for city in cities.values():
                if city.id == city_id:
                    for key, value in city_json.items():
                        if key not in ["id", "created_at", "updated_at"]:
                            setattr(city, key, value)
                    city.save()
                    return jsonify(city.to_dict()), 200
            return jsonify({"error": "Not found"}), 404
        else:
            return jsonify({"error": "Not a JSON"}), 400
    else:
        return jsonify({"error": "Not found"}), 404
