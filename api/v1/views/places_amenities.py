#!/usr/bin/python3
"""
View for Places_amenities objects that handles all default RESTFul API actions.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def place_amenities_id(place_id=None):
    """Retrieves all amenities from a place
    """
    place_obj = storage.get(Place, place_id)

    if request.method == 'GET':
        if place_obj is None:
            abort(404, 'Not found')
        place_amenities = [obj.to_dict() for obj in place_obj.amenities]
        return jsonify(place_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'])
def amenity_to_place(place_id=None, amenity_id=None):
    """Delete amenity from place.
    """
    place_obj = storage.get(Place, place_id)
    amenity_obj = storage.get(Amenity, amenity_id)
    if place_obj is None or amenity_obj is None:
        abort(404, 'Not found')

    if request.method == 'DELETE':
        if amenity_obj not in place_obj.amenities:
            abort(404, 'Not found')
        place_obj.amenities.remove(amenity_obj)
        storage.save()
        return jsonify({}), 200

    if request.method == 'POST':
        if amenity_obj in place_obj.amenities:
            return jsonify(amenity_obj.to_dict()), 200
        place_obj.amenities.append(amenity_obj)
        return jsonify(amenity_obj.to_dict()), 201
