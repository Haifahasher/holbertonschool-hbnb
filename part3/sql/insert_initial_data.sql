-- SQL Script to insert initial data for HBnB project
-- This script populates the database with sample data

-- Insert admin user (password: admin123)
INSERT INTO users (id, first_name, last_name, email, password_hash, is_admin, created_at, updated_at) 
VALUES (
    'admin-user-001',
    'Admin',
    'User',
    'admin@hbnb.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4j5Kj5Kj5K', -- bcrypt hash for 'admin123'
    TRUE,
    datetime('now'),
    datetime('now')
);

-- Insert regular users
INSERT INTO users (id, first_name, last_name, email, password_hash, is_admin, created_at, updated_at) 
VALUES 
(
    'user-001',
    'John',
    'Doe',
    'john.doe@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4j5Kj5Kj5K', -- bcrypt hash for 'password123'
    FALSE,
    datetime('now'),
    datetime('now')
),
(
    'user-002',
    'Jane',
    'Smith',
    'jane.smith@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4j5Kj5Kj5K', -- bcrypt hash for 'password123'
    FALSE,
    datetime('now'),
    datetime('now')
),
(
    'user-003',
    'Bob',
    'Johnson',
    'bob.johnson@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4j5Kj5Kj5K', -- bcrypt hash for 'password123'
    FALSE,
    datetime('now'),
    datetime('now')
);

-- Insert amenities
INSERT INTO amenities (id, name, created_at, updated_at) 
VALUES 
('amenity-001', 'WiFi', datetime('now'), datetime('now')),
('amenity-002', 'Pool', datetime('now'), datetime('now')),
('amenity-003', 'Gym', datetime('now'), datetime('now')),
('amenity-004', 'Parking', datetime('now'), datetime('now')),
('amenity-005', 'Kitchen', datetime('now'), datetime('now')),
('amenity-006', 'Air Conditioning', datetime('now'), datetime('now')),
('amenity-007', 'Heating', datetime('now'), datetime('now')),
('amenity-008', 'TV', datetime('now'), datetime('now')),
('amenity-009', 'Washer', datetime('now'), datetime('now')),
('amenity-010', 'Dryer', datetime('now'), datetime('now'));

-- Insert places
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at) 
VALUES 
(
    'place-001',
    'Beautiful Beach House',
    'A stunning beachfront property with ocean views and modern amenities.',
    150.00,
    34.0522,
    -118.2437,
    'user-001',
    datetime('now'),
    datetime('now')
),
(
    'place-002',
    'Cozy Downtown Apartment',
    'Modern apartment in the heart of the city with easy access to public transportation.',
    85.00,
    40.7128,
    -74.0060,
    'user-002',
    datetime('now'),
    datetime('now')
),
(
    'place-003',
    'Mountain Cabin Retreat',
    'Peaceful cabin surrounded by nature, perfect for a quiet getaway.',
    120.00,
    39.7392,
    -104.9903,
    'user-001',
    datetime('now'),
    datetime('now')
),
(
    'place-004',
    'Luxury Penthouse',
    'High-end penthouse with panoramic city views and premium amenities.',
    300.00,
    41.8781,
    -87.6298,
    'user-003',
    datetime('now'),
    datetime('now')
);

-- Insert place-amenity associations
INSERT INTO place_amenities (place_id, amenity_id) 
VALUES 
-- Beach House amenities
('place-001', 'amenity-001'), -- WiFi
('place-001', 'amenity-002'), -- Pool
('place-001', 'amenity-004'), -- Parking
('place-001', 'amenity-005'), -- Kitchen
('place-001', 'amenity-006'), -- Air Conditioning
('place-001', 'amenity-008'), -- TV
-- Downtown Apartment amenities
('place-002', 'amenity-001'), -- WiFi
('place-002', 'amenity-004'), -- Parking
('place-002', 'amenity-005'), -- Kitchen
('place-002', 'amenity-006'), -- Air Conditioning
('place-002', 'amenity-007'), -- Heating
('place-002', 'amenity-008'), -- TV
-- Mountain Cabin amenities
('place-003', 'amenity-001'), -- WiFi
('place-003', 'amenity-004'), -- Parking
('place-003', 'amenity-005'), -- Kitchen
('place-003', 'amenity-007'), -- Heating
('place-003', 'amenity-008'), -- TV
('place-003', 'amenity-009'), -- Washer
('place-003', 'amenity-010'), -- Dryer
-- Luxury Penthouse amenities
('place-004', 'amenity-001'), -- WiFi
('place-004', 'amenity-002'), -- Pool
('place-004', 'amenity-003'), -- Gym
('place-004', 'amenity-004'), -- Parking
('place-004', 'amenity-005'), -- Kitchen
('place-004', 'amenity-006'), -- Air Conditioning
('place-004', 'amenity-007'), -- Heating
('place-004', 'amenity-008'), -- TV
('place-004', 'amenity-009'), -- Washer
('place-004', 'amenity-010'); -- Dryer

-- Insert reviews
INSERT INTO reviews (id, text, rating, place_id, user_id, created_at, updated_at) 
VALUES 
(
    'review-001',
    'Amazing beach house with incredible ocean views! The property was clean and well-maintained.',
    5,
    'place-001',
    'user-002',
    datetime('now'),
    datetime('now')
),
(
    'review-002',
    'Great location in downtown. The apartment was modern and comfortable.',
    4,
    'place-002',
    'user-001',
    datetime('now'),
    datetime('now')
),
(
    'review-003',
    'Perfect for a quiet retreat. The cabin was cozy and had everything we needed.',
    5,
    'place-003',
    'user-003',
    datetime('now'),
    datetime('now')
),
(
    'review-004',
    'Luxury at its finest! The penthouse exceeded all expectations.',
    5,
    'place-004',
    'user-001',
    datetime('now'),
    datetime('now')
),
(
    'review-005',
    'Good value for money. The apartment was clean and well-equipped.',
    4,
    'place-002',
    'user-003',
    datetime('now'),
    datetime('now')
);
