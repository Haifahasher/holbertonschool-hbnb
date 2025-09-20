#!/usr/bin/python3


from app.models.BaseModel import BaseModel
from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Review(BaseModel):
    """Review class"""
    __tablename__ = 'reviews'

    text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    place_id = Column(String(36), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)

    # Relationships
    place = relationship("Place", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

    def __init__(self, text, rating, place_id=None, user_id=None, **kwargs):
        """Initialize review with validation"""
        super().__init__(**kwargs)

        if not isinstance(text, str) or not text or not text.strip():
            raise ValueError("Are we rating without reasons now..")
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("choose from 1-5 only")

        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id
