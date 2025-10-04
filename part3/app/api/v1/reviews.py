#!/usr/bin/python3

from flask import request
from flask_restx import Namespace, Resource
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews')
facade = HBnBFacade()

def review_to_dict(review):
    return {
        'id': getattr(review, 'id', None),
        'title': getattr(review, 'title', None),
        'comment': getattr(review, 'comment', None),
        'rating': getattr(review, 'rating', None),
        'place_id': getattr(review, 'place_id', None),
        'user_id': getattr(review, 'user_id', None),
        'created_at': getattr(review, 'created_at', None),
        'updated_at': getattr(review, 'updated_at', None),
    }

@api.route('/')
class ReviewList(Resource):
    def get(self):
        try:
            reviews = facade.get_all_reviews()
            return [review_to_dict(review) for review in reviews], 200
        except Exception as error:
            return {'error': f'Internal server error: {str(error)}'}, 500

    @jwt_required()
    def post(self):
        try:
            current_identity = get_jwt_identity()
            data = request.get_json() or {}

            for field in ['title', 'comment', 'rating', 'place_id']:
                if field not in data:
                    return {'error': f'Missing required field: {field}'}, 400

            try:
                data['rating'] = int(data['rating'])
                if data['rating'] < 1 or data['rating'] > 5:
                    return {'error': 'Rating must be between 1 and 5'}, 400
            except (ValueError, TypeError):
                return {'error': 'Rating must be a valid integer'}, 400

            # Check if place exists
            place = facade.get_place(data['place_id'])
            if not place:
                return {'error': 'Place not found'}, 404

            # Check if user already reviewed this place
            existing_review = facade.get_review_by_user_and_place(current_identity['id'], data['place_id'])
            if existing_review:
                return {'error': 'You have already reviewed this place'}, 400

            data['user_id'] = current_identity['id']
            review = facade.create_review(data)
            return review_to_dict(review), 201
        except ValueError as error:
            return {'error': str(error)}, 400
        except Exception as error:
            return {'error': f'Internal server error: {str(error)}'}, 500

@api.route('/<string:review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        try:
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Review not found'}, 404
            return review_to_dict(review), 200
        except Exception as error:
            return {'error': f'Internal server error: {str(error)}'}, 500

    @jwt_required()
    def put(self, review_id):
        try:
            current_identity = get_jwt_identity()
            data = request.get_json() or {}

            if 'rating' in data:
                try:
                    data['rating'] = int(data['rating'])
                    if data['rating'] < 1 or data['rating'] > 5:
                        return {'error': 'Rating must be between 1 and 5'}, 400
                except (ValueError, TypeError):
                    return {'error': 'Rating must be a valid integer'}, 400

            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Review not found'}, 404

            # Check if user owns this review or is admin
            is_admin = bool(current_identity.get('is_admin', False))
            if not is_admin and str(review.user_id) != str(current_identity['id']):
                return {'error': 'Unauthorized action'}, 403

            updated_review = facade.update_review(review_id, data)
            return review_to_dict(updated_review), 200
        except ValueError as error:
            message = str(error)
            if 'not found' in message.lower():
                return {'error': message}, 404
            return {'error': message}, 400
        except Exception as error:
            return {'error': f'Internal server error: {str(error)}'}, 500

    @jwt_required()
    def delete(self, review_id):
        try:
            current_identity = get_jwt_identity()
            
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Review not found'}, 404

            # Check if user owns this review or is admin
            is_admin = bool(current_identity.get('is_admin', False))
            if not is_admin and str(review.user_id) != str(current_identity['id']):
                return {'error': 'Unauthorized action'}, 403

            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except Exception as error:
            return {'error': f'Internal server error: {str(error)}'}, 500
