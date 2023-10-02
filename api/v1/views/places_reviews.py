#!/usr/bin/python3
"""Review objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_review_by_id(review_id):
    """Retrieves, Deletes or Updates a Review object by it's id"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    if request.method == "GET":
        return jsonify(review.to_dict())

    elif request.method == "DELETE":
        review.delete()
        storage.save()
        return jsonify({}), 200

    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    nope = {"id", "user_id", "place_id", "created_at", "updated_at"}
    [setattr(review, key, val) for key, val in data.items() if key not in nope]
    review.save()
    return jsonify(review.to_dict()), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a Review object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    if "user_id" not in data:
        return "Missing user_id", 400
    user = storage.get("User", data["user_id"])
    if user is None:
        abort(404)
    if "text" not in data:
        return "Missing text", 400
    data["place_id"] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    nope = {"id", "user_id", "place_id", "created_at", "updated_at"}
    [setattr(review, key, val) for key, val in data.items() if key not in nope]
    review.save()
    return jsonify(review.to_dict()), 200
