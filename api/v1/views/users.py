#!/usr/bin/python3
"""Module for index route of the api to handle index requests
This module handles the HTTP requests that are sent to the api
for getting the states objects from the storage engine
Methods:
    all_users_objs - Returns a JSON response to an HTTP request
    delete_user_obj - Deletes a user object for a given user id
    create_user_obj - Creates a user object
    update_user_obj - Updates a user object for a given user id
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from flask import request


@app_views.route('/users', methods=['GET'])
@app_views.route('/users/<user_id>', methods=['GET'])
def all_users_objs(user_id=None):
    """ Returns a JSON response to an HTTP request"""
    users = []
    if user_id:
        users_list = storage.all(User)
        for user in users_list.values():
            if user.id == user_id:
                users.append(user.to_dict())
                break
    else:
        users_list = storage.all(User)
        for user in users_list.values():
            users.append(user.to_dict())
    if users == []:
        return jsonify({"error": "Not found"}), 404
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user_obj(user_id=None):
    """ Deletes a user object for a given user id"""
    if user_id:
        users = storage.all(User)
        for user in users.values():
            if user.id == user_id:
                storage.delete(user)
                storage.save()
                return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('/users', methods=['POST'])
def create_user_obj():
    """ Creates a user object and returns a JSON response to an HTTP request"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in request.get_json():
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in request.get_json():
        return jsonify({"error": "Missing password"}), 400
    user = User(**request.get_json())
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user_obj(user_id=None):
    """ Updates a user object for a given user id"""
    if user_id:
        users = storage.all(User)
        for user in users.values():
            if user.id == user_id:
                if not request.get_json():
                    return jsonify({"error": "Not a JSON"}), 400
                for key, value in request.get_json().items():
                    if key not in ['id', 'email', 'created_at', 'updated_at']:
                        setattr(user, key, value)
                user.save()
                return jsonify(user.to_dict()), 200
    return jsonify({"error": "Not found"}), 404