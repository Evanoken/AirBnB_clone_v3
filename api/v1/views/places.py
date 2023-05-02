#!/usr/bin/python3
"""
View for Place objects that handles all default RESTFul API actions.
"""
from api.v1.views import app_views
from flask import (jsonify, abort, make_response, request)
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def places_id(city_id):
    """Retrieves the list of all Place objects on GET.
    Creates a Place on POST.
    """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        all_places = storage.all(Place)
        city_places = [obj.to_dict() for obj in all_places.values()
                       if obj.city_id == city_id]
        return jsonify(city_places)

    if request.method == 'POST':
        place_data = request.get_json()
        if place_data is None:
            abort(400, "Not a JSON")
        if place_data.get('user_id') is None:
            abort(400, "Missing user_id")
        user_obj = storage.get(User, place_data.get('user_id'))
        if not user_obj:
            abort(404, 'Not found')
        if place_data.get('name') is None:
            abort(400, 'Missing name')
        new_place = Place(**place_data)
        new_place.city_id = city_id
        new_place.save()
        return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_id(place_id):
    """Retrieves a Place object on GET request.
    Deletes a Place object on POST request.
    Updates a Place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        place.delete()
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        place_data = request.get_json()
        if place_data is None:
            abort(400, "Not a JSON")
        for key, value in place_data.items():
            if key not in ['id', 'user_id',
                           'city_id', 'created_at', 'updated_at']:
                setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    """Retrieves all Place objects depending of the JSON
    in the body of the request. """
    places_data = request.get_json()
    if places_data is None:
        abort(400, "Not a JSON")
    all_places = [place for place in storage.all(Place).values()]
    if places_data and len(places_data):
        states = places_data.get('states')
        cities = places_data.get('cities')
        amenities = places_data.get('amenities')

        if states:
            all_cities = storage.all(City).values()
            state_cities = set([obj.id for obj in all_cities
                                if obj.state_id in states])
        else:
            place_cities = set()

        if len(cities):
            cities = set([obj_id for obj_id in cities
                          if storage.get(City, obj_id)])
            place_cities = state_cities | cities

        if len(place_cities):
            all_places = [place for place in all_places
                          if obj.city_id in place_cities]

        if len(amenities):
            amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
            places = [place.to_dict() for place in all_places if
                      all([am in place.amenities for am in amenities_obj])]
    else:
        places = [place.to_dict() for place in all_places]

    return jsonify(places)
