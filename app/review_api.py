import re
from datetime import datetime

from flask import request
from flask_restx import Resource, fields

from app import review_api, db, place_api
from config import Config
from models.review import Review
from models.user import User
from models.place import Place

"""Define the Review model for the API documentation"""
review_model = review_api.model('Review', {
    'id': fields.String(readonly=True, description='The review unique identifier'),
    'user_id': fields.String(required=True, description='The user identifier'),
    'place_id': fields.String(required=True, description='The place identifier'),
    'comment': fields.String(required=True, description='The review comment'),
    'rating': fields.Float(required=True, description='The rating given by the user'),
    'created_at': fields.DateTime(readonly=True, description='The time the review was created'),
    'updated_at': fields.DateTime(readonly=True, description='The time the review was last updated')
})


@review_api.route("")
class ReviewList(Resource):
    @review_api.doc("get all reviews")
    def get(self):
        """Query all reviews from the database"""
        reviews = Review.query.all()
        result = []
        """Convert each Review object to a dictionary"""
        for review in reviews:
            if review.user.is_deleted == 0 and review.place.is_deleted == 0:
                result.append({
                    "id": review.id,
                    "user_id": review.user_id,
                    "user": {
                        "id": review.user.id,
                        "first_name": review.user.first_name,
                        "last_name": review.user.last_name,
                        "email": review.user.email
                    },
                    "place_id": review.place_id,
                    "place": {
                        "id": review.place.id,
                        "name": review.place.name,
                        "city_id": review.place.city_id,
                        "address": review.place.address,
                        "price_per_night": review.place.price_per_night
                    },
                    "comment": review.comment,
                    "rating": review.rating,
                    "created_at": review.created_at.strftime(Config.datetime_format),
                    "updated_at": review.updated_at.strftime(Config.datetime_format)
                })
        return result

    @review_api.doc('create a new review')
    @review_api.expect(review_model)
    @review_api.response(201, 'Review created successfully')
    @review_api.response(400, 'Invalid input')
    @review_api.response(404, 'User or Place not found')
    def post(self):
        """Create a new review"""
        data = request.get_json()

        if not data.get('user_id') or not data.get('place_id') or not data.get('comment') or not data.get('rating'):
            review_api.abort(400, message='Invalid input')

        user = User.query.filter_by(id=data['user_id']).first()
        place = Place.query.filter_by(id=data['place_id']).first()
        if not user or not place:
            review_api.abort(400, message='User or Place not found')

        new_review = Review(
            user_id=data['user_id'],
            place_id=data['place_id'],
            comment=data['comment'],
            rating=data['rating']
        )
        db.session.add(new_review)
        db.session.commit()

        return {
            "id": new_review.id,
            "user_id": new_review.user_id,
            "place_id": new_review.place_id,
            "comment": new_review.comment,
            "rating": new_review.rating,
            "created_at": new_review.created_at.strftime(Config.datetime_format),
            "updated_at": new_review.updated_at.strftime(Config.datetime_format)
        }, 201


@place_api.route('/<string:place_id>/reviews')
class PlaceReviews(Resource):
    @place_api.doc('get_place_reviews')
    def get(self, place_id):
        """Retrieve all reviews for a specific place"""
        place = Place.query.get(place_id)
        if not place:
            place_api.abort(404, 'Place not found')

        reviews = place.reviews
        result = []
        for review in reviews:
            result.append({
                'id': review.id,
                'user_id': review.user_id,
                'user': {
                    'id': review.reviewer.id,
                    'first_name': review.reviewer.first_name,
                    'last_name': review.reviewer.last_name,
                    'email': review.reviewer.email
                },
                'comment': review.comment,
                'rating': review.rating,
                'created_at': review.created_at.strftime(Config.datetime_format),
                'updated_at': review.updated_at.strftime(Config.datetime_format)
            })
        return result

    @place_api.doc('create_place_review')
    @place_api.expect(review_model)
    @place_api.response(201, 'Review created successfully')
    @place_api.response(400, 'Invalid input')
    def post(self, place_id):
        """Create a new review for a specific place"""
        data = request.get_json()
        if not data.get('user_id') or not data.get('place_id') or not data.get('comment') or not data.get('rating'):
            place_api.abort(400, 'Invalid input')

        user = User.query.filter_by(id=data['user_id'], is_deleted=0).first()

        place = Place.query.filter_by(id=data['place_id'], is_deleted=0).first()
        if not user or not place:
            review_api.abort(404, message='User or Place not found')

        new_review = Review(
            user_id=data['user_id'],
            place_id=data['place_id'],
            comment=data['comment'],
            rating=data['rating']
        )
        db.session.add(new_review)
        db.session.commit()

        return {
            'id': new_review.id,
            'user_id': new_review.user_id,
            'place_id': new_review.place_id,
            'comment': new_review.comment,
            'rating': new_review.rating,
            'created_at': new_review.created_at.strftime(Config.datetime_format),
            'updated_at': new_review.updated_at.strftime(Config.datetime_format)
        },