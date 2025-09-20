#!/usr/bin/python3


from app.models.BaseModel import BaseModel
from sqlalchemy import Column, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship

class Place(BaseModel):
    """Place model"""
    __tablename__ = 'places'

    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    owner_id = Column(String(36), ForeignKey('users.id'), nullable=False)

    # Relationships
    owner = relationship("User", back_populates="places")
    reviews = relationship("Review", back_populates="place", cascade="all, delete-orphan")
    # amenities = relationship("Amenity", secondary="place_amenities", back_populates="places")

    def __init__(self, title, description, price, latitude, longitude, owner_id=None, **kwargs):
        """Initialize place with validation"""
        super().__init__(**kwargs)
        
        if not title or len(title) > 100:
            raise ValueError("Maximum Characters Reached. Try Below a 100")
        if price < 0:
            raise ValueError("Are you really selling it for a negative price?")
        if price == 0:
            raise ValueError("Umm, Free Housing isn't allowed here.. Sorry")
        if not (-90 <= latitude <= 90):
            raise ValueError("Please enter a valid latitude")
        if not (-180 <= longitude <= 180):
            raise ValueError("Please enter a valid longitude")
        
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

    @property
    def owner_id_prop(self):
        """Get the owner ID for API responses"""
        return self.owner_id

    def to_dict(self):
        """Override to_dict to include owner_id"""
        result = super().to_dict()
        result['owner_id'] = self.owner_id
        return result
