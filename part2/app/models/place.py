#!/usr/bin/python3


from app.models.BaseModel import BaseModel
from app.models.user import User

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        if not title or len(title) > 100:
            raise ValueError("Maximum Characters Reached. Try Below a 100")
        if (price < 0):
            raise ValueError("Are you really selling it for a negative price?")
        if (price == 0):
            raise ValueError("Umm, Free Housing isn't allowed here.. Sorry")
        if not (-90 <= latitude <= 90):
            raise ValueError("Please enter a valid latitude")
        if not (-180 <= longitude <= 180):
            raise ValueError("Please enter a valid longitude")
        if not isinstance(owner, User):
            raise ValueError("Owner Validation Failed!")
        
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

    @property
    def owner_id(self):
        """Get the owner ID for API responses"""
        return self.owner.id if self.owner else None

    def add_review(self, review):
        """add review to place"""
        self.reviews.append(review)

    def remove_review(self, review):
        """delete review of place"""
        self.reviews.remove(review)

    def add_amenity(self, amenity):
        """add amenity to place."""
        self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        """delete amenity of place"""
        self.amenities.remove(amenity)

    def to_dict(self):
        """Override to_dict to include owner_id and handle relationships"""
        result = super().to_dict()
        result['owner_id'] = self.owner_id
        return result
