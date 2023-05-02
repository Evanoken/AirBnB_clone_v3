#!/usr/bin/python3
"""
View for Amenity objects that handles all default RESTFul API actions.
"""
from api.v1.views import app_views
from flask import (jsonify, abort, make_response, request)
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/<amenity_id>/',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def amenity_id(amenity_id):
    """Retrieves an Amenity object on GET.
    Updates a Amenity object on PUT.
    Deletes a Amenity object on DELETE.
    """
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(amenity_obj.to_dict())

    if request.method == 'DELETE':
        amenity_obj.delete()
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        amenity_data = request.get_json()
        if amenity_data is None:
            abort(400, "Not a JSON")
        for key, value in amenity_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity_obj, key, value)
        storage.save()
        return jsonify(amenity_obj.to_dict()), 200


@app_views.route('/amenities', methods=['GET', 'POST'],
                 strict_slashes=False)
def amenity():
    """Retrieves the list of all Amenity object on GET.
    Creates a Amenity object on POST.
    """

    if request.method == 'GET':
        all_amenities = storage.all(Amenity)
        return jsonify([obj.to_dict() for obj in all_amenities.values()])

    if request.method == 'POST':
        amenity_data = request.get_json()
        if amenity_data is None:
            abort(400, "Not a JSON")
        if amenity_data.get('name') is None:
            abort(400, "Missing name")
        new_amenity = Amenity(**amenity_data)
        new_amenity.save()
        return make_response(jsonify(new_amenity.to_dict()), 201)
