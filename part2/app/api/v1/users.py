#!/usr/bin/python3

from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

# Create namespace
api = Namespace('users', description='User operations')

# Create facade instance
facade = HBnBFacade()

# Define models for request/response documentation
user_model = api.model('User', {
    'id': fields.String(readonly=True, description='User ID'),
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'is_admin': fields.Boolean(description='Admin status'),
    'created_at': fields.DateTime(readonly=True, description='Creation timestamp'),
    'updated_at': fields.DateTime(readonly=True, description='Last update timestamp')
})

user_create_model = api.model('UserCreate', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'is_admin': fields.Boolean(description='Admin status')
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email address'),
    'is_admin': fields.Boolean(description='Admin status')
})

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        try:
            users = facade.get_all_users()
            # Remove password from response (users don't have passwords in this implementation)
            return users, 200
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

    @api.doc('create_user')
    @api.expect(user_create_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        try:
            data = request.get_json()
            if not data:
                api.abort(400, "No data provided")
            
            # Validate required fields
            required_fields = ['first_name', 'last_name', 'email']
            for field in required_fields:
                if field not in data:
                    api.abort(400, f"Missing required field: {field}")
            
            user = facade.create_user(data)
            return user, 201
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_model)
    def get(self, user_id):
        """Get a user by ID"""
        try:
            user = facade.get_user(user_id)
            if not user:
                api.abort(404, "User not found")
            return user, 200
        except Exception as e:
            if "not found" in str(e).lower():
                api.abort(404, str(e))
            else:
                api.abort(500, f"Internal server error: {str(e)}")

    @api.doc('update_user')
    @api.expect(user_update_model)
    @api.marshal_with(user_model)
    def put(self, user_id):
        """Update a user"""
        try:
            data = request.get_json()
            if not data:
                api.abort(400, "No data provided")
            
            user = facade.update_user(user_id, data)
            return user, 200
        except ValueError as e:
            if "not found" in str(e).lower():
                api.abort(404, str(e))
            else:
                api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")
