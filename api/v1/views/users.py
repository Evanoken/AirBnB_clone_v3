#!/usr/bin/python3
"""
View for User objects that handles all default RESTFul API actions.
"""
from api.v1.views import app_views
from flask import (jsonify, abort, make_response, request)
from models import storage
from models.user import User


@app_views.route('/users/<user_id>/',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def user_id(user_id):
    """Retrieves an User object on GET.
    Updates a User object on PUT.
    Deletes a User object on DELETE.
    """
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(user_obj.to_dict())

    if request.method == 'DELETE':
        user_obj.delete()
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        user_data = request.get_json()
        if user_data is None:
            abort(400, "Not a JSON")
        for key, value in user_data.items():
            if key not in ['id', 'created_at', 'updated_at', 'email']:
                setattr(user_obj, key, value)
        storage.save()
        return jsonify(user_obj.to_dict()), 200


@app_views.route('/users', methods=['GET', 'POST'],
                 strict_slashes=False)
def user():
    """Retrieves the list of all User object on GET.
    Creates a User object on POST.
    """

    if request.method == 'GET':
        all_users = storage.all(User)
        return jsonify([obj.to_dict() for obj in all_users.values()])

    if request.method == 'POST':
        user_data = request.get_json()
        if user_data is None:
            abort(400, "Not a JSON")
        if 'email' not in user_data:
            abort(400, 'Missing email')
        if 'password' not in user_data:
            abort(400, 'Missing password')
        new_user = User(**user_data)
        new_user.save()
        return make_response(jsonify(new_user.to_dict()), 201)
