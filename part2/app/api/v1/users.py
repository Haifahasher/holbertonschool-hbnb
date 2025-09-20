#!/usr/bin/python3

from flask import request
from flask_restx import Namespace, Resource
from app.services.facade import HBnBFacade
from app import bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

api = Namespace('users')
facade = HBnBFacade()

def user_to_dict(user):
    def convert_datetime(value):
        return value.isoformat() if isinstance(value, datetime) else value
    return {
        'id': getattr(user, 'id', None),
        'first_name': getattr(user, 'first_name', None),
        'last_name': getattr(user, 'last_name', None),
        'email': getattr(user, 'email', None),
        'is_admin': bool(getattr(user, 'is_admin', False)),
        'created_at': convert_datetime(getattr(user, 'created_at', None)),
        'updated_at': convert_datetime(getattr(user, 'updated_at', None)),
    }

@api.route('/')
class UserList(Resource):
    def get(self):
        try:
            users = facade.get_all_users()
            return [user_to_dict(user) for user in users], 200
        except Exception as error:
            return {'error': f'Internal server error: {str(error)}'}, 500

    @jwt_required()
    def post(self):
        try:
            current_identity = get_jwt_identity()
            if not current_identity.get('is_admin'):
                return {'error': 'Admin privileges required'}, 403

            data = request.get_json() or {}
            for field in ['first_name', 'last_name', 'email', 'password']:
                if field not in data:
                    return {'error': f'Missing required field: {field}'}, 400

            if facade.get_user_by_email(data['email']):
                return {'error': 'Email already registered'}, 400

            data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            user = facade.create_user(data)
            return {'id': user.id, 'message': 'User registered successfully'}, 201
        except ValueError as error:
            return {'error': str(error)}, 400
        except Exception as error:
            return {'error': f'Internal server error: {str(error)}'}, 500

@api.route('/<string:user_id>')
class UserResource(Resource):
    def get(self, user_id):
        try:
            user = facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404
            return user_to_dict(user), 200
        except Exception as error:
            return {'error': f'Internal server error: {str(error)}'}, 500

    @jwt_required()
    def put(self, user_id):
        try:
            current_identity = get_jwt_identity()
            data = request.get_json() or {}

            if current_identity.get('is_admin'):
                new_email = data.get('email')
                if new_email:
                    existing_user = facade.get_user_by_email(new_email)
                    if existing_user and str(existing_user.id) != str(user_id):
                        return {'error': 'Email already in use'}, 400
                user = facade.update_user(user_id, data)
                return user_to_dict(user), 200

            if str(user_id) != str(current_identity['id']):
                return {'error': 'Unauthorized action'}, 403
            if 'email' in data or 'password' in data:
                return {'error': 'You cannot modify email or password'}, 400

            user = facade.update_user(user_id, data)
            return user_to_dict(user), 200
        except ValueError as error:
            message = str(error)
            if 'not found' in message.lower():
                return {'error': message}, 404
            return {'error': message}, 400
        except Exception as error:
            return {'error': f'Internal server error: {str(error)}'}, 500
