# Sequence Diagrams for HBnB Evolution API Calls

## Overview
These sequence diagrams illustrate the interaction flow between the different layers of the HBnB Evolution application based on the three-layer architecture with facade patterns.

## 1. User Registration Sequence Diagram

```mermaid
sequenceDiagram
    participant Client
    participant APIE as API Endpoints
    participant SA as ServiceAPI
    participant PRC as Processor
    participant User
    participant DT as Data
    participant REPO as Repositories
    participant DB as Database
    
    Client->>APIE: POST /users/register
    Note over Client,APIE: {phoneNum, firstName, lastName, email, password}
    
    APIE->>SA: registerUser(userData)
    SA->>SA: validateInputData()
    SA->>SA: checkEmailUniqueness()
    
    SA->>PRC: processUserRegistration(userData)
    PRC->>User: register(phoneNum, firstName, lastName)
    User->>User: generateUUID()
    User->>User: setTimestamps()
    User->>User: hashPassword()
    
    User->>DT: saveUser(user)
    DT->>REPO: save(user)
    REPO->>DB: INSERT INTO users
    DB-->>REPO: user_id
    REPO-->>DT: saved_user
    DT-->>User: confirmation
    User-->>PRC: user_object
    PRC-->>SA: registration_result
    SA-->>APIE: user_response
    APIE-->>Client: 201 Created + user_data
```

## 2. Place Creation Sequence Diagram

```mermaid
sequenceDiagram
    participant Client
    participant APIE as API Endpoints
    participant SA as ServiceAPI
    participant PRC as Processor
    participant Place
    participant User
    participant DT as Data
    participant REPO as Repositories
    participant DB as Database
    
    Client->>APIE: POST /places
    Note over Client,APIE: {title, description, price, latitude, longitude}
    
    APIE->>SA: createPlace(placeData, userId)
    SA->>SA: validatePlaceData()
    SA->>SA: verifyUserOwnership(userId)
    
    SA->>PRC: processPlaceCreation(placeData, userId)
    PRC->>User: getUserById(userId)
    User->>DT: findUser(userId)
    DT->>REPO: findById(userId)
    REPO->>DB: SELECT FROM users
    DB-->>REPO: user_data
    REPO-->>DT: user_object
    DT-->>User: user_found
    User-->>PRC: user_verified
    
    PRC->>Place: createP(title, description, price, latitude, longitude)
    Place->>Place: generateUUID()
    Place->>Place: setTimestamps()
    Place->>Place: validateCoordinates()
    Place->>Place: validatePrice()
    
    Place->>DT: savePlace(place)
    DT->>REPO: save(place)
    REPO->>DB: INSERT INTO places
    DB-->>REPO: place_id
    REPO-->>DT: saved_place
    DT-->>Place: confirmation
    Place-->>PRC: place_object
    PRC-->>SA: creation_result
    SA-->>APIE: place_response
    APIE-->>Client: 201 Created + place_data
```

## 3. Review Submission Sequence Diagram

```mermaid
sequenceDiagram
    participant Client
    participant APIE as API Endpoints
    participant SA as ServiceAPI
    participant PRC as Processor
    participant Review
    participant Place
    participant User
    participant DT as Data
    participant REPO as Repositories
    participant DB as Database
    
    Client->>APIE: POST /places/{placeId}/reviews
    Note over Client,APIE: {rating, comment}
    
    APIE->>SA: createReview(placeId, userId, reviewData)
    SA->>SA: validateReviewData()
    
    SA->>PRC: processReviewCreation(placeId, userId, reviewData)
    
    PRC->>Place: getPlaceById(placeId)
    Place->>DT: findPlace(placeId)
    DT->>REPO: findById(placeId)
    REPO->>DB: SELECT FROM places
    DB-->>REPO: place_data
    REPO-->>DT: place_object
    DT-->>Place: place_found
    Place-->>PRC: place_exists
    
    PRC->>User: getUserById(userId)
    User->>DT: findUser(userId)
    DT->>REPO: findById(userId)
    REPO->>DB: SELECT FROM users
    DB-->>REPO: user_data
    REPO-->>DT: user_object
    DT-->>User: user_found
    User-->>PRC: user_exists
    
    PRC->>Review: createRev(rating, comment)
    Review->>Review: generateUUID()
    Review->>Review: setTimestamps()
    Review->>Review: validateRating()
    Review->>Review: setPlaceAndUser(placeId, userId)
    
    Review->>DT: saveReview(review)
    DT->>REPO: save(review)
    REPO->>DB: INSERT INTO reviews
    DB-->>REPO: review_id
    REPO-->>DT: saved_review
    DT-->>Review: confirmation
    Review-->>PRC: review_object
    PRC-->>SA: creation_result
    SA-->>APIE: review_response
    APIE-->>Client: 201 Created + review_data
```

