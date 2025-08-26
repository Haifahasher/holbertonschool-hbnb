#!/usr/bin/python3


from app.models.base_model import BaseModel


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        if not (price >= 0):
            raise ValueError("Are you really selling it for a negative price?"
        if not (-90 <= latitude <= 90):
            raise ValueError("Please enter a valid latitude")
        if not (-180 <= longitude <= 180):
            raise ValueError("Please enter a valid longitude")
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        """add review to place"""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """add amenity to place."""
        self.amenities.append(amenity)
