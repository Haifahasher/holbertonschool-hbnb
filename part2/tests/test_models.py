#!/usr/bin/python3
"""
Unit tests for all models
"""
import unittest
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class TestUserModel(unittest.TestCase):
    """Test cases for User model"""

    def setUp(self):
        """Set up test fixtures"""
        self.valid_user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com'
        }

    def test_valid_user_creation(self):
        """Test creating a user with valid data"""
        user = User(**self.valid_user_data)
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'john.doe@example.com')
        self.assertFalse(user.is_admin)
        self.assertIsNotNone(user.id)
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)

    def test_user_with_admin_flag(self):
        """Test creating a user with admin flag"""
        user_data = self.valid_user_data.copy()
        user_data['is_admin'] = True
        user = User(**user_data)
        self.assertTrue(user.is_admin)

    def test_empty_first_name_validation(self):
        """Test validation for empty first name"""
        user_data = self.valid_user_data.copy()
        user_data['first_name'] = ""
        with self.assertRaises(ValueError):
            User(**user_data)

    def test_empty_last_name_validation(self):
        """Test validation for empty last name"""
        user_data = self.valid_user_data.copy()
        user_data['last_name'] = ""
        with self.assertRaises(ValueError):
            User(**user_data)

    def test_long_first_name_validation(self):
        """Test validation for first name exceeding 50 characters"""
        user_data = self.valid_user_data.copy()
        user_data['first_name'] = "A" * 51
        with self.assertRaises(ValueError):
            User(**user_data)

    def test_long_last_name_validation(self):
        """Test validation for last name exceeding 50 characters"""
        user_data = self.valid_user_data.copy()
        user_data['last_name'] = "B" * 51
        with self.assertRaises(ValueError):
            User(**user_data)

    def test_invalid_email_format(self):
        """Test validation for invalid email format"""
        invalid_emails = [
            "invalid-email",
            "test@",
            "@example.com",
            "test..test@example.com",
            "test@.com"
        ]
        for email in invalid_emails:
            user_data = self.valid_user_data.copy()
            user_data['email'] = email
            with self.assertRaises(ValueError):
                User(**user_data)

    def test_valid_email_formats(self):
        """Test validation for valid email formats"""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org",
            "123@numbers.com"
        ]
        for email in valid_emails:
            user_data = self.valid_user_data.copy()
            user_data['email'] = email
            try:
                user = User(**user_data)
                self.assertEqual(user.email, email.lower())
            except ValueError:
                self.fail(f"Valid email {email} failed validation")

    def test_user_to_dict(self):
        """Test user serialization to dictionary"""
        user = User(**self.valid_user_data)
        user_dict = user.to_dict()
        self.assertIn('id', user_dict)
        self.assertIn('first_name', user_dict)
        self.assertIn('last_name', user_dict)
        self.assertIn('email', user_dict)
        self.assertIn('is_admin', user_dict)
        self.assertIn('created_at', user_dict)
        self.assertIn('updated_at', user_dict)

    def test_user_update(self):
        """Test updating user attributes"""
        user = User(**self.valid_user_data)
        original_updated_at = user.updated_at
        
        user.update({'first_name': 'Jane'})
        self.assertEqual(user.first_name, 'Jane')
        self.assertGreater(user.updated_at, original_updated_at)


