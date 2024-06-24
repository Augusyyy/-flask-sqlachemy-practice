import re
from datetime import datetime

from flask import request
from flask_restx import Resource, fields

from app import review_api, db
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
            result.append({
                "id": review.id,
                "user_id": review.user_id,
                "place_id": review.place_id,
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


@review_api.route('/<string:review_id>')
class ReviewById(Resource):
    @review_api.doc('get_review')
    def get(self, review_id):
        """Query the review by ID from the database"""
        review = Review.query.filter_by(id=review_id).first()
        if review is None:
            review_api.abort(400, message='Review not found!')
        else:
            """Convert the Review object to a dictionary"""
            return {
                "id": review.id,
                "user_id": review.user_id,
                "place_id": review.place_id,
                "comment": review.comment,
                "rating": review.rating,
                "created_at": review.created_at.strftime(Config.datetime_format),
                "updated_at": review.updated_at.strftime(Config.datetime_format)
            }

    @review_api.doc('update_review')
    @review_api.expect(review_model)
    @review_api.response(200, 'Review updated successfully')
    @review_api.response(400, 'Invalid input')
    @review_api.response(404, 'Review not found')
    def put(self, review_id):
        data = request.get_json()
        if not data:
            review_api.abort(400, "Invalid input")

        review = Review.query.filter_by(id=review_id).first()
        if not review:
            review_api.abort(404, 'Review not found')

        if 'comment' in data:
            review.comment = data['comment']
        if 'rating' in data:
            review.rating = data['rating']

        review.updated_at = datetime.now()
        db.session.commit()

        return {
            "id": review.id,
            "user_id": review.user_id,
            "place_id": review.place_id,
            "comment": review.comment,
            "rating": review.rating,
            "created_at": review.created_at.strftime(Config.datetime_format),
            "updated_at": review.updated_at.strftime(Config.datetime_format)
        }, 200

    @review_api.doc('delete_review')
    def delete(self, review_id):
        review = Review.query.filter_by(id=review_id).first()
        if review is None:
            return review_api.abort(400, 'User not found')
        try:
            db.session.delete(review)
            db.session.commit()
            return "delete successfully", 200
        except Exception as e:
            db.session.rollback()
            review_api.abort(404, message='Create fail')