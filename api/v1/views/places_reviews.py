#!/usr/bin/python3
"""
View for Places_reviews objects that handles all default RESTFul API actions.
"""
from api.v1.views import app_views
from flask import (jsonify, abort, make_response, request)
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'], strict_slashes=False)
def places_reviews_id(place_id=None):
    """Retrieves the list of all Review objects on GET.
    Creates a Review on POST.
    """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        all_reviews = storage.all(Review).values()
        place_reviews = [obj.to_dict() for obj in all_reviews
                         if obj.place_id == place_id]
        return jsonify(place_reviews)

    if request.method == 'POST':
        review_data = request.get_json()
        if review_data is None:
            abort(400, "Not a JSON")
        if review_data.get('user_id') is None:
            abort(400, "Missing user_id")
        user_obj = storage.get(User, review_data.get('user_id'))
        if not user_obj:
            abort(404, 'Not found')
        if review_data.get('text') is None:
            abort(400, 'Missing text')
        new_review = Review(**review_data)
        new_review.place_id = place_id
        new_review.save()
        return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def reviews_id(review_id):
    """Retrieves a Review object on GET request.
    Deletes a Review object on POST request.
    Updates a Review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        review.delete()
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        review_data = request.get_json()
        if review_data is None:
            abort(400, "Not a JSON")
        for key, value in review_data.items():
            if key not in ['id', 'user_id',
                           'place_id', 'created_at', 'updated_at']:
                setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict()), 200
