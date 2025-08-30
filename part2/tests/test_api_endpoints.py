#!/usr/bin/python3
"""
API endpoint tests for all resources
"""
import unittest
import json
from app import create_app
from app.services.facade import HBnBFacade


class TestAPIEndpoints(unittest.TestCase):
    """Test cases for API endpoints"""

    def setUp(self):
        """Set up test fixtures"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.facade = HBnBFacade()

    def tearDown(self):
        """Clean up after tests"""
        pass

    def test_swagger_documentation_accessible(self):
        """Test that Swagger documentation is accessible"""
        response = self.client.get('/api/v1/')
        self.assertEqual(response.status_code, 200)
        # Check if it's HTML (Swagger UI)
        self.assertIn('text/html', response.content_type)

    def test_api_namespace_accessible(self):
        """Test that API namespace is accessible"""
        response = self.client.get('/api/v1/')
        self.assertEqual(response.status_code, 200)


class TestUserEndpoints(unittest.TestCase):
    """Test cases for User endpoints"""

    def setUp(self):
        """Set up test fixtures"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.valid_user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com'
        }

    def test_create_user_success(self):
        """Test successful user creation"""
        response = self.client.post('/api/v1/users/',
                                  json=self.valid_user_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], 'John')
        self.assertEqual(data['last_name'], 'Doe')
        self.assertEqual(data['email'], 'john.doe@example.com')
        self.assertFalse(data['is_admin'])

    def test_create_user_missing_required_fields(self):
        """Test user creation with missing required fields"""
        # Test missing first_name
        user_data = self.valid_user_data.copy()
        del user_data['first_name']
        response = self.client.post('/api/v1/users/',
                                  json=user_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test missing last_name
        user_data = self.valid_user_data.copy()
        del user_data['last_name']
        response = self.client.post('/api/v1/users/',
                                  json=user_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test missing email
        user_data = self.valid_user_data.copy()
        del user_data['email']
        response = self.client.post('/api/v1/users/',
                                  json=user_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_data(self):
        """Test user creation with invalid data"""
        # Test empty first_name
        user_data = self.valid_user_data.copy()
        user_data['first_name'] = ""
        response = self.client.post('/api/v1/users/',
                                  json=user_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test empty last_name
        user_data = self.valid_user_data.copy()
        user_data['last_name'] = ""
        response = self.client.post('/api/v1/users/',
                                  json=user_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test invalid email format
        user_data = self.valid_user_data.copy()
        user_data['email'] = "invalid-email"
        response = self.client.post('/api/v1/users/',
                                  json=user_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_create_user_with_admin_flag(self):
        """Test user creation with admin flag"""
        user_data = self.valid_user_data.copy()
        user_data['is_admin'] = True
        response = self.client.post('/api/v1/users/',
                                  json=user_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        data = json.loads(response.data)
        self.assertTrue(data['is_admin'])

    def test_get_all_users(self):
        """Test getting all users"""
        # First create a user
        self.client.post('/api/v1/users/',
                        json=self.valid_user_data,
                        content_type='application/json')
        
        # Then get all users
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_get_user_by_id(self):
        """Test getting a user by ID"""
        # First create a user
        create_response = self.client.post('/api/v1/users/',
                                         json=self.valid_user_data,
                                         content_type='application/json')
        user_data = json.loads(create_response.data)
        user_id = user_data['id']
        
        # Then get the user by ID
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['id'], user_id)
        self.assertEqual(data['first_name'], 'John')

    def test_get_user_by_invalid_id(self):
        """Test getting a user with invalid ID"""
        response = self.client.get('/api/v1/users/invalid-id')
        self.assertEqual(response.status_code, 404)

    def test_update_user_success(self):
        """Test successful user update"""
        # First create a user
        create_response = self.client.post('/api/v1/users/',
                                         json=self.valid_user_data,
                                         content_type='application/json')
        user_data = json.loads(create_response.data)
        user_id = user_data['id']
        
        # Then update the user
        update_data = {'first_name': 'Jane'}
        response = self.client.put(f'/api/v1/users/{user_id}',
                                 json=update_data,
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], 'Jane')
        self.assertEqual(data['last_name'], 'Doe')  # Should remain unchanged

    def test_update_user_invalid_data(self):
        """Test user update with invalid data"""
        # First create a user
        create_response = self.client.post('/api/v1/users/',
                                         json=self.valid_user_data,
                                         content_type='application/json')
        user_data = json.loads(create_response.data)
        user_id = user_data['id']
        
        # Try to update with invalid email
        update_data = {'email': 'invalid-email'}
        response = self.client.put(f'/api/v1/users/{user_id}',
                                 json=update_data,
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update_nonexistent_user(self):
        """Test updating a user that doesn't exist"""
        update_data = {'first_name': 'Jane'}
        response = self.client.put('/api/v1/users/nonexistent-id',
                                 json=update_data,
                                 content_type='application/json')
        self.assertEqual(response.status_code, 404)


class TestPlaceEndpoints(unittest.TestCase):
    """Test cases for Place endpoints"""

    def setUp(self):
        """Set up test fixtures"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Create a user first for place ownership
        self.user_data = {
            'first_name': 'Owner',
            'last_name': 'User',
            'email': 'owner@example.com'
        }
        user_response = self.client.post('/api/v1/users/',
                                       json=self.user_data,
                                       content_type='application/json')
        self.user = json.loads(user_response.data)
        
        self.valid_place_data = {
            'title': 'Beautiful Apartment',
            'description': 'A lovely place to stay',
            'price': 150.0,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'owner_id': self.user['id']
        }

    def test_create_place_success(self):
        """Test successful place creation"""
        response = self.client.post('/api/v1/places/',
                                  json=self.valid_place_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['title'], 'Beautiful Apartment')
        self.assertEqual(data['price'], 150.0)
        self.assertEqual(data['latitude'], 40.7128)
        self.assertEqual(data['longitude'], -74.0060)
        self.assertEqual(data['owner_id'], self.user['id'])

    def test_create_place_missing_required_fields(self):
        """Test place creation with missing required fields"""
        # Test missing title
        place_data = self.valid_place_data.copy()
        del place_data['title']
        response = self.client.post('/api/v1/places/',
                                  json=place_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test missing price
        place_data = self.valid_place_data.copy()
        del place_data['price']
        response = self.client.post('/api/v1/places/',
                                  json=place_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_data(self):
        """Test place creation with invalid data"""
        # Test empty title
        place_data = self.valid_place_data.copy()
        place_data['title'] = ""
        response = self.client.post('/api/v1/places/',
                                  json=place_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test negative price
        place_data = self.valid_place_data.copy()
        place_data['price'] = -50.0
        response = self.client.post('/api/v1/places/',
                                  json=place_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test zero price
        place_data = self.valid_place_data.copy()
        place_data['price'] = 0
        response = self.client.post('/api/v1/places/',
                                  json=place_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test invalid latitude
        place_data = self.valid_place_data.copy()
        place_data['latitude'] = 91
        response = self.client.post('/api/v1/places/',
                                  json=place_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test invalid longitude
        place_data = self.valid_place_data.copy()
        place_data['longitude'] = 181
        response = self.client.post('/api/v1/places/',
                                  json=place_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_owner(self):
        """Test place creation with invalid owner"""
        place_data = self.valid_place_data.copy()
        place_data['owner_id'] = 'invalid-owner-id'
        response = self.client.post('/api/v1/places/',
                                  json=place_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_get_all_places(self):
        """Test getting all places"""
        # First create a place
        self.client.post('/api/v1/places/',
                        json=self.valid_place_data,
                        content_type='application/json')
        
        # Then get all places
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_get_place_by_id(self):
        """Test getting a place by ID"""
        # First create a place
        create_response = self.client.post('/api/v1/places/',
                                         json=self.valid_place_data,
                                         content_type='application/json')
        place_data = json.loads(create_response.data)
        place_id = place_data['id']
        
        # Then get the place by ID
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['id'], place_id)
        self.assertEqual(data['title'], 'Beautiful Apartment')

    def test_update_place_success(self):
        """Test successful place update"""
        # First create a place
        create_response = self.client.post('/api/v1/places/',
                                         json=self.valid_place_data,
                                         content_type='application/json')
        place_data = json.loads(create_response.data)
        place_id = place_data['id']
        
        # Then update the place
        update_data = {'title': 'Updated Apartment'}
        response = self.client.put(f'/api/v1/places/{place_id}',
                                 json=update_data,
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Updated Apartment')


class TestAmenityEndpoints(unittest.TestCase):
    """Test cases for Amenity endpoints"""

    def setUp(self):
        """Set up test fixtures"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.valid_amenity_data = {'name': 'WiFi'}

    def test_create_amenity_success(self):
        """Test successful amenity creation"""
        response = self.client.post('/api/v1/amenities/',
                                  json=self.valid_amenity_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'WiFi')

    def test_create_amenity_missing_name(self):
        """Test amenity creation with missing name"""
        response = self.client.post('/api/v1/amenities/',
                                  json={},
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_create_amenity_empty_name(self):
        """Test amenity creation with empty name"""
        amenity_data = {'name': ''}
        response = self.client.post('/api/v1/amenities/',
                                  json=amenity_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_get_all_amenities(self):
        """Test getting all amenities"""
        # First create an amenity
        self.client.post('/api/v1/amenities/',
                        json=self.valid_amenity_data,
                        content_type='application/json')
        
        # Then get all amenities
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)


class TestReviewEndpoints(unittest.TestCase):
    """Test cases for Review endpoints"""

    def setUp(self):
        """Set up test fixtures"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Create a user first
        self.user_data = {
            'first_name': 'Reviewer',
            'last_name': 'User',
            'email': 'reviewer@example.com'
        }
        user_response = self.client.post('/api/v1/users/',
                                       json=self.user_data,
                                       content_type='application/json')
        self.user = json.loads(user_response.data)
        
        # Create an owner user
        self.owner_data = {
            'first_name': 'Owner',
            'last_name': 'User',
            'email': 'owner@example.com'
        }
        owner_response = self.client.post('/api/v1/users/',
                                        json=self.owner_data,
                                        content_type='application/json')
        self.owner = json.loads(owner_response.data)
        
        # Create a place
        self.place_data = {
            'title': 'Test Place',
            'description': 'Test Description',
            'price': 100.0,
            'latitude': 0,
            'longitude': 0,
            'owner_id': self.owner['id']
        }
        place_response = self.client.post('/api/v1/places/',
                                        json=self.place_data,
                                        content_type='application/json')
        self.place = json.loads(place_response.data)
        
        self.valid_review_data = {
            'text': 'This is a great place!',
            'rating': 5,
            'place_id': self.place['id'],
            'user_id': self.user['id']
        }

    def test_create_review_success(self):
        """Test successful review creation"""
        response = self.client.post('/api/v1/reviews/',
                                  json=self.valid_review_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['text'], 'This is a great place!')
        self.assertEqual(data['rating'], 5)

    def test_create_review_missing_required_fields(self):
        """Test review creation with missing required fields"""
        # Test missing text
        review_data = self.valid_review_data.copy()
        del review_data['text']
        response = self.client.post('/api/v1/reviews/',
                                  json=review_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test missing rating
        review_data = self.valid_review_data.copy()
        del review_data['rating']
        response = self.client.post('/api/v1/reviews/',
                                  json=review_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_data(self):
        """Test review creation with invalid data"""
        # Test empty text
        review_data = self.valid_review_data.copy()
        review_data['text'] = ""
        response = self.client.post('/api/v1/reviews/',
                                  json=review_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test invalid rating
        review_data = self.valid_review_data.copy()
        review_data['rating'] = 0
        response = self.client.post('/api/v1/reviews/',
                                  json=review_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

        review_data['rating'] = 6
        response = self.client.post('/api/v1/reviews/',
                                  json=review_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_get_all_reviews(self):
        """Test getting all reviews"""
        # First create a review
        self.client.post('/api/v1/reviews/',
                        json=self.valid_review_data,
                        content_type='application/json')
        
        # Then get all reviews
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)


if __name__ == '__main__':
    unittest.main()
