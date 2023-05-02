#!/usr/bin/python3
"""
View for State objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import (jsonify, abort, make_response, redirect,
                   url_for, request)
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    """Retrieves the list of all State objects on GET.
    Creates a State on POST.
    """
    if request.method == 'GET':
        objs = storage.all(State)
        all_states = [obj.to_dict() for obj in objs.values()]
        return jsonify(all_states)

    if request.method == 'POST':
        state_obj = request.get_json()
        if state_obj is None:
            abort(400, "Not a JSON")
        if state_obj.get('name') is None:
            abort(400, "Missing name")
        new_state = State(**state_obj)
        new_state.save()
        return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def state_id(state_id):
    """Retrieves a State object on GET request.
    Deletes a State object on POST request.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(state.to_dict())

    if request.method == 'DELETE':
        state.delete()
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        state_obj = request.get_json()
        if state_obj is None:
            abort(400, "Not a JSON")
        for key, value in state_obj.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict())
