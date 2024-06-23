import re
from datetime import datetime

from flask import request
from flask_restx import Resource, fields

from app import country_api
from config import Config
from modles.country import Country

"""Define the Country model for the API documentation"""
country_model = country_api.model('Country', {
    'id': fields.String(readonly=True, description='The country unique identifier'),
    'name': fields.String(required=True, description='The country name'),
    'code': fields.String(required=True, description='The country code'),
})


@country_api.route("/")
class CountryList(Resource):
    @country_api.doc("get all countries")
    def get(self):
        """Query all countries from the database"""
        countries = Country.query.all()
        result = []
        """Convert each Country object to a dictionary"""
        for country in countries:
            result.append({
                "id": country.id,
                "name": country.name,
                "code": country.code,
                "created_at": country.created_at.strftime(Config.datetime_format),
                "updated_at": country.updated_at.strftime(Config.datetime_format)
            })
        return result


@country_api.route('/<string:country_code>')
class CountriesByCode(Resource):
    @country_api.doc('get_country')
    def get(self, country_code):
        """Query the country by code from the database"""
        country = Country.query.filter_by(code=country_code).first()
        if country is None:
            country_api.abort(404, message='Country not found!')
        else:
            """Convert the Country object to a dictionary"""
            return {
                "id": country.id,
                "name": country.name,
                "code": country.code,
                "created_at": country.created_at.strftime(Config.datetime_format),
                "updated_at": country.updated_at.strftime(Config.datetime_format)
            }


@country_api.route('/<string:country_code>/cities')
class CountryCities(Resource):
    @country_api.doc('get_country_cities')
    def get(self, country_code):
        pass

