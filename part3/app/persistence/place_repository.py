#!/usr/bin/python3


from app.persistence.repository import SQLAlchemyRepository
from app.models.place import Place

class PlaceRepository(SQLAlchemyRepository):
    """Place-specific repository with additional methods"""
    
    def __init__(self):
        super().__init__(Place)
    
    def get_by_owner(self, owner_id):
        """Get all places owned by a specific user"""
        return self.model.query.filter_by(owner_id=owner_id).all()
    
    def get_by_price_range(self, min_price, max_price):
        """Get places within a price range"""
        return self.model.query.filter(
            Place.price >= min_price,
            Place.price <= max_price
        ).all()
