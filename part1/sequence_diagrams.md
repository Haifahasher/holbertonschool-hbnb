# Sequence Diagrams for API Calls

## Objective
The following sequence diagrams illustrate the interaction between the different layers (Presentation, Business Logic, and Persistence) in the HBnB application for handling various API calls.

## API Calls

### 1. User Registration
```mermaid
sequenceDiagram
    participant User
    participant ServiceAPI
    participant Processor
    participant UserRepository
    participant Database

    User->>ServiceAPI: Register User (email, password, first_name, last_name)
    ServiceAPI->>Processor: Validate and Process Registration
    Processor->>UserRepository: Check Email Uniqueness
    UserRepository->>Database: Query Existing Users
    Database-->>UserRepository: Return Results
    UserRepository-->>Processor: Email Status
    Processor->>UserRepository: Save New User (UUID4, timestamps)
    UserRepository->>Database: Insert User Data
    Database-->>UserRepository: Confirm Save
    UserRepository-->>Processor: Return User Object
    Processor-->>ServiceAPI: Return Success/Failure
    ServiceAPI-->>User: Registration Successful/Error
```

**Explanation:**
- The user sends a registration request to the ServiceAPI.
- The ServiceAPI forwards the request to the Processor for validation and processing.
- The Processor checks email uniqueness via UserRepository.
- A new user is created with UUID4 ID and timestamps.
- The user data is stored in the database through UserRepository.
- A response is returned to the user indicating success or failure.

### 2. Place Creation
```mermaid
sequenceDiagram
    participant User
    participant ServiceAPI
    participant Processor
    participant PlaceRepository
    participant AmenityRepository
    participant Database

    User->>ServiceAPI: Create Place (title, description, price, location, amenity_ids)
    ServiceAPI->>Processor: Validate and Process Place Creation
    Processor->>AmenityRepository: Verify Amenity IDs
    AmenityRepository->>Database: Query Amenities
    Database-->>AmenityRepository: Return Amenities
    AmenityRepository-->>Processor: Amenities Verified
    Processor->>PlaceRepository: Save Place (UUID4, owner, timestamps)
    PlaceRepository->>Database: Insert Place Data
    PlaceRepository->>Database: Create Place-Amenity Relations
    Database-->>PlaceRepository: Confirm Save
    PlaceRepository-->>Processor: Return Place Object
    Processor-->>ServiceAPI: Return Success/Failure
    ServiceAPI-->>User: Place Created Successfully/Error
```

**Explanation:**
- The user submits a request to create a place with amenities.
- The ServiceAPI routes the request to Processor for validation.
- The Processor verifies amenity IDs through AmenityRepository.
- A new place is created with UUID4 ID, owner linkage, and timestamps.
- The place and its amenity relationships are stored in the database.
- The API responds to the user with the creation outcome.

### 3. Review Submission
```mermaid
sequenceDiagram
    participant User
    participant ServiceAPI
    participant Processor
    participant ReviewRepository
    participant PlaceRepository
    participant Database

    User->>ServiceAPI: Submit Review (place_id, rating, comment)
    ServiceAPI->>Processor: Validate and Process Review
    Processor->>PlaceRepository: Verify Place Exists
    PlaceRepository->>Database: Query Place
    Database-->>PlaceRepository: Return Place Status
    PlaceRepository-->>Processor: Place Verified
    Processor->>ReviewRepository: Check Duplicate Review
    ReviewRepository->>Database: Query Existing Reviews
    Database-->>ReviewRepository: Return Review Status
    ReviewRepository-->>Processor: Duplicate Check Result
    Processor->>ReviewRepository: Save Review (UUID4, rating bounds, timestamps)
    ReviewRepository->>Database: Insert Review Data
    Database-->>ReviewRepository: Confirm Save
    ReviewRepository-->>Processor: Return Review Object
    Processor-->>ServiceAPI: Return Success/Failure
    ServiceAPI-->>User: Review Submitted Successfully/Error
```

**Explanation:**
- The user submits a review for a specific place.
- The ServiceAPI processes the request via the Processor layer.
- The Processor verifies the place exists and checks for duplicate reviews.
- A new review is created with UUID4 ID, rating validation (1-5), and timestamps.
- The review is stored in the database through ReviewRepository.
- The process concludes with a response to the user.

### 4. Fetching a List of Places
```mermaid
sequenceDiagram
    participant User
    participant ServiceAPI
    participant Processor
    participant PlaceRepository
    participant Database

    User->>ServiceAPI: Request Places (filters: location, price, amenities, pagination)
    ServiceAPI->>Processor: Process Request & Apply Filters
    Processor->>PlaceRepository: Query Places with Filters
    PlaceRepository->>Database: Fetch Matching Places with Amenities
    Database-->>PlaceRepository: Return Places List
    PlaceRepository-->>Processor: Return Places Data
    Processor-->>ServiceAPI: Return Filtered Places
    ServiceAPI-->>User: Display List of Places
```

**Explanation:**
- The user requests a list of places based on various filters.
- The ServiceAPI forwards the request to Processor for processing.
- The Processor applies filters and queries the database via PlaceRepository.
- The filtered results with amenities are returned through the ServiceAPI to the user.

## Key Design Patterns Demonstrated

- **UUID4 Primary Keys**: All entities use UUID4 for unique identification
- **Timestamp Tracking**: `CreatedAt` and `UpdatedAt` fields on all entities
- **Owner Relationship**: Places are linked to their creating user via `owner` field
- **Rating Validation**: Reviews enforce rating bounds (1-5)
- **Many-to-Many Relations**: Place-Amenity relationship via junction table
- **Business Rule Enforcement**: Duplicate review prevention, email uniqueness
- **Geospatial Filtering**: Location-based place queries with radius support
- **Pagination**: Standardized pagination with metadata 