#!/usr/bin/python3

from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

# Create namespace
api = Namespace('amenities', description='Amenity operations')

# Create facade instance
facade = HBnBFacade()

# Define models for request/response documentation
amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True, description='Amenity ID'),
    'name': fields.String(required=True, description='Amenity name'),
    'created_at': fields.DateTime(readonly=True, description='Creation timestamp'),
    'updated_at': fields.DateTime(readonly=True, description='Last update timestamp')
})

amenity_create_model = api.model('AmenityCreate', {
    'name': fields.String(required=True, description='Amenity name')
})

amenity_update_model = api.model('AmenityUpdate', {
    'name': fields.String(description='Amenity name')
})

@api.route('/')
class AmenityList(Resource):
    @api.doc('list_amenities')
    @api.marshal_list_with(amenity_model)
    def get(self):
        """List all amenities"""
        try:
            amenities = facade.get_all_amenities()
            return amenities, 200
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

    @api.doc('create_amenity')
    @api.expect(amenity_create_model)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity"""
        try:
            data = request.get_json()
            if not data:
                api.abort(400, "No data provided")
            
            # Validate required fields
            if 'name' not in data:
                api.abort(400, "Missing required field: name")
            
            amenity = facade.create_amenity(data)
            return amenity, 201
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    @api.doc('get_amenity')
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Get an amenity by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                api.abort(404, "Amenity not found")
            return amenity, 200
        except Exception as e:
            if "not found" in str(e).lower():
                api.abort(404, str(e))
            else:
                api.abort(500, f"Internal server error: {str(e)}")

    @api.doc('update_amenity')
    @api.expect(amenity_update_model)
    @api.marshal_with(amenity_model)
    def put(self, amenity_id):
        """Update an amenity"""
        try:
            data = request.get_json()
            if not data:
                api.abort(400, "No data provided")
            
            amenity = facade.update_amenity(amenity_id, data)
            return amenity, 200
        except ValueError as e:
            if "not found" in str(e).lower():
                api.abort(404, str(e))
            else:
                api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")
