#!/usr/bin/python3

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User operations
    def create_user(self, user_data):
        """Create a new user"""
        try:
            user = User(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                is_admin=user_data.get('is_admin', False)
            )
            self.user_repo.add(user)
            return user
        except Exception as e:
            raise ValueError(f"Failed to create user: {str(e)}")

    def get_user(self, user_id):
        """Get user by ID"""
        return self.user_repo.get(user_id)

    def get_all_users(self):
        """Get all users"""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update user information"""
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        
        try:
            # Create a new user with updated data to validate
            updated_user = User(
                first_name=user_data.get('first_name', user.first_name),
                last_name=user_data.get('last_name', user.last_name),
                email=user_data.get('email', user.email),
                is_admin=user_data.get('is_admin', user.is_admin)
            )
            
            # Update the existing user
            user.first_name = updated_user.first_name
            user.last_name = updated_user.last_name
            user.email = updated_user.email
            user.is_admin = updated_user.is_admin
            user.save()
            
            return user
        except Exception as e:
            raise ValueError(f"Failed to update user: {str(e)}")

    # Amenity operations
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        try:
            amenity = Amenity(name=amenity_data['name'])
            self.amenity_repo.add(amenity)
            return amenity
        except Exception as e:
            raise ValueError(f"Failed to create amenity: {str(e)}")

    def get_amenity(self, amenity_id):
        """Get amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update amenity information"""
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        
        try:
            # Create a new amenity with updated data to validate
            updated_amenity = Amenity(name=amenity_data['name'])
            
            # Update the existing amenity
            amenity.name = updated_amenity.name
            amenity.save()
            
            return amenity
        except Exception as e:
            raise ValueError(f"Failed to update amenity: {str(e)}")

    # Place operations
    def create_place(self, place_data):
        """Create a new place"""
        try:
            # Get the owner user
            owner = self.get_user(place_data['owner_id'])
            if not owner:
                raise ValueError("Owner not found")
            
            place = Place(
                title=place_data['title'],
                description=place_data['description'],
                price=place_data['price'],
                latitude=place_data['latitude'],
                longitude=place_data['longitude'],
                owner=owner
            )
            self.place_repo.add(place)
            return place
        except Exception as e:
            raise ValueError(f"Failed to create place: {str(e)}")

    def get_place(self, place_id):
        """Get place by ID"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Get all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update place information"""
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        
        try:
            # Get the owner user if provided
            owner = place.owner
            if 'owner_id' in place_data:
                owner = self.get_user(place_data['owner_id'])
                if not owner:
                    raise ValueError("Owner not found")
            
            # Create a new place with updated data to validate
            updated_place = Place(
                title=place_data.get('title', place.title),
                description=place_data.get('description', place.description),
                price=place_data.get('price', place.price),
                latitude=place_data.get('latitude', place.latitude),
                longitude=place_data.get('longitude', place.longitude),
                owner=owner
            )
            
            # Update the existing place
            place.title = updated_place.title
            place.description = updated_place.description
            place.price = updated_place.price
            place.latitude = updated_place.latitude
            place.longitude = updated_place.longitude
            place.owner = updated_place.owner
            place.save()
            
            return place
        except Exception as e:
            raise ValueError(f"Failed to update place: {str(e)}")
