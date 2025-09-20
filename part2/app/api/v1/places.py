#!/usr/bin/python3

from flask import request
from flask_restx import Namespace, Resource
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places')
facade = HBnBFacade()

def place_to_dict(place):
    return {
        'id': getattr(place, 'id', None),
        'title': getattr(place, 'title', None),
        'description': getattr(place, 'description', None),
        'price': getattr(place, 'price', None),
        'latitude': getattr(place, 'latitude', None),
        'longitude': getattr(place, 'longitude', None),
        'owner_id': getattr(getattr(place, 'owner', None), 'id', None) or getattr(place, 'owner_id', None),
    }

@api.route('/')
class PlaceList(Resource):
    def get(self):
        try:
            places = facade.get_all_places()
            return [place_to_dict(place) for place in places], 200
        except Exception as error:
            return {'error': f'Internal server error: {str(error)}'}, 500

    @jwt_required()
    def post(self):
        try:
            current_identity = get_jwt_identity()
            data = request.get_json() or {}

            for field in ['title', 'description', 'price', 'latitude', 'longitude']:
                if field not in data:
                    return {'error': f'Missing required field: {field}'}, 400

            try:
                data['price'] = float(data['price'])
                data['latitude'] = float(data['latitude'])
                data['longitude'] = float(data['longitude'])
            except (ValueError, TypeError):
                return {'error': 'Price, latitude, and longitude must be valid numbers'}, 400

            data['owner_id'] = current_identity['id']
            place = facade.create_place(data)
            return place_to_dict(place), 201
        except ValueError as error:
            return {'error': str(error)}, 400
        except Exception as error:
            return {'error': f'Internal server error: {str(error)}'}, 500

@api.route('/<string:place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        try:
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404
            return place_to_dict(place), 200
        except Exception as error:
            return {'error': f'Internal server error: {str(error)}'}, 500

    @jwt_required()
    def put(self, place_id):
        try:
            current_identity = get_jwt_identity()
            data = request.get_json() or {}

            if 'price' in data:
                try:
                    data['price'] = float(data['price'])
                except (ValueError, TypeError):
                    return {'error': 'Price must be a valid number'}, 400
            if 'latitude' in data:
                try:
                    data['latitude'] = float(data['latitude'])
                except (ValueError, TypeError):
                    return {'error': 'Latitude must be a valid number'}, 400
            if 'longitude' in data:
                try:
                    data['longitude'] = float(data['longitude'])
                except (ValueError, TypeError):
                    return {'error': 'Longitude must be a valid number'}, 400

            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            owner_id = getattr(getattr(place, 'owner', None), 'id', None)
            is_admin = bool(current_identity.get('is_admin', False))
            if not is_admin and str(owner_id) != str(current_identity['id']):
                return {'error': 'Unauthorized action'}, 403

            updated_place = facade.update_place(place_id, data)
            return place_to_dict(updated_place), 200
        except ValueError as error:
            message = str(error)
            if 'not found' in message.lower():
                return {'error': message}, 404
            return {'error': message}, 400
        except Exception as error:
            return {'error': f'Internal server error: {str(error)}'}, 500
