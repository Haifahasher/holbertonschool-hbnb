#!/usr/bin/python3


from app.persistence.repository import SQLAlchemyRepository
from app.models.amenity import Amenity

class AmenityRepository(SQLAlchemyRepository):
    """Amenity-specific repository with additional methods"""
    
    def __init__(self):
        super().__init__(Amenity)
    
    def get_by_name(self, name):
        """Get amenity by name"""
        return self.get_by_attribute('name', name)
    
    def name_exists(self, name):
        """Check if amenity name already exists"""
        return self.get_by_name(name) is not None
