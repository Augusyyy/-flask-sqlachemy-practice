import re
from datetime import datetime

from flask import request
from flask_restx import Resource, fields

from app import amenity_api, db
from config import Config
from models.amenity import Amenity

"""Define the Amenity model for the API documentation"""
amenity_model = amenity_api.model('Amenity', {
    'id': fields.String(readonly=True, description='The amenity unique identifier'),
    'name': fields.String(required=True, description='The amenity name'),
    'created_at': fields.DateTime(readonly=True, description='The time the amenity was created'),
    'updated_at': fields.DateTime(readonly=True, description='The time the amenity was last updated')
})

@amenity_api.route("")
class AmenityList(Resource):
    @amenity_api.doc("get all amenities")
    def get(self):
        """Query all amenities from the database"""
        amenities = Amenity.query.all()
        result = []
        """Convert each Amenity object to a dictionary"""
        for amenity in amenities:
            result.append({
                "id": amenity.id,
                "name": amenity.name,
                "created_at": amenity.created_at.strftime(Config.datetime_format),
                "updated_at": amenity.updated_at.strftime(Config.datetime_format)
            })
        return result

    @amenity_api.doc('create a new amenity')
    def post(self):
        """Create a new amenity"""
        data = request.get_json()

        if not data.get('name'):
            amenity_api.abort(400, message='Invalid input')

        new_amenity = Amenity(name=data['name'])
        db.session.add(new_amenity)
        db.session.commit()

        return {
            "id": new_amenity.id,
            "name": new_amenity.name,
            "created_at": new_amenity.created_at.strftime(Config.datetime_format),
            "updated_at": new_amenity.updated_at.strftime(Config.datetime_format)
        }

    @amenity_api.doc('delete_amenity')
    def delete(self, amenity_id):
        amenity = Amenity.query.filter_by(id=amenity_id).first()
        if amenity is None:
            return amenity_api.abort(404, 'User not found')
        try:
            db.session.delete(amenity)
            db.session.commit()
            return "delete successfully", 200
        except Exception as e:
            db.session.rollback()
            amenity_api.abort(404, message='Create fail')