# HBnB API Implementation

This directory contains the complete implementation of the HBnB API endpoints for Users, Amenities, and Places.

## Overview

The implementation follows a clean architecture pattern with proper separation of concerns:

- **Presentation Layer**: Flask-RESTx API endpoints
- **Business Logic Layer**: Facade pattern with service methods
- **Persistence Layer**: Repository pattern with in-memory storage
- **Domain Layer**: Model classes with validation

## Features

✅ **User Endpoints**: Complete CRUD operations (Create, Read, Update)
✅ **Amenity Endpoints**: Complete CRUD operations (Create, Read, Update)
✅ **Place Endpoints**: Complete CRUD operations (Create, Read, Update)
✅ **Input Validation**: Comprehensive validation for all inputs
✅ **Error Handling**: Proper HTTP status codes and error messages
✅ **JSON Responses**: All responses are properly formatted JSON
✅ **API Documentation**: Auto-generated via Flask-RESTx
✅ **Testing**: Comprehensive test suite

## Quick Start

### Installation
```bash
pip3 install -r requirements.txt
```

### Running the Application
```bash
python3 run.py
```

The API will be available at `http://localhost:5001`

### API Documentation
Visit `http://localhost:5001/api/v1/` for interactive API documentation.

### Running Tests
```bash
python3 test_api_documentation.py
```

## API Endpoints

### Users
- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/` - Get all users
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user

### Amenities
- `POST /api/v1/amenities/` - Create a new amenity
- `GET /api/v1/amenities/` - Get all amenities
- `GET /api/v1/amenities/{id}` - Get amenity by ID
- `PUT /api/v1/amenities/{id}` - Update amenity

### Places
- `POST /api/v1/places/` - Create a new place
- `GET /api/v1/places/` - Get all places
- `GET /api/v1/places/{id}` - Get place by ID
- `PUT /api/v1/places/{id}` - Update place

## Example Usage

### Create a User
```bash
curl -X POST http://localhost:5001/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "is_admin": false
  }'
```

### Create an Amenity
```bash
curl -X POST http://localhost:5001/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Swimming Pool"
  }'
```

### Get All Users
```bash
curl -X GET http://localhost:5001/api/v1/users/
```

## Project Structure

```
part2/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── users.py      # User API endpoints
│   │       ├── amenities.py  # Amenity API endpoints
│   │       └── places.py     # Place API endpoints
│   ├── models/
│   │   ├── BaseModel.py      # Base model class
│   │   ├── user.py           # User model
│   │   ├── amenity.py        # Amenity model
│   │   └── place.py          # Place model
│   ├── services/
│   │   └── facade.py         # Business logic facade
│   └── persistence/
│       └── repository.py     # Repository pattern
├── tests/
│   └── models/
│       └── tuser.py          # User model tests
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
├── test_api_documentation.py # API test suite
└── API_IMPLEMENTATION_SUMMARY.md # Detailed documentation
```

## Validation Rules

### User Validation
- First name and last name: Required, max 50 characters
- Email: Required, valid email format, converted to lowercase
- Admin status: Boolean, defaults to false

### Amenity Validation
- Name: Required, max 50 characters

### Place Validation
- Title: Required, max 100 characters
- Price: Required, must be positive and non-zero
- Latitude: Required, between -90 and 90
- Longitude: Required, between -180 and 180
- Owner: Required, must reference existing user

## Error Handling

The API returns appropriate HTTP status codes:

- **200 OK**: Successful GET/PUT operations
- **201 Created**: Successful POST operations
- **400 Bad Request**: Invalid data or validation errors
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server errors


## Testing

The implementation includes comprehensive testing that covers:
- Model validation
- API endpoint functionality
- Error handling
- Integration scenarios

Run the test suite to verify all functionality:
```bash
python3 test_api_documentation.py
```

