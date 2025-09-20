-- SQL Script to test CRUD operations for HBnB project
-- This script demonstrates various database operations

-- Test 1: Query all users
SELECT '=== ALL USERS ===' as test_name;
SELECT id, first_name, last_name, email, is_admin, created_at 
FROM users 
ORDER BY created_at;

-- Test 2: Query all places with owner information
SELECT '=== ALL PLACES WITH OWNERS ===' as test_name;
SELECT 
    p.id,
    p.title,
    p.price,
    p.latitude,
    p.longitude,
    u.first_name || ' ' || u.last_name as owner_name,
    u.email as owner_email
FROM places p
JOIN users u ON p.owner_id = u.id
ORDER BY p.price DESC;

-- Test 3: Query all amenities
SELECT '=== ALL AMENITIES ===' as test_name;
SELECT id, name, created_at 
FROM amenities 
ORDER BY name;

-- Test 4: Query places with their amenities
SELECT '=== PLACES WITH AMENITIES ===' as test_name;
SELECT 
    p.title,
    GROUP_CONCAT(a.name, ', ') as amenities
FROM places p
LEFT JOIN place_amenities pa ON p.id = pa.place_id
LEFT JOIN amenities a ON pa.amenity_id = a.id
GROUP BY p.id, p.title
ORDER BY p.title;

-- Test 5: Query reviews with place and user information
SELECT '=== ALL REVIEWS WITH DETAILS ===' as test_name;
SELECT 
    r.id,
    r.text,
    r.rating,
    p.title as place_title,
    u.first_name || ' ' || u.last_name as reviewer_name,
    r.created_at
FROM reviews r
JOIN places p ON r.place_id = p.id
JOIN users u ON r.user_id = u.id
ORDER BY r.created_at DESC;

-- Test 6: Calculate average rating for each place
SELECT '=== AVERAGE RATINGS BY PLACE ===' as test_name;
SELECT 
    p.title,
    COUNT(r.id) as review_count,
    ROUND(AVG(r.rating), 2) as average_rating
FROM places p
LEFT JOIN reviews r ON p.id = r.place_id
GROUP BY p.id, p.title
ORDER BY average_rating DESC;

-- Test 7: Query places by price range
SELECT '=== PLACES BETWEEN $100 AND $200 ===' as test_name;
SELECT 
    p.title,
    p.price,
    u.first_name || ' ' || u.last_name as owner_name
FROM places p
JOIN users u ON p.owner_id = u.id
WHERE p.price BETWEEN 100.00 AND 200.00
ORDER BY p.price;

-- Test 8: Query users who are admins
SELECT '=== ADMIN USERS ===' as test_name;
SELECT id, first_name, last_name, email, created_at 
FROM users 
WHERE is_admin = TRUE;

-- Test 9: Query places owned by a specific user
SELECT '=== PLACES OWNED BY JOHN DOE ===' as test_name;
SELECT 
    p.title,
    p.price,
    p.description
FROM places p
JOIN users u ON p.owner_id = u.id
WHERE u.first_name = 'John' AND u.last_name = 'Doe'
ORDER BY p.price;

-- Test 10: Query reviews by a specific user
SELECT '=== REVIEWS BY JANE SMITH ===' as test_name;
SELECT 
    r.text,
    r.rating,
    p.title as place_title,
    r.created_at
FROM reviews r
JOIN places p ON r.place_id = p.id
JOIN users u ON r.user_id = u.id
WHERE u.first_name = 'Jane' AND u.last_name = 'Smith'
ORDER BY r.created_at DESC;
