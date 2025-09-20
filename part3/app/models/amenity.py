#!/usr/bin/python3


from app.models.BaseModel import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class Amenity(BaseModel):
    """Amenity Class"""
    __tablename__ = 'amenities'

    name = Column(String(50), nullable=False, unique=True)

    # Relationships
    # places = relationship("Place", secondary="place_amenities", back_populates="amenities")

    def __init__(self, name, **kwargs):
        """Initialize amenity with validation"""
        super().__init__(**kwargs)
        
        if not name or len(name) > 50:
            raise ValueError("Please make sure its 50 characters or less.")
        
        self.name = name
