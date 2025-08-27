#!/usr/bin/python3


from app.models.BaseModel import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    """Review class"""

    def __init__(self, text, rating, place, user):
        """init"""
        super().__init__()

        if not isinstance(text, str) or  not text or not text.strip():
            raise ValueError("Are we rating without reasons now..")
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("choose from 1-5 only")
        if not isinstance(place, Place):
            raise TypeError("Place Validation Failed!")
        if not isinstance(user, User):
            raise TypeError("User Validation Failed!")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
