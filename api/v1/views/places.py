#!/usr/bin/python3
""" Module for index route of the api to handle index requests
This module handles the HTTP requests that are sent to the api
for getting the cities objects from the storage engine
Methods:
    all_places_objs - Returns a JSON response to an HTTP request
    delete_place_obj - Deletes a place object for a given place id
    create_place_obj - Creates a place object
    update_place_obj - Updates a place object for a given place id
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.place import Place
from flask import request
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'])
@app_views.route('/places/<place_id>', methods=['GET'])
def all_places_objs(city_id=None, place_id=None):
    """ Returns a JSON response to an HTTP request"""
    places_list = []
    if place_id:
        places = storage.all(Place)
        for place in places.values():
            if place.id == place_id:
                places_list.append(place.to_dict())
                break

    elif city_id:
        places = storage.all(Place)
        for place in places.values():
            if place.city_id == city_id:
                places_list.append(place.to_dict())
    else:
        places = storage.all(Place)
        for place in places.values():
            places_list.append(place.to_dict())
    if places_list == []:
        return jsonify({"error": "Not found"}), 404
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place_obj(place_id=None):
    """ Deletes a place object for a given place id"""
    if place_id:
        places = storage.all(Place)
        for place in places.values():
            if place.id == place_id:
                storage.delete(place)
                storage.save()
                return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place_obj(city_id=None):
    """ Creates a place object and returns a JSON
    response to an HTTP request
    """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request.get_json():
        return jsonify({"error": "Missing user_id"}), 400
    if 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    if city_id:
        cities = storage.all(City)
        for city in cities.values():
            if city.id == city_id:
                place = Place(**request.get_json())
                place.save()
                return jsonify(place.to_dict()), 201
    return jsonify({"error": "Not found"}), 404


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place_obj(place_id=None):
    """ Updates a place object for a given place id"""
    if place_id:
        place = storage.get(Place, place_id)
        if place is None:
            return jsonify({"error": "Not found"}), 404
        if not request.get_json():
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in request.get_json().items():
            if key not in ['id', 'user_id', 'city_id', 'created_at',
                           'updated_at']:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('/places_search', methods=['POST'])
def search_place_obj():
    """ Searches for a place object for a given place id"""
    if request.is_json:
        place_json = request.get_json()
        if place_json == {}:
            return jsonify([place.to_dict() for place in
                            storage.all(Place).values()])
        if place_json.get("states") is None:
            states = [state for state in storage.all("State").values()]
        else:
            states = [storage.get("State", state_id) for state_id in
                      place_json.get("states")]
        if place_json.get("cities") is None:
            cities = [city for city in storage.all("City").values()]
        else:
            cities = [storage.get("City", city_id) for city_id in
                      place_json.get("cities")]
        if place_json.get("amenities") is None:
            amenities = [amenity for amenity in
                         storage.all("Amenity").values()]
        else:
            amenities = [storage.get("Amenity", amenity_id) for amenity_id in
                         place_json.get("amenities")]
        places = []
        for state in states:
            for city in state.cities:
                if city in cities:
                    for place in city.places:
                        if place not in places:
                            if all([amenity in place.amenities
                                    for amenity in amenities]):
                                places.append(place)
        return jsonify([place.to_dict() for place in places])
    else:
        return jsonify({"error": "Not a JSON"}), 400
