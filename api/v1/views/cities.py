#!/usr/bin/python3
"""
View for City objects that handles all default RESTFul API actions.
"""
from api.v1.views import app_views
from flask import (jsonify, abort, make_response, redirect,
                   url_for, request)
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'], strict_slashes=False)
def cities(state_id):
    """Retrieves the list of all City objects on GET.
    Creates a City on POST.
    """
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        all_cities = storage.all(City)
        state_cities = [obj.to_dict() for obj in all_cities.values()
                        if obj.state_id == state_id]
        return jsonify(state_cities)

    if request.method == 'POST':
        city_obj = request.get_json()
        if city_obj is None:
            abort(400, "Not a JSON")
        if city_obj.get('name') is None:
            abort(400, "Missing name")
        city_state = storage.get(State, state_id)
        if not city_state:
            abort(404)
        new_city = City(**city_obj)
        new_city.state_id = state_id
        new_city.save()
        return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def city_id(city_id):
    """Retrieves a City object on GET request.
    Deletes a City object on POST request.
    Updates a City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        city.delete()
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        city_obj = request.get_json()
        if city_obj is None:
            abort(400, "Not a JSON")
        for key, value in city_obj.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict())
