#!/usr/bin/python3
""" Module for index route of the api to handle index requests
This module handles the HTTP requests that are sent to the api
for getting the cities objects from the storage engine

Methods:
    all_amenity_objs - Returns a JSON response to an HTTP request
    delete_amenity_obj - Deletes a amenity object for a given amenity id
    create_amenity_obj - Creates a amenity object
    update_amenity_obj - Updates a amenity object for a given amenity id
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from flask import request


@app_views.route('/amenities', methods=['GET'])
@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def all_amenity_objs(amenity_id=None):
    """ Returns a JSON response to an HTTP request"""
    amenities = []
    if amenity_id:
        amenities_list = storage.all(Amenity)
        for amenity in amenities_list.values():
            if amenity.id == amenity_id:
                amenities.append(amenity.to_dict())
                break
    else:
        amenities_list = storage.all(Amenity)
        for amenity in amenities_list.values():
            amenities.append(amenity.to_dict())
    if amenities == []:
        return jsonify({"error": "Not found"}), 404
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity_obj(amenity_id=None):
    """ Deletes a amenity object for a given amenity id"""
    if amenity_id:
        amenities = storage.all(Amenity)
        for amenity in amenities.values():
            if amenity.id == amenity_id:
                storage.delete(amenity)
                storage.save()
                return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('/amenities', methods=['POST'])
def create_amenity_obj():
    """Creates a amenity object and returns a JSON
    response to an HTTP request
    """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    amenity = Amenity(**request.get_json())
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity_obj(amenity_id=None):
    """ Updates a amenity object for a given amenity id"""
    if amenity_id:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            return jsonify({"error": "Not found"}), 404
        if not request.get_json():
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in request.get_json().items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    else:
        return jsonify({"error": "Not found"}), 404
