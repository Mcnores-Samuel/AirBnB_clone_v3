#!/usr/bin/python3
""" Module for index route of the api to handle index requests
This module handles the HTTP requests that are sent to the api
for getting the states objects from the storage engine

Methods:
    all_state_objs - Returns a JSON response to an HTTP request
    delete_state_obj - Deletes a state object for a given state id
    create_state_obj - Creates a state object
    update_state_obj - Updates a state object for a given state id
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from flask import request


@app_views.route('/states')
@app_views.route('/states/<state_id>', methods=['GET'])
def all_state_objs(state_id=None):
    """ Returns a JSON response to an HTTP request"""
    states_list = []
    if state_id:
        states = storage.all(State)
        for state in states.values():
            if state.id == state_id:
                states_list.append(state.to_dict())
                break
    else:
        states = storage.all(State)
        for state in states.values():
            states_list.append(state.to_dict())
    if states_list == []:
        return jsonify({"error": "Not found"}), 404
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state_obj(state_id=None):
    """ Deletes a state object for a given state id"""
    states = storage.all(State)
    for state in states.values():
        if state.id == state_id:
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('/states', methods=['POST'])
def create_state_obj():
    """ Creates a state object"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    state = State(**request.get_json())
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state_obj(state_id=None):
    """ Updates a state object for a given state id"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    states = storage.all(State)
    for state in states.values():
        if state.id == state_id:
            for key, value in request.get_json().items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(state, key, value)
            state.save()
            return jsonify(state.to_dict()), 200
    return jsonify({"error": "Not found"}), 404