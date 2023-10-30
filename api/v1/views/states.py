#!/usr/bin/python3
""" Module for index route of the api to handle index requests
This module handles the HTTP requests that are sent to the api
for getting the states objects from the storage engine
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State


@app_views.route('/states')
@app_views.route('/states/<state_id>', methods=['GET'])
def states(state_id=None):
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