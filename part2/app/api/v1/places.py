#!/usr/bin/python3

from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

# Create namespace
api = Namespace('places', description='Place operations')

# Create facade instance
facade = HBnBFacade()

# Define models for request/response documentation
place_model = api.model('Place', {
    'id': fields.String(readonly=True, description='Place ID'),
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Place price'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'owner_id': fields.String(description='Owner user ID'),
    'owner': fields.Nested(api.model('Owner', {
        'id': fields.String(description='Owner ID'),
        'first_name': fields.String(description='Owner first name'),
        'last_name': fields.String(description='Owner last name'),
        'email': fields.String(description='Owner email')
    }), description='Owner information'),
    'amenities': fields.List(fields.Nested(api.model('Amenity', {
        'id': fields.String(description='Amenity ID'),
        'name': fields.String(description='Amenity name')
    })), description='List of amenities'),
    'created_at': fields.DateTime(readonly=True, description='Creation timestamp'),
    'updated_at': fields.DateTime(readonly=True, description='Last update timestamp')
})

place_create_model = api.model('PlaceCreate', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Place price'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'owner_id': fields.String(required=True, description='Owner user ID')
})

place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(description='Place price'),
    'latitude': fields.Float(description='Latitude'),
    'longitude': fields.Float(description='Longitude'),
    'owner_id': fields.String(description='Owner user ID')
})

@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    @api.marshal_list_with(place_model)
    def get(self):
        """List all places"""
        try:
            places = facade.get_all_places()
            return places, 200
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

    @api.doc('create_place')
    @api.expect(place_create_model)
    @api.marshal_with(place_model, code=201)
    def post(self):
        """Create a new place"""
        try:
            data = request.get_json()
            if not data:
                api.abort(400, "No data provided")
            
            # Validate required fields
            required_fields = ['title', 'description', 'price', 'latitude', 'longitude', 'owner_id']
            for field in required_fields:
                if field not in data:
                    api.abort(400, f"Missing required field: {field}")
            
            # Validate numeric fields
            try:
                data['price'] = float(data['price'])
                data['latitude'] = float(data['latitude'])
                data['longitude'] = float(data['longitude'])
            except (ValueError, TypeError):
                api.abort(400, "Price, latitude, and longitude must be valid numbers")
            
            place = facade.create_place(data)
            return place, 201
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

@api.route('/<string:place_id>')
@api.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    @api.doc('get_place')
    @api.marshal_with(place_model)
    def get(self, place_id):
        """Get a place by ID"""
        try:
            place = facade.get_place(place_id)
            if not place:
                api.abort(404, "Place not found")
            return place, 200
        except Exception as e:
            if "not found" in str(e).lower():
                api.abort(404, str(e))
            else:
                api.abort(500, f"Internal server error: {str(e)}")

    @api.doc('update_place')
    @api.expect(place_update_model)
    @api.marshal_with(place_model)
    def put(self, place_id):
        """Update a place"""
        try:
            data = request.get_json()
            if not data:
                api.abort(400, "No data provided")
            
            # Validate numeric fields if provided
            if 'price' in data:
                try:
                    data['price'] = float(data['price'])
                except (ValueError, TypeError):
                    api.abort(400, "Price must be a valid number")
            
            if 'latitude' in data:
                try:
                    data['latitude'] = float(data['latitude'])
                except (ValueError, TypeError):
                    api.abort(400, "Latitude must be a valid number")
            
            if 'longitude' in data:
                try:
                    data['longitude'] = float(data['longitude'])
                except (ValueError, TypeError):
                    api.abort(400, "Longitude must be a valid number")
            
            place = facade.update_place(place_id, data)
            return place, 200
        except ValueError as e:
            if "not found" in str(e).lower():
                api.abort(404, str(e))
            else:
                api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")