class TestPlaceModel(unittest.TestCase):
    """Test cases for Place model"""

    def setUp(self):
        """Set up test fixtures"""
        self.owner = User('Owner', 'User', 'owner@example.com')
        self.valid_place_data = {
            'title': 'Beautiful Apartment',
            'description': 'A lovely place to stay',
            'price': 150.0,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'owner': self.owner
        }

    def test_valid_place_creation(self):
        """Test creating a place with valid data"""
        place = Place(**self.valid_place_data)
        self.assertEqual(place.title, 'Beautiful Apartment')
        self.assertEqual(place.description, 'A lovely place to stay')
        self.assertEqual(place.price, 150.0)
        self.assertEqual(place.latitude, 40.7128)
        self.assertEqual(place.longitude, -74.0060)
        self.assertEqual(place.owner, self.owner)

    def test_empty_title_validation(self):
        """Test validation for empty title"""
        place_data = self.valid_place_data.copy()
        place_data['title'] = ""
        with self.assertRaises(ValueError):
            Place(**place_data)

    def test_long_title_validation(self):
        """Test validation for title exceeding 100 characters"""
        place_data = self.valid_place_data.copy()
        place_data['title'] = "A" * 101
        with self.assertRaises(ValueError):
            Place(**place_data)

    def test_negative_price_validation(self):
        """Test validation for negative price"""
        place_data = self.valid_place_data.copy()
        place_data['price'] = -50.0
        with self.assertRaises(ValueError):
            Place(**place_data)

    def test_zero_price_validation(self):
        """Test validation for zero price"""
        place_data = self.valid_place_data.copy()
        place_data['price'] = 0
        with self.assertRaises(ValueError):
            Place(**place_data)

    def test_invalid_latitude_validation(self):
        """Test validation for invalid latitude values"""
        invalid_latitudes = [-91, 91, 100, -100]
        for lat in invalid_latitudes:
            place_data = self.valid_place_data.copy()
            place_data['latitude'] = lat
            with self.assertRaises(ValueError):
                Place(**place_data)

    def test_valid_latitude_boundaries(self):
        """Test validation for valid latitude boundary values"""
        valid_latitudes = [-90, -45, 0, 45, 90]
        for lat in valid_latitudes:
            place_data = self.valid_place_data.copy()
            place_data['latitude'] = lat
            try:
                place = Place(**place_data)
                self.assertEqual(place.latitude, lat)
            except ValueError:
                self.fail(f"Valid latitude {lat} failed validation")

    def test_invalid_longitude_validation(self):
        """Test validation for invalid longitude values"""
        invalid_longitudes = [-181, 181, 200, -200]
        for lon in invalid_longitudes:
            place_data = self.valid_place_data.copy()
            place_data['longitude'] = lon
            with self.assertRaises(ValueError):
                Place(**place_data)

    def test_valid_longitude_boundaries(self):
        """Test validation for valid longitude boundary values"""
        valid_longitudes = [-180, -90, 0, 90, 180]
        for lon in valid_longitudes:
            place_data = self.valid_place_data.copy()
            place_data['longitude'] = lon
            try:
                place = Place(**place_data)
                self.assertEqual(place.longitude, lon)
            except ValueError:
                self.fail(f"Valid longitude {lon} failed validation")

    def test_invalid_owner_validation(self):
        """Test validation for invalid owner type"""
        place_data = self.valid_place_data.copy()
        place_data['owner'] = "not_a_user"
        with self.assertRaises(ValueError):
            Place(**place_data)

    def test_place_to_dict(self):
        """Test place serialization to dictionary"""
        place = Place(**self.valid_place_data)
        place_dict = place.to_dict()
        self.assertIn('owner_id', place_dict)
        self.assertEqual(place_dict['owner_id'], self.owner.id)

    def test_add_remove_review(self):
        """Test adding and removing reviews"""
        place = Place(**self.valid_place_data)
        review = Review("Great place!", 5, place, self.owner)
        
        place.add_review(review)
        self.assertIn(review, place.reviews)
        
        place.remove_review(review)
        self.assertNotIn(review, place.reviews)

    def test_add_remove_amenity(self):
        """Test adding and removing amenities"""
        place = Place(**self.valid_place_data)
        amenity = Amenity("WiFi")
        
        place.add_amenity(amenity)
        self.assertIn(amenity, place.amenities)
        
        place.remove_amenity(amenity)
        self.assertNotIn(amenity, place.amenities)


