#!/usr/bin/python3

from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

api = Namespace('auth')
facade = HBnBFacade()

@api.route('/login')
class Login(Resource):
    def post(self):
        payload = request.get_json() or {}
        email = payload.get('email')
        password = payload.get('password')
        if not email or not password:
            return {'error': 'Email and password are required'}, 400

        user = facade.get_user_by_email(email)
        if not user or not user.verify_password(password):
            return {'error': 'Invalid credentials'}, 401

        token = create_access_token(identity={'id': str(user.id), 'is_admin': bool(user.is_admin)})
        return {'access_token': token}, 200

@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_identity = get_jwt_identity()
        return {'message': f'Hello, user {current_identity["id"]}'}, 200
