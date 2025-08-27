#!/usr/bin/python3


from app.models.BaseModel import BaseModel


class Amenity(BaseModel):
    """Amenity Class"""

    def __init__(self, name):
        """init"""
        super().__init__()
        
        if not name or len(name) > 50:
            raise ValueError("Please make sure its 50 characters or less.")
        
        self.name = name
