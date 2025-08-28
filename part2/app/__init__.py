#!/usr/bin/python3


from flask import Flask
from flask_restx import Api

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Import and register API namespaces
    from app.api.v1.users import api as users_api
    from app.api.v1.amenities import api as amenities_api
    from app.api.v1.places import api as places_api

    # Add namespaces to the API
    api.add_namespace(users_api, path='/api/v1/users')
    api.add_namespace(amenities_api, path='/api/v1/amenities')
    api.add_namespace(places_api, path='/api/v1/places')

    return app
