#!/usr/bin/python3
""" Module for index route of the api to handle index requests """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from flask import request, abort


@app_views.route('places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def all_review_objs(place_id=None, review_id=None):
    """ Returns a JSON response to an HTTP request"""
    reviews_list = []
    if place_id:
        place = storage.get(Place, place_id)
        if place:
            for review in place.reviews:
                reviews_list.append(review.to_dict())
            return jsonify(reviews_list)
        else:
            return jsonify({"error": "Not found"}), 404
    if review_id:
        review = storage.get(Review, review_id)
        if review:
            return jsonify(review.to_dict())
        else:
            return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Not found"}), 404


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review_obj(review_id=None):
    """ Deletes a review object for a given review id"""
    if review_id:
        reviews = storage.get(Review, review_id)
        if reviews:
            storage.delete(reviews)
            storage.save()
            return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review_obj(place_id=None):
    """ Creates a review object and returns a JSON response
    to an HTTP request
    """
    if place_id:
        if request.is_json:
            review_json = request.get_json()
            place = storage.get(Place, place_id)
            if not place:
                abort(404, "Not found")
            if 'user_id' not in review_json:
                abort(400, "Missing user_id")
            if 'text' not in review_json:
                abort(400, "Missing text")
            user_id = review_json['user_id']
            user = storage.get(User, user_id)
            if not user:
                abort(404, "Not found")
            review = Review(**review_json)
            review.save()
            return jsonify(review.to_dict()), 201
        else:
            return jsonify({"error": "Not a JSON"}), 400
    return jsonify({"error": "Not found"}), 404


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review_obj(review_id=None):
    """ Updates a review object for a given review id"""
    if review_id:
        review = storage.get(Review, review_id)
        if not review:
            return jsonify({"error": "Not found"}), 404
        if not request.get_json():
            return jsonify({"error": "Not a JSON"}), 400
        ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in request.get_json().items():
            if key not in ignore:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
    return jsonify({"error": "Not found"}), 404
