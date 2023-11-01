#!/usr/bin/python3
""" Module for index route of the api to handle index requests """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.place import Place
from models.city import City
from flask import request, abort


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def all_place_objs(city_id=None, place_id=None):
    """ Returns a JSON response to an HTTP request"""
    places_list = []
    if city_id:
        city = storage.get(City, city_id)
        if city:
            for place in city.places:
                places_list.append(place.to_json())
            return jsonify(places_list)
        else:
            return jsonify({"error": "Not found"}), 404
    if place_id:
        place = storage.get(Place, place_id)
        if place:
            return jsonify(place.to_json())
        else:
            return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Not found"}), 404


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_obj(place_id=None):
    """ Deletes a place object for a given place id"""
    if place_id:
        places = storage.get(Place, place_id)
        if places:
            storage.delete(places)
            storage.save()
            return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place_obj(city_id=None):
    """ Creates a place object and returns a JSON response
    to an HTTP request
    """
    if city_id:
        if request.is_json:
            place_json = request.get_json()
            city = storage.get(City, city_id)
            if not city:
                abort(404, "Not found")
            if 'user_id' not in place_json:
                abort(400, "Missing user_id")
            if 'name' not in place_json:
                abort(400, "Missing name")
            place_json['city_id'] = city_id
            place = Place(**place_json)
            place.save()
            return jsonify(place.to_json()), 201
        else:
            return jsonify({"error": "Not a JSON"}), 400
    return jsonify({"error": "Not found"}), 404


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place_obj(place_id=None):
    """ Updates a place object for a given place id"""
    if place_id:
        place = storage.get(Place, place_id)
        if not place:
            abort(404, "Not found")
        if not request.get_json():
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in request.get_json().items():
            if key not in ['id', 'user_id', 'city_id', 'created_at',
                           'updated_at']:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_json()), 200
    return jsonify({"error": "Not found"}), 404
