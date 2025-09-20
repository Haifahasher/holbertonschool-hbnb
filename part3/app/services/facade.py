#!/usr/bin/python3

from app.persistence.repository import InMemoryRepository
from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # User operations
    def create_user(self, user_data):
        """Create a new user"""
        try:
            # Check if email already exists
            if self.user_repo.email_exists(user_data['email']):
                raise ValueError("Email already exists")
            
            user = User(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                password=user_data.get('password'),
                is_admin=user_data.get('is_admin', False)
            )
            self.user_repo.add(user)
            return user
        except Exception as e:
            raise ValueError(f"Failed to create user: {str(e)}")

    def get_user(self, user_id):
        """Get user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Get user by email"""
        return self.user_repo.get_by_email(email)

    def get_all_users(self):
        """Get all users"""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update user information"""
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        
        try:
            # Check email uniqueness if email is being updated
            if 'email' in user_data and user_data['email'] != user.email:
                if self.user_repo.email_exists(user_data['email']):
                    raise ValueError("Email already exists")
            
            # Update user attributes
            if 'first_name' in user_data:
                user.first_name = user_data['first_name']
            if 'last_name' in user_data:
                user.last_name = user_data['last_name']
            if 'email' in user_data:
                user.email = user_data['email'].lower()
            if 'is_admin' in user_data:
                user.is_admin = user_data['is_admin']
            if 'password' in user_data:
                user.set_password(user_data['password'])
            
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
            # Verify the owner exists
            owner = self.get_user(place_data['owner_id'])
            if not owner:
                raise ValueError("Owner not found")
            
            place = Place(
                title=place_data['title'],
                description=place_data['description'],
                price=place_data['price'],
                latitude=place_data['latitude'],
                longitude=place_data['longitude'],
                owner_id=place_data['owner_id']
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
            # Verify owner exists if owner_id is being updated
            if 'owner_id' in place_data:
                owner = self.get_user(place_data['owner_id'])
                if not owner:
                    raise ValueError("Owner not found")
                place.owner_id = place_data['owner_id']
            
            # Update other attributes
            if 'title' in place_data:
                place.title = place_data['title']
            if 'description' in place_data:
                place.description = place_data['description']
            if 'price' in place_data:
                place.price = place_data['price']
            if 'latitude' in place_data:
                place.latitude = place_data['latitude']
            if 'longitude' in place_data:
                place.longitude = place_data['longitude']
            
            place.save()
            return place
        except Exception as e:
            raise ValueError(f"Failed to update place: {str(e)}")

    # Review operations
    def create_review(self, review_data):
        """Create a new review"""
        try:
            # Verify place and user exist
            place = self.get_place(review_data['place_id'])
            if not place:
                raise ValueError("Place not found")
            
            user = self.get_user(review_data['user_id'])
            if not user:
                raise ValueError("User not found")
            
            # Check if user already reviewed this place
            existing_review = self.review_repo.get_by_place_and_user(
                review_data['place_id'], review_data['user_id']
            )
            if existing_review:
                raise ValueError("User has already reviewed this place")
            
            review = Review(
                text=review_data['text'],
                rating=review_data['rating'],
                place_id=review_data['place_id'],
                user_id=review_data['user_id']
            )
            self.review_repo.add(review)
            return review
        except Exception as e:
            raise ValueError(f"Failed to create review: {str(e)}")

    def get_review(self, review_id):
        """Get review by ID"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Get all reviews"""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a place"""
        return self.review_repo.get_by_place(place_id)

    def get_reviews_by_user(self, user_id):
        """Get all reviews by a user"""
        return self.review_repo.get_by_user(user_id)

    def update_review(self, review_id, review_data):
        """Update review information"""
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")
        
        try:
            if 'text' in review_data:
                review.text = review_data['text']
            if 'rating' in review_data:
                review.rating = review_data['rating']
            
            review.save()
            return review
        except Exception as e:
            raise ValueError(f"Failed to update review: {str(e)}")

    def delete_review(self, review_id):
        """Delete a review"""
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")
        
        self.review_repo.delete(review_id)
        return True