class TestReviewModel(unittest.TestCase):
    """Test cases for Review model"""

    def setUp(self):
        """Set up test fixtures"""
        self.owner = User('Owner', 'User', 'owner@example.com')
        self.place = Place('Test Place', 'Test Description', 100.0, 0, 0, self.owner)
        self.user = User('Reviewer', 'User', 'reviewer@example.com')
        self.valid_review_data = {
            'text': 'This is a great place!',
            'rating': 5,
            'place': self.place,
            'user': self.user
        }

    def test_valid_review_creation(self):
        """Test creating a review with valid data"""
        review = Review(**self.valid_review_data)
        self.assertEqual(review.text, 'This is a great place!')
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.place, self.place)
        self.assertEqual(review.user, self.user)

    def test_empty_text_validation(self):
        """Test validation for empty text"""
        review_data = self.valid_review_data.copy()
        review_data['text'] = ""
        with self.assertRaises(ValueError):
            Review(**review_data)

    def test_whitespace_only_text_validation(self):
        """Test validation for whitespace-only text"""
        review_data = self.valid_review_data.copy()
        review_data['text'] = "   "
        with self.assertRaises(ValueError):
            Review(**review_data)

    def test_invalid_rating_validation(self):
        """Test validation for invalid rating values"""
        invalid_ratings = [0, 6, -1, 10, 3.5]
        for rating in invalid_ratings:
            review_data = self.valid_review_data.copy()
            review_data['rating'] = rating
            with self.assertRaises(ValueError):
                Review(**review_data)

    def test_valid_rating_boundaries(self):
        """Test validation for valid rating boundary values"""
        valid_ratings = [1, 2, 3, 4, 5]
        for rating in valid_ratings:
            review_data = self.valid_review_data.copy()
            review_data['rating'] = rating
            try:
                review = Review(**review_data)
                self.assertEqual(review.rating, rating)
            except ValueError:
                self.fail(f"Valid rating {rating} failed validation")

    def test_invalid_place_validation(self):
        """Test validation for invalid place type"""
        review_data = self.valid_review_data.copy()
        review_data['place'] = "not_a_place"
        with self.assertRaises(TypeError):
            Review(**review_data)

    def test_invalid_user_validation(self):
        """Test validation for invalid user type"""
        review_data = self.valid_review_data.copy()
        review_data['user'] = "not_a_user"
        with self.assertRaises(TypeError):
            Review(**review_data)

    def test_review_to_dict(self):
        """Test review serialization to dictionary"""
        review = Review(**self.valid_review_data)
        review_dict = review.to_dict()
        self.assertIn('text', review_dict)
        self.assertIn('rating', review_dict)
        self.assertIn('place', review_dict)
        self.assertIn('user', review_dict)


class TestAmenityModel(unittest.TestCase):
    """Test cases for Amenity model"""

    def setUp(self):
        """Set up test fixtures"""
        self.valid_amenity_data = {'name': 'WiFi'}

    def test_valid_amenity_creation(self):
        """Test creating an amenity with valid data"""
        amenity = Amenity(**self.valid_amenity_data)
        self.assertEqual(amenity.name, 'WiFi')
        self.assertIsNotNone(amenity.id)
        self.assertIsNotNone(amenity.created_at)
        self.assertIsNotNone(amenity.updated_at)

    def test_empty_name_validation(self):
        """Test validation for empty name"""
        amenity_data = self.valid_amenity_data.copy()
        amenity_data['name'] = ""
        with self.assertRaises(ValueError):
            Amenity(**amenity_data)

    def test_long_name_validation(self):
        """Test validation for name exceeding 50 characters"""
        amenity_data = self.valid_amenity_data.copy()
        amenity_data['name'] = "A" * 51
        with self.assertRaises(ValueError):
            Amenity(**amenity_data)

    def test_amenity_to_dict(self):
        """Test amenity serialization to dictionary"""
        amenity = Amenity(**self.valid_amenity_data)
        amenity_dict = amenity.to_dict()
        self.assertIn('name', amenity_dict)
        self.assertEqual(amenity_dict['name'], 'WiFi')


if __name__ == '__main__':
    unittest.main()
