#!/usr/bin/python3


from flask_restx import Namespace, Resource, fields
from app.services import facade


api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place'),
})

review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating (1-5)'),
})

def review_to_dict(r):
    """Serialize a Review object to the JSON shape required by the task."""
    return {
        "id": r.id,
        "text": r.text,
        "rating": r.rating,
        "user_id": r.user.id,
        "place_id": r.place.id,
    }

@api.route('/')
class ReviewList(Resource):
    """review list"""

    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """post a review"""
        try:
            r = facade.create_review(api.payload)
            return review_to_dict(r), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """gets list of all reviews"""
        reviews = facade.get_all_reviews()
        return [review_to_dict(r) for r in reviews], 200

@api.route('/<string:review_id>')
class ReviewResource(Resource):
    """review resource"""

    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        r = facade.get_review(review_id)
        if not r:
            return {"error": "Review not found"}, 404
        return review_to_dict(r), 200

    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        try:
            r = facade.update_review(review_id, api.payload or {})
            return {"message": "Review updated successfully", **review_to_dict(r)}, 200
        except ValueError as e:
            msg = str(e)
            if "not found" in msg.lower():
                return {"error": msg}, 404
            return {"error": msg}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        try:
            facade.delete_review(review_id)
            return {"message": "Review deleted successfully"}, 200
        except ValueError as e:
            return {"error": str(e)}, 404

@api.route('/places/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    """place review list"""

    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [review_to_dict(r) for r in reviews], 200
        except ValueError as e:
            return {"error": str(e)}, 404