## 4. Fetching Places List Sequence Diagram

```mermaid
sequenceDiagram
    participant Client
    participant APIE as API Endpoints
    participant SA as ServiceAPI
    participant PRC as Processor
    participant Place
    participant Amenity
    participant DT as Data
    participant REPO as Repositories
    participant DB as Database
    
    Client->>APIE: GET /places?page=1&limit=10
    Note over Client,APIE: Query parameters for pagination
    
    APIE->>SA: getPlaces(pagination, filters)
    SA->>SA: parsePaginationParams()
    SA->>SA: validateFilters()
    
    SA->>PRC: processPlacesRetrieval(pagination, filters)
    PRC->>Place: listPlaces()
    Place->>DT: getPlaces(pagination, filters)
    DT->>REPO: findAll(pagination, filters)
    REPO->>DB: SELECT FROM places LIMIT offset, limit
    DB-->>REPO: places_data
    REPO-->>DT: places_list
    DT-->>Place: places_found
    Place-->>PRC: places_objects
    
    PRC->>PRC: enrichPlacesWithAmenities(places)
    
    loop for each place
        PRC->>Amenity: getAmenitiesForPlace(placeId)
        Amenity->>DT: findAmenitiesByPlace(placeId)
        DT->>REPO: findAmenitiesByPlace(placeId)
        REPO->>DB: SELECT amenities FROM place_amenities WHERE place_id = ?
        DB-->>REPO: amenities_data
        REPO-->>DT: amenities_list
        DT-->>Amenity: amenities_found
        Amenity-->>PRC: place_amenities
    end
    
    PRC-->>SA: enriched_places_response
    SA-->>APIE: places_response
    APIE-->>Client: 200 OK + places_list
```

## API Call Descriptions

### 1. User Registration
**Purpose**: Allows new users to create accounts in the system
**Key Steps**:
- Input validation and email uniqueness check through ServiceAPI
- User creation via Processor facade
- Password hashing and UUID generation
- Data persistence through Data facade

### 2. Place Creation
**Purpose**: Enables users to list their properties
**Key Steps**:
- User ownership verification
- Place data validation (coordinates, price)
- Place creation with geographic constraints
- Data persistence with proper relationships

### 3. Review Submission
**Purpose**: Allows users to provide feedback on places they've visited
**Key Steps**:
- Verification of place and user existence
- Review data validation (rating range 1-5)
- Review creation with proper associations
- Data persistence with foreign key relationships

### 4. Fetching Places List
**Purpose**: Retrieves a paginated list of places with amenities
**Key Steps**:
- Pagination parameter parsing and validation
- Places retrieval through Processor facade
- Amenity enrichment for each place
- Response with complete place information

## Architecture Patterns Demonstrated

- **Facade Pattern**: ServiceAPI, Processor, and Data facades simplify layer interactions
- **Repository Pattern**: Data access abstraction through Repositories
- **Service Layer Pattern**: Business logic coordination through Services
- **Validation Pattern**: Input verification at multiple levels
- **Enrichment Pattern**: Adding related data (amenities) to responses 