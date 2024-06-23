import re
from datetime import datetime

from flask import request
from flask_restx import Resource, fields

from app import country_api
from config import Config
from modles.country import Country


country_model = country_api.model('Country', {
    'id': fields.String(readonly=True, description='The country unique identifier'),
    'name': fields.String(required=True, description='The country name'),
    'code': fields.String(required=True, description='The country code'),
})


@country_api.route("/")
class CountryList(Resource):
    @country_api.doc("get all countries")
    def get(self):
        countries = Country.query.all()
        result = []
        for country in countries:
            result.append({
                "id": country.id,
                "name": country.name,
                "code": country.code,
                "created_at": country.created_at.strftime,
                "updated_at": country.updated_at.strftime
            })
        return result


@country_api.route('/<string:country_code>')
class CountriesByCode(Resource):
    @country_api.doc('get_country')
    def get(self, country_code):
        country = Country.query.filter_by(code=country_code).first()
        if country is None:
            country_api.abort(404, message='Country not found!')
        else:
            return {
                "id": country.id,
                "name": country.name,
                "code": country.code,
                "created_at": country.created_at.strftime,
                "updated_at": country.updated_at.strftime
            }


@country_api.route('/<string:country_code>/cities')
class CountryCities(Resource):
    @country_api.doc('get_country_cities')
    def get(self, country_code):
        pass

