# Part 4 - Simple Web Client

This part implements a complete frontend web client for the HBnB application using HTML5, CSS3, and JavaScript ES6.

## Features Implemented

### Task 2: Login Functionality ✅
- Login form with email and password validation
- JWT token storage in cookies for session management
- Automatic redirect to main page after successful login
- Error handling and display for failed login attempts
- API endpoint: `POST /api/v1/auth/login`

### Task 3: Index Page (Places List) ✅
- Dynamic loading of places from the API
- Client-side price filtering (All, $10, $50, $100)
- Authentication check with login link visibility
- Responsive grid layout for place cards
- API endpoint: `GET /api/v1/places/`

### Task 4: Place Details ✅
- Dynamic loading of place details from API
- Display of place information (name, price, description, host)
- Dynamic loading and display of reviews
- Conditional display of "Add Review" button based on authentication
- API endpoints: `GET /api/v1/places/{id}`, `GET /api/v1/reviews/`, `GET /api/v1/users/{id}`

### Task 5: Add Review Form ✅
- Authentication-required review submission form
- Redirect to index page for unauthenticated users
- Form validation and error handling
- Success/error message display
- Automatic redirect to place details after successful submission
- API endpoint: `POST /api/v1/reviews/`

## Technical Implementation

### Frontend Technologies
- **HTML5**: Semantic markup with proper structure
- **CSS3**: Modern styling with CSS Grid, Flexbox, and custom properties
- **JavaScript ES6**: Async/await, Fetch API, modern DOM manipulation

### Key Features
- **JWT Authentication**: Token-based authentication with cookie storage
- **CORS Support**: Backend configured for cross-origin requests
- **Responsive Design**: Mobile-friendly interface
- **Error Handling**: Comprehensive error handling and user feedback
- **Dynamic Content**: All content loaded dynamically from API

### API Integration
- All API calls use the Fetch API with proper error handling
- JWT tokens included in Authorization headers for protected endpoints
- Proper Content-Type headers for JSON requests
- CORS-enabled backend for frontend integration

## Setup Instructions

### Backend Setup (Part 3)
1. Navigate to the part3 directory
2. Install dependencies: `pip install -r requirements.txt`
3. Initialize the database: `python init_database.py`
4. Start the server: `python run.py`
5. The API will be available at `http://127.0.0.1:5000`

### Frontend Setup (Part 4)
1. Navigate to the part4 directory
2. Open `index.html` in a web browser or use a local server
3. For best results, use a local server like Live Server (VS Code extension) or Python's built-in server:
   ```bash
   python -m http.server 8000
   ```
4. Access the application at `http://localhost:8000`

## File Structure

```
part4/
├── index.html          # Main places listing page
├── login.html          # Login form page
├── place.html          # Place details page
├── add_review.html     # Add review form page
├── script.js           # Main JavaScript functionality
├── style.css           # CSS styles
└── README.md           # This file
```

## API Endpoints Used

### Authentication
- `POST /api/v1/auth/login` - User login

### Places
- `GET /api/v1/places/` - Get all places
- `GET /api/v1/places/{id}` - Get place by ID

### Reviews
- `GET /api/v1/reviews/` - Get all reviews
- `POST /api/v1/reviews/` - Create new review

### Users
- `GET /api/v1/users/{id}` - Get user by ID

## Sample User Accounts

Use these accounts for testing:
- **Admin**: admin@hbnb.com / admin123
- **Regular User**: john.doe@example.com / password123

## Browser Compatibility

The application uses modern JavaScript features and should work in:
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Notes

- All pages are W3C valid
- The application handles CORS properly for local development
- JWT tokens expire after 4 hours
- All form inputs are properly validated
- The interface is fully responsive and mobile-friendly