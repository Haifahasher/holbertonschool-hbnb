# HBnB Database Schema Diagrams

This document contains Entity-Relationship (ER) diagrams for the HBnB project database schema using Mermaid.js.

## Complete Database Schema

```mermaid
erDiagram
    USERS {
        string id PK "Primary Key (UUID)"
        string first_name "User's first name (max 50 chars)"
        string last_name "User's last name (max 50 chars)"
        string email UK "User's email (unique, max 255 chars)"
        string password_hash "Hashed password (max 128 chars)"
        boolean is_admin "Admin flag (default false)"
        datetime created_at "Creation timestamp"
        datetime updated_at "Last update timestamp"
    }

    PLACES {
        string id PK "Primary Key (UUID)"
        string title "Place title (max 100 chars)"
        text description "Place description"
        float price "Price per night"
        float latitude "Geographic latitude"
        float longitude "Geographic longitude"
        string owner_id FK "Foreign Key to Users"
        datetime created_at "Creation timestamp"
        datetime updated_at "Last update timestamp"
    }

    AMENITIES {
        string id PK "Primary Key (UUID)"
        string name UK "Amenity name (unique, max 50 chars)"
        datetime created_at "Creation timestamp"
        datetime updated_at "Last update timestamp"
    }

    REVIEWS {
        string id PK "Primary Key (UUID)"
        text text "Review text content"
        integer rating "Rating (1-5 scale)"
        string place_id FK "Foreign Key to Places"
        string user_id FK "Foreign Key to Users"
        datetime created_at "Creation timestamp"
        datetime updated_at "Last update timestamp"
    }

    PLACE_AMENITIES {
        string place_id PK,FK "Foreign Key to Places"
        string amenity_id PK,FK "Foreign Key to Amenities"
    }

    %% Relationships
    USERS ||--o{ PLACES : "owns"
    USERS ||--o{ REVIEWS : "writes"
    PLACES ||--o{ REVIEWS : "receives"
    PLACES ||--o{ PLACE_AMENITIES : "has"
    AMENITIES ||--o{ PLACE_AMENITIES : "belongs_to"
```

## Simplified Entity Overview

```mermaid
erDiagram
    USER ||--o{ PLACE : "owns"
    USER ||--o{ REVIEW : "writes"
    PLACE ||--o{ REVIEW : "receives"
    PLACE }o--o{ AMENITY : "has"
```

## Detailed Relationship Diagram

```mermaid
erDiagram
    USERS {
        string id PK
        string first_name
        string last_name
        string email UK
        string password_hash
        boolean is_admin
        datetime created_at
        datetime updated_at
    }

    PLACES {
        string id PK
        string title
        text description
        float price
        float latitude
        float longitude
        string owner_id FK
        datetime created_at
        datetime updated_at
    }

    AMENITIES {
        string id PK
        string name UK
        datetime created_at
        datetime updated_at
    }

    REVIEWS {
        string id PK
        text text
        integer rating
        string place_id FK
        string user_id FK
        datetime created_at
        datetime updated_at
    }

    PLACE_AMENITIES {
        string place_id PK,FK
        string amenity_id PK,FK
    }

    %% One-to-Many Relationships
    USERS ||--o{ PLACES : "A user can own multiple places"
    USERS ||--o{ REVIEWS : "A user can write multiple reviews"
    PLACES ||--o{ REVIEWS : "A place can have multiple reviews"

    %% Many-to-Many Relationship
    PLACES }o--o{ AMENITIES : "A place can have multiple amenities, an amenity can belong to multiple places"
```

## Database Constraints and Indexes

