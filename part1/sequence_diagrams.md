# Sequence Diagrams for API Calls

## Objective
The following sequence diagrams illustrate the interaction between the different layers in the HBnB application—**Presentation** (`ServiceAPI`), **Business Logic** (`Processor` + domain models), and **Persistence** (Repositories + Database)—for handling key API calls. They reflect your diagrams: unique `UUID4` IDs and timestamps (`CreatedAt`, `UpdatedAt`), owner linkage on `Place`, rating bounds on `Review`, and the many-to-many relation between `Place` and `Amenity`.

---

## 1. User Registration

```mermaid
sequenceDiagram
    participant User
    participant ServiceAPI as ServiceAPI (Presentation)
    participant Processor as Processor (Business Logic)
    participant UserRepo as UserRepository (Persistence)
    participant DB as Database

    User->>ServiceAPI: POST /v1/users {first_name,last_name,email,password,phone,admin?}
    ServiceAPI->>Processor: registerUser(dto)
    Processor->>Processor: validate email format, pw length
    Processor->>UserRepo: existsByEmail(email)?
    UserRepo->>DB: SELECT 1 FROM users WHERE email=?
    DB-->>UserRepo: 0/1
    alt email taken
        UserRepo-->>Processor: true
        Processor-->>ServiceAPI: ConflictError
        ServiceAPI-->>User: 409 CONFLICT
    else new email
        UserRepo-->>Processor: false
        Processor->>Processor: hash password; set id=UUID4; set CreatedAt/UpdatedAt
        Processor->>UserRepo: save(user)
        UserRepo->>DB: INSERT INTO users (...)
        DB-->>UserRepo: ok
        UserRepo-->>Processor: persisted user
        Processor-->>ServiceAPI: user DTO (no password)
        ServiceAPI-->>User: 201 CREATED {id, names, email, admin, created_at}
    end
```

**Explanation**: ServiceAPI forwards to Processor, which validates, enforces unique email, hashes the password, assigns UUID4 and timestamps, persists via UserRepository, and returns a safe DTO.

## 2. Place Creation

```mermaid
sequenceDiagram
    participant User
    participant ServiceAPI as ServiceAPI (Presentation)
    participant Processor as Processor (Business Logic)
    participant PlaceRepo as PlaceRepository (Persistence)
    participant AmenityRepo as AmenityRepository (Persistence)
    participant DB as Database

    User->>ServiceAPI: POST /v1/places {title,description,price,lat,lon,amenity_ids[]}
    ServiceAPI->>Processor: createPlace(dto, authUserId)
    Processor->>Processor: validate price>=0, lat∈[-90,90], lon∈[-180,180]
    Processor->>Processor: owner = authUserId; set id=UUID4; timestamps

    alt amenity_ids provided
        Processor->>AmenityRepo: findAllByIds(amenity_ids)
        AmenityRepo->>DB: SELECT * FROM amenities WHERE id IN (...)
        DB-->>AmenityRepo: rows
        AmenityRepo-->>Processor: amenities
        Processor->>Processor: ensure all requested IDs exist
    end

    Processor->>PlaceRepo: save(place, amenities)
    PlaceRepo->>DB: INSERT INTO places (...)
    PlaceRepo->>DB: INSERT INTO place_amenities(place_id, amenity_id)*  (for each amenity)
    DB-->>PlaceRepo: ok
    PlaceRepo-->>Processor: persisted place (+amenities)
    Processor-->>ServiceAPI: place DTO
    ServiceAPI-->>User: 201 CREATED {id, owner, fields..., amenities[]}
```

**Explanation**: Processor validates numeric bounds, binds owner from the authenticated user, verifies amenity IDs against AmenityRepository, then persists the Place and the many-to-many junction rows.

## 3. Review Submission

```mermaid
sequenceDiagram
    participant User
    participant ServiceAPI as ServiceAPI (Presentation)
    participant Processor as Processor (Business Logic)
    participant ReviewRepo as ReviewRepository (Persistence)
    participant PlaceRepo as PlaceRepository (Persistence)
    participant DB as Database

    User->>ServiceAPI: POST /v1/places/:placeId/reviews {rating, comment}
    ServiceAPI->>Processor: createReview(placeId, dto, authUserId)
    Processor->>Processor: validate rating ∈ [1..5], comment length
    Processor->>PlaceRepo: exists(placeId)?
    PlaceRepo->>DB: SELECT 1 FROM places WHERE id=?
    DB-->>PlaceRepo: 0/1
    alt place not found
        PlaceRepo-->>Processor: false
        Processor-->>ServiceAPI: NotFoundError
        ServiceAPI-->>User: 404 NOT FOUND
    else place exists
        PlaceRepo-->>Processor: true
        Processor->>ReviewRepo: hasUserReviewed(placeId, authUserId)?
        ReviewRepo->>DB: SELECT id FROM reviews WHERE place_id=? AND user_id=?
        DB-->>ReviewRepo: none/existing
        alt already reviewed
            ReviewRepo-->>Processor: found
            Processor-->>ServiceAPI: ConflictError
            ServiceAPI-->>User: 409 CONFLICT
        else new review
            ReviewRepo-->>Processor: none
            Processor->>Processor: set id=UUID4; timestamps
            Processor->>ReviewRepo: save(review)
            ReviewRepo->>DB: INSERT INTO reviews (...)
            DB-->>ReviewRepo: ok
            ReviewRepo-->>Processor: persisted review
            Processor-->>ServiceAPI: review DTO
            ServiceAPI-->>User: 201 CREATED {id, rating, comment, user_id, place_id}
        end
    end
```

**Explanation**: Processor enforces rating bounds, ensures the Place exists, prevents duplicate reviews per user/place, assigns UUID4 and timestamps, and persists via ReviewRepository.

## 4. Fetching a List of Places

```mermaid
sequenceDiagram
    participant User
    participant ServiceAPI as ServiceAPI (Presentation)
    participant Processor as Processor (Business Logic)
    participant PlaceRepo as PlaceRepository (Persistence)
    participant DB as Database

    User->>ServiceAPI: GET /v1/places?lat=&lon=&radius=&min_price=&max_price=&amenity_id=&page=&size=
    ServiceAPI->>Processor: listPlaces(filters, pagination)
    Processor->>Processor: normalize filters; defaults; bounds
    Processor->>PlaceRepo: query(filters, pagination)
    PlaceRepo->>DB: SELECT p.* FROM places p
    Note right of DB: WHERE by price range, optional geo (lat/lon or radius),\nAND EXISTS amenity filter via join/junction
    DB-->>PlaceRepo: rows + total_count
    PlaceRepo-->>Processor: Place[] + total_count
    Processor-->>ServiceAPI: map to PlaceDTO[] + page meta
    ServiceAPI-->>User: 200 OK {items: [...], page, size, total}
```

**Explanation**: Processor applies filter logic (price, geospatial, amenity). PlaceRepository executes the query (with a junction table for amenities), returning a paginated result set mapped to DTOs.

## Key Design Patterns Demonstrated

- **UUID4 Primary Keys**: All entities use UUID4 for unique identification
- **Timestamp Tracking**: `CreatedAt` and `UpdatedAt` fields on all entities
- **Owner Relationship**: Places are linked to their creating user via `owner` field
- **Rating Validation**: Reviews enforce rating bounds (1-5)
- **Many-to-Many Relations**: Place-Amenity relationship via junction table
- **Business Rule Enforcement**: Duplicate review prevention, email uniqueness
- **Geospatial Filtering**: Location-based place queries with radius support
- **Pagination**: Standardized pagination with metadata 