#!/usr/bin/python3
"""
Database initialization script for HBnB project
This script creates the database and populates it with initial data
"""

import os
import sys
import sqlite3
from datetime import datetime
import bcrypt

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

def init_database():
    """Initialize the database with tables and initial data"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("✓ Tables created successfully")
        
        # Check if data already exists
        if db.session.query(User).count() > 0:
            print("Database already contains data. Skipping initial data insertion.")
            return
        
        # Create admin user
        print("Creating admin user...")
        admin_user = User(
            first_name="Admin",
            last_name="User",
            email="admin@hbnb.com",
            password="admin123",
            is_admin=True
        )
        db.session.add(admin_user)
        
        # Create regular users
        print("Creating regular users...")
        users_data = [
            ("John", "Doe", "john.doe@example.com", "password123", False),
            ("Jane", "Smith", "jane.smith@example.com", "password123", False),
            ("Bob", "Johnson", "bob.johnson@example.com", "password123", False)
        ]
        
        users = [admin_user]
        for first_name, last_name, email, password, is_admin in users_data:
            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                is_admin=is_admin
            )
            db.session.add(user)
            users.append(user)
        
        # Create amenities
        print("Creating amenities...")
        amenity_names = [
            "WiFi", "Pool", "Gym", "Parking", "Kitchen",
            "Air Conditioning", "Heating", "TV", "Washer", "Dryer"
        ]
        
        amenities = []
        for name in amenity_names:
            amenity = Amenity(name=name)
            db.session.add(amenity)
            amenities.append(amenity)
        
        # Create places
        print("Creating places...")
        places_data = [
            ("Beautiful Beach House", "A stunning beachfront property with ocean views and modern amenities.", 150.00, 34.0522, -118.2437, users[1]),  # John Doe
            ("Cozy Downtown Apartment", "Modern apartment in the heart of the city with easy access to public transportation.", 85.00, 40.7128, -74.0060, users[2]),  # Jane Smith
            ("Mountain Cabin Retreat", "Peaceful cabin surrounded by nature, perfect for a quiet getaway.", 120.00, 39.7392, -104.9903, users[1]),  # John Doe
            ("Luxury Penthouse", "High-end penthouse with panoramic city views and premium amenities.", 300.00, 41.8781, -87.6298, users[3])  # Bob Johnson
        ]
        
        places = []
        for title, description, price, latitude, longitude, owner in places_data:
            place = Place(
                title=title,
                description=description,
                price=price,
                latitude=latitude,
                longitude=longitude,
                owner_id=owner.id
            )
            db.session.add(place)
            places.append(place)
        
        # Create reviews
        print("Creating reviews...")
        reviews_data = [
            ("Amazing beach house with incredible ocean views! The property was clean and well-maintained.", 5, places[0], users[2]),  # Jane reviews Beach House
            ("Great location in downtown. The apartment was modern and comfortable.", 4, places[1], users[1]),  # John reviews Downtown Apartment
            ("Perfect for a quiet retreat. The cabin was cozy and had everything we needed.", 5, places[2], users[3]),  # Bob reviews Mountain Cabin
            ("Luxury at its finest! The penthouse exceeded all expectations.", 5, places[3], users[1]),  # John reviews Luxury Penthouse
            ("Good value for money. The apartment was clean and well-equipped.", 4, places[1], users[3])  # Bob reviews Downtown Apartment
        ]
        
        for text, rating, place, user in reviews_data:
            review = Review(
                text=text,
                rating=rating,
                place_id=place.id,
                user_id=user.id
            )
            db.session.add(review)
        
        # Add amenities to places
        print("Adding amenities to places...")
        place_amenities = [
            # Beach House amenities
            (places[0], [amenities[0], amenities[1], amenities[3], amenities[4], amenities[5], amenities[7]]),  # WiFi, Pool, Parking, Kitchen, AC, TV
            # Downtown Apartment amenities
            (places[1], [amenities[0], amenities[3], amenities[4], amenities[5], amenities[6], amenities[7]]),  # WiFi, Parking, Kitchen, AC, Heating, TV
            # Mountain Cabin amenities
            (places[2], [amenities[0], amenities[3], amenities[4], amenities[6], amenities[7], amenities[8], amenities[9]]),  # WiFi, Parking, Kitchen, Heating, TV, Washer, Dryer
            # Luxury Penthouse amenities
            (places[3], [amenities[0], amenities[1], amenities[2], amenities[3], amenities[4], amenities[5], amenities[6], amenities[7], amenities[8], amenities[9]])  # All amenities
        ]
        
        for place, place_amenities_list in place_amenities:
            for amenity in place_amenities_list:
                place.amenities.append(amenity)
        
        # Commit all changes
        print("Committing changes to database...")
        db.session.commit()
        print("✓ Database initialized successfully!")
        
        # Display summary
        print("\n=== DATABASE SUMMARY ===")
        print(f"Users: {db.session.query(User).count()}")
        print(f"Places: {db.session.query(Place).count()}")
        print(f"Reviews: {db.session.query(Review).count()}")
        print(f"Amenities: {db.session.query(Amenity).count()}")
        
        # Display some sample data
        print("\n=== SAMPLE DATA ===")
        print("Users:")
        for user in db.session.query(User).limit(3):
            print(f"  - {user.first_name} {user.last_name} ({user.email}) - Admin: {user.is_admin}")
        
        print("\nPlaces:")
        for place in db.session.query(Place).limit(3):
            print(f"  - {place.title} - ${place.price} - Owner: {place.owner.first_name} {place.owner.last_name}")
        
        print("\nAmenities:")
        for amenity in db.session.query(Amenity).limit(5):
            print(f"  - {amenity.name}")

if __name__ == "__main__":
    init_database()