```mermaid
graph TD
    A[Database Constraints] --> B[Primary Keys]
    A --> C[Foreign Keys]
    A --> D[Unique Constraints]
    A --> E[Check Constraints]
    A --> F[Indexes]

    B --> B1[users.id]
    B --> B2[places.id]
    B --> B3[amenities.id]
    B --> B4[reviews.id]
    B --> B5[place_amenities composite PK]

    C --> C1[places.owner_id → users.id]
    C --> C2[reviews.place_id → places.id]
    C --> C3[reviews.user_id → users.id]
    C --> C4[place_amenities.place_id → places.id]
    C --> C5[place_amenities.amenity_id → amenities.id]

    D --> D1[users.email UNIQUE]
    D --> D2[amenities.name UNIQUE]

    E --> E1[reviews.rating BETWEEN 1 AND 5]
    E --> E2[places.price > 0]
    E --> E3[places.latitude BETWEEN -90 AND 90]
    E --> E4[places.longitude BETWEEN -180 AND 180]

    F --> F1[users.email INDEX]
    F --> F2[places.owner_id INDEX]
    F --> F3[reviews.place_id INDEX]
    F --> F4[reviews.user_id INDEX]
    F --> F5[amenities.name INDEX]
```

## Data Flow Diagram

```mermaid
flowchart TD
    A[User Registration] --> B[User Table]
    B --> C[User Authentication]
    C --> D[Place Creation]
    D --> E[Place Table]
    E --> F[Amenity Assignment]
    F --> G[Place-Amenity Association]
    G --> H[Place-Amenities Table]
    
    C --> I[Review Creation]
    I --> J[Review Table]
    J --> K[Place Rating Update]
    
    B --> L[Admin Operations]
    L --> M[User Management]
    L --> N[Amenity Management]
    
    E --> O[Place Search]
    O --> P[Filter by Amenities]
    O --> Q[Filter by Price Range]
    O --> R[Filter by Location]
```

## Sample Data Relationships

```mermaid
graph LR
    subgraph "Sample Users"
        U1[Admin User<br/>admin@hbnb.com]
        U2[John Doe<br/>john.doe@example.com]
        U3[Jane Smith<br/>jane.smith@example.com]
        U4[Bob Johnson<br/>bob.johnson@example.com]
    end

    subgraph "Sample Places"
        P1[Beautiful Beach House<br/>$150/night]
        P2[Cozy Downtown Apartment<br/>$85/night]
        P3[Mountain Cabin Retreat<br/>$120/night]
        P4[Luxury Penthouse<br/>$300/night]
    end

    subgraph "Sample Amenities"
        A1[WiFi]
        A2[Pool]
        A3[Gym]
        A4[Parking]
        A5[Kitchen]
    end

    U2 --> P1
    U3 --> P2
    U2 --> P3
    U4 --> P4

    P1 --> A1
    P1 --> A2
    P1 --> A4
    P1 --> A5

    P2 --> A1
    P2 --> A4
    P2 --> A5

    P3 --> A1
    P3 --> A4
    P3 --> A5

    P4 --> A1
    P4 --> A2
    P4 --> A3
    P4 --> A4
    P4 --> A5
```

## Database Schema Summary

### Tables:
1. **users** - Stores user information including authentication data
2. **places** - Stores property listings with location and pricing
3. **amenities** - Stores available amenities (WiFi, Pool, etc.)
4. **reviews** - Stores user reviews and ratings for places
5. **place_amenities** - Junction table for many-to-many relationship between places and amenities

### Key Relationships:
- **One-to-Many**: User → Places (a user can own multiple places)
- **One-to-Many**: User → Reviews (a user can write multiple reviews)
- **One-to-Many**: Place → Reviews (a place can have multiple reviews)
- **Many-to-Many**: Place ↔ Amenities (places can have multiple amenities, amenities can belong to multiple places)

### Security Features:
- Password hashing using bcrypt
- Email uniqueness constraints
- Admin role-based access control
- Foreign key constraints for data integrity

### Performance Optimizations:
- Indexes on frequently queried columns (email, owner_id, place_id, user_id)
- Proper foreign key relationships for efficient joins
- Composite primary key for junction table
