# HBnB Part 3: Enhanced Backend with Authentication and Database Integration

This document outlines the implementation of Part 3 of the HBnB project, which introduces user authentication, authorization, and database integration using SQLAlchemy and SQLite.

## Overview

Part 3 extends the backend application by:
- Implementing JWT-based user authentication
- Adding role-based access control (admin vs regular users)
- Replacing in-memory storage with SQLite database
- Mapping all entities to SQLAlchemy models
- Creating comprehensive database relationships
- Providing SQL scripts for database setup and testing

## Features Implemented

### 1. User Authentication & Authorization
- **Password Hashing**: Secure password storage using bcrypt
- **JWT Authentication**: Token-based authentication system
- **Role-Based Access Control**: Admin and regular user privileges
- **Email Validation**: Unique email constraints and validation

### 2. Database Integration
- **SQLAlchemy ORM**: Object-relational mapping for all entities
- **SQLite Database**: Development database with SQLite
- **Database Relationships**: Proper foreign keys and relationships
- **Data Persistence**: All data now persists between application restarts

### 3. Enhanced Models
- **User Model**: Includes password hashing and admin privileges
- **Place Model**: Location-based property listings
- **Review Model**: User reviews and ratings
- **Amenity Model**: Property amenities with many-to-many relationships

## Project Structure

```
part2/
├── app/
│   ├── models/
│   │   ├── BaseModel.py          # SQLAlchemy base model
│   │   ├── user.py               # User model with authentication
│   │   ├── place.py              # Place model
│   │   ├── review.py             # Review model
│   │   ├── amenity.py            # Amenity model
│   │   └── place_amenity.py      # Association table
│   ├── persistence/
│   │   ├── repository.py         # Base repository pattern
│   │   ├── user_repository.py    # User-specific repository
│   │   ├── place_repository.py   # Place-specific repository
│   │   ├── review_repository.py  # Review-specific repository
│   │   └── amenity_repository.py # Amenity-specific repository
│   ├── services/
│   │   └── facade.py             # Business logic facade
│   └── __init__.py               # App factory with database config
├── sql/
│   ├── create_tables.sql         # Database schema creation
│   ├── insert_initial_data.sql   # Sample data insertion
│   └── test_operations.sql       # Database testing queries
├── database_diagrams.md          # Comprehensive ER diagrams
├── er_diagram.md                 # Main ER diagram
├── init_database.py              # Database initialization script
├── requirements.txt              # Updated dependencies
└── README_PART3.md              # This file
```

## Database Schema

### Tables
1. **users** - User accounts with authentication
2. **places** - Property listings
3. **amenities** - Available amenities
4. **reviews** - User reviews and ratings
5. **place_amenities** - Many-to-many relationship table

### Key Relationships
- User → Places (One-to-Many): A user can own multiple places
- User → Reviews (One-to-Many): A user can write multiple reviews
- Place → Reviews (One-to-Many): A place can have multiple reviews
- Place ↔ Amenities (Many-to-Many): Places can have multiple amenities

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python init_database.py
```

This will:
- Create the SQLite database (`hbnb.db`)
- Create all tables with proper relationships
- Insert sample data including admin user and amenities

### 3. Run the Application
```bash
python run.py
```

## API Endpoints

### User Management
- `POST /api/v1/users/` - Create new user (with password)
- `GET /api/v1/users/` - List all users
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user (with password support)

### Place Management
- `POST /api/v1/places/` - Create new place
- `GET /api/v1/places/` - List all places
- `GET /api/v1/places/{id}` - Get place by ID
- `PUT /api/v1/places/{id}` - Update place

### Review Management
- `POST /api/v1/reviews/` - Create new review
- `GET /api/v1/reviews/` - List all reviews
- `GET /api/v1/reviews/{id}` - Get review by ID
- `PUT /api/v1/reviews/{id}` - Update review

### Amenity Management
- `POST /api/v1/amenities/` - Create new amenity
- `GET /api/v1/amenities/` - List all amenities
- `GET /api/v1/amenities/{id}` - Get amenity by ID
- `PUT /api/v1/amenities/{id}` - Update amenity

## Sample Data

The database is initialized with:
- **Admin User**: admin@hbnb.com (password: admin123)
- **Regular Users**: john.doe@example.com, jane.smith@example.com, bob.johnson@example.com
- **Sample Places**: Beach house, downtown apartment, mountain cabin, luxury penthouse
- **Amenities**: WiFi, Pool, Gym, Parking, Kitchen, Air Conditioning, Heating, TV, Washer, Dryer
- **Sample Reviews**: Reviews for various places with ratings

## Database Testing

### Using SQL Scripts
```bash
# Create tables
sqlite3 hbnb.db < sql/create_tables.sql

# Insert sample data
sqlite3 hbnb.db < sql/insert_initial_data.sql

# Run test queries
sqlite3 hbnb.db < sql/test_operations.sql
```

### Using Python Script
```bash
python init_database.py
```

## Security Features

1. **Password Hashing**: All passwords are hashed using bcrypt
2. **Email Uniqueness**: Email addresses must be unique
3. **Input Validation**: All inputs are validated before processing
4. **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
5. **Admin Privileges**: Role-based access control for admin operations

## Database Diagrams

The project includes comprehensive Mermaid.js diagrams:
- **ER Diagram**: Complete entity-relationship diagram
- **Data Flow**: Database operations flow
- **Constraints**: Database constraints and indexes
- **Sample Data**: Visual representation of sample relationships

View the diagrams in:
- `database_diagrams.md` - Comprehensive diagrams
- `er_diagram.md` - Main ER diagram

## Development Notes

### Model Changes
- All models now inherit from SQLAlchemy BaseModel
- Password handling is integrated into User model
- Relationships are properly defined with foreign keys
- Validation is maintained from previous parts

### Repository Pattern
- Maintained repository pattern for data access
- Added specialized repositories for each entity
- Enhanced with entity-specific query methods

### Facade Updates
- Updated to use SQLAlchemy repositories
- Added password handling for user operations
- Enhanced error handling and validation

## Next Steps

This implementation provides a solid foundation for:
1. JWT authentication implementation
2. API endpoint protection
3. Production database configuration (MySQL/PostgreSQL)
4. Advanced querying and filtering
5. API documentation and testing

## Troubleshooting

### Common Issues
1. **Database not created**: Run `python init_database.py`
2. **Import errors**: Ensure all dependencies are installed
3. **Password issues**: Use the sample passwords provided
4. **Relationship errors**: Check that all models are properly imported

### Database Reset
To reset the database:
```bash
rm hbnb.db
python init_database.py
```

This completes the implementation of Part 3 with full database integration and authentication support.
