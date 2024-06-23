import re
from datetime import datetime

from flask import request
from flask_restx import Resource, fields

from app import city_api, db, country_api
from config import Config
from models.city import City
from models.country import Country

city_model = city_api.model('City', {
    'name': fields.String(required=True, description='The city name'),
    'country_id': fields.String(required=True, description='The country identifier')
})

@city_api.route("/")
class CityList(Resource):
    @city_api.doc("get all cities")
    def get(self):
        """Query all cities from the database"""
        cities = City.query.all()
        result = []
        """Convert each City object to a dictionary"""
        for city in cities:
            result.append({
                "id": city.id,
                "name": city.name,
                "country_id": city.country_id,
                "country_code": city.country.code,
                "created_at": city.created_at.strftime(Config.datetime_format),
                "updated_at": city.updated_at.strftime(Config.datetime_format)
            })
        return result

@city_api.route('/<string:city_id>')
class CityById(Resource):
    @city_api.doc('get_city')
    def get(self, city_id):
        """Query the city by ID from the database"""
        city = City.query.filter_by(id=city_id).first()
        if city is None:
            city_api.abort(400, message='City not found!')
        else:
            """Convert the City object to a dictionary"""
            return {
                "id": city.id,
                "name": city.name,
                "country_id": city.country_id,
                "country_code": city.country_code,
                "created_at": city.created_at.strftime(Config.datetime_format),
                "updated_at": city.updated_at.strftime(Config.datetime_format)
            }

    @city_api.doc('create a new city')
    @city_api.expect(city_model)
    @city_api.response(201, 'City created successfully')
    @city_api.response(400, 'Invalid input')
    @city_api.response(404, 'Country not found')
    def post(self):
        """Create a new city"""
        data = request.get_json()
        if not data.get('name') or not data.get('country_id'):
            city_api.abort(400, message='Invalid input')

        country = Country.query.filter_by(id=data['country_id']).first()
        if not country:
            city_api.abort(404, message='Country not found')
        try:
            new_city = City(
                name=data['name'],
                country_id=data['country_id'])
            db.session.add(new_city)
            db.session.commit()

            return {
                "id": new_city.id,
                "name": new_city.name,
                "country_id": new_city.country_id,
                "country_code": new_city.country.code,
                "created_at": new_city.created_at.strftime(Config.datetime_format),
                "updated_at": new_city.updated_at.strftime(Config.datetime_format)
            }, 201

        except Exception as e:
            db.session.rollback()


@city_api.route('/city/<string:city_id>')
class CityById(Resource):
    @city_api.doc('get_city')
    def get(self, city_id):
        """Query the city by ID from the database"""
        city = City.query.filter_by(id=city_id).first()
        if city is None:
            city_api.abort(400, message='City not found!')
        else:
            """Convert the City object to a dictionary"""
            return {
                "id": city.id,
                "name": city.name,
                "country_id": city.country_id,
                "country_code": city.country_code,
                "created_at": city.created_at.strftime(Config.datetime_format),
                "updated_at": city.updated_at.strftime(Config.datetime_format)
            }

    @city_api.expect(city_model)
    def put(self, city_id):
        data = request.get_json()
        if not data:
            city_api.abort(400, "Invalid input")

        city = City.query.filter_by(id=city_id).first()
        if not city:
            city_api.abort(404, 'City not found')

        if 'name' in data:
            city.name = data['name']
        if 'country_id' in data:
            country = Country.query.filter_by(id=data['country_id']).first()
            if not country:
                city_api.abort(409, 'Country not found')
            city.country_id = data['country_id']

        city.updated_at = datetime.now()
        db.session.commit()

        return {
            "id": city.id,
            "name": city.name,
            "country_id": city.country_id,
            "country_code": city.country.code,
            "created_at": city.created_at.strftime(Config.datetime_format),
            "updated_at": city.updated_at.strftime(Config.datetime_format)
        }

    @city_api.doc('Delete a specific city')
    def delete(self, city_id):
        city = City.query.filter_by(id=city_id).first()
        if city is None:
            return city_api.abort(404, 'User not found')
        try:
            db.session.delete(city)
            db.session.commit()
            return "delete successfully", 200
        except Exception as e:
            db.session.rollback()
            city_api.abort(404, message='Create fail')