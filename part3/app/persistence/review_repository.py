#!/usr/bin/python3


from app.persistence.repository import SQLAlchemyRepository
from app.models.review import Review

class ReviewRepository(SQLAlchemyRepository):
    """Review-specific repository with additional methods"""
    
    def __init__(self):
        super().__init__(Review)
    
    def get_by_place(self, place_id):
        """Get all reviews for a specific place"""
        return self.model.query.filter_by(place_id=place_id).all()
    
    def get_by_user(self, user_id):
        """Get all reviews by a specific user"""
        return self.model.query.filter_by(user_id=user_id).all()
    
    def get_by_place_and_user(self, place_id, user_id):
        """Get review by specific user for specific place"""
        return self.model.query.filter_by(place_id=place_id, user_id=user_id).first()
    
    def get_average_rating(self, place_id):
        """Get average rating for a place"""
        from sqlalchemy import func
        result = self.model.query.filter_by(place_id=place_id).with_entities(
            func.avg(Review.rating)
        ).scalar()
        return round(result, 2) if result else 0
