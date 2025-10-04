const API_BASE = "http://127.0.0.1:5000/api";

function setCookie(name, value, maxSeconds) {
  const encoded = encodeURIComponent(value);
  const max = maxSeconds ? `; Max-Age=${maxSeconds}` : "";
  const samesite = "; SameSite=Lax";
  const path = "; Path=/";
  document.cookie = `${name}=${encoded}${max}${samesite}${path}`;
}

function getCookie(name) {
  const items = document.cookie.split(";").map(s => s.trim());
  for (const item of items) {
    if (item.startsWith(name + "=")) {
      return decodeURIComponent(item.substring(name.length + 1));
    }
  }
  return "";
}

function deleteCookie(name) {
  document.cookie = `${name}=; Max-Age=0; Path=/; SameSite=Lax`;
}

function hasToken() {
  return getCookie("token") !== "";
}

function getAuthHeaders() {
  const token = getCookie("token");
  return token ? { "Authorization": `Bearer ${token}` } : {};
}

function requireAuthOrRedirect() {
  if (!hasToken()) {
    window.location.href = "index.html";
  }
}

function getPlaceIdFromURL() {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get('id');
}

// Task 2: Login functionality
async function loginUser(email, password) {
  const url = `${API_BASE}/v1/auth/login`;
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.error || "Login failed");
  }
  const data = await res.json();
  if (!data || !data.access_token) {
    throw new Error("Missing access_token in response");
  }
  setCookie("token", data.access_token, 60 * 60 * 4);
}

// Task 3: Index page functionality
async function fetchPlaces() {
  try {
    const url = `${API_BASE}/v1/places/`;
    const headers = { "Content-Type": "application/json", ...getAuthHeaders() };
    const res = await fetch(url, { headers });
    
    if (!res.ok) {
      throw new Error(`Failed to fetch places: ${res.statusText}`);
    }
    
    const places = await res.json();
    return places;
  } catch (error) {
    console.error("Error fetching places:", error);
    return [];
  }
}

function displayPlaces(places) {
  const placesContainer = document.getElementById("places");
  if (!placesContainer) return;
  
  placesContainer.innerHTML = "";
  
  places.forEach(place => {
    const placeCard = document.createElement("article");
    placeCard.className = "place-card";
    placeCard.innerHTML = `
      <h3>${place.title || "Unnamed Place"}</h3>
      <p>$${place.price || 0} / night</p>
      <a class="details-button" href="place.html?id=${place.id}">View Details</a>
    `;
    placesContainer.appendChild(placeCard);
  });
}

function setupPriceFilter(places) {
  const priceFilter = document.getElementById("price-filter");
  if (!priceFilter) return;
  
  // Clear existing options except "All"
  priceFilter.innerHTML = '<option value="">All</option>';
  
  // Add price options
  const priceOptions = [10, 50, 100];
  priceOptions.forEach(price => {
    const option = document.createElement("option");
    option.value = price;
    option.textContent = `$${price} or less`;
    priceFilter.appendChild(option);
  });
  
  priceFilter.addEventListener("change", (event) => {
    const maxPrice = event.target.value ? parseFloat(event.target.value) : Infinity;
    const placeCards = document.querySelectorAll(".place-card");
    
    placeCards.forEach(card => {
      const priceText = card.querySelector("p").textContent;
      const price = parseFloat(priceText.match(/\$(\d+)/)[1]);
      
      if (price <= maxPrice) {
        card.style.display = "block";
      } else {
        card.style.display = "none";
      }
    });
  });
}

function checkAuthentication() {
  const token = getCookie("token");
  const loginLink = document.querySelector(".login-button");
  
  if (!token && loginLink) {
    loginLink.style.display = "block";
  } else if (token && loginLink) {
    loginLink.style.display = "none";
  }
  
  return token;
}

// Task 4: Place details functionality
async function fetchPlaceDetails(placeId) {
  try {
    const url = `${API_BASE}/v1/places/${placeId}`;
    const headers = { "Content-Type": "application/json", ...getAuthHeaders() };
    const res = await fetch(url, { headers });
    
    if (!res.ok) {
      throw new Error(`Failed to fetch place details: ${res.statusText}`);
    }
    
    return await res.json();
  } catch (error) {
    console.error("Error fetching place details:", error);
    return null;
  }
}

async function fetchPlaceReviews(placeId) {
  try {
    const url = `${API_BASE}/v1/reviews/`;
    const headers = { "Content-Type": "application/json", ...getAuthHeaders() };
    const res = await fetch(url, { headers });
    
    if (!res.ok) {
      throw new Error(`Failed to fetch reviews: ${res.statusText}`);
    }
    
    const allReviews = await res.json();
    // Filter reviews for this specific place
    return allReviews.filter(review => review.place_id === placeId);
  } catch (error) {
    console.error("Error fetching reviews:", error);
    return [];
  }
}

async function fetchUserDetails(userId) {
  try {
    const url = `${API_BASE}/v1/users/${userId}`;
    const headers = { "Content-Type": "application/json", ...getAuthHeaders() };
    const res = await fetch(url, { headers });
    
    if (!res.ok) {
      return { first_name: "Unknown", last_name: "User" };
    }
    
    return await res.json();
  } catch (error) {
    console.error("Error fetching user details:", error);
    return { first_name: "Unknown", last_name: "User" };
  }
}

async function displayPlaceDetails(place) {
  if (!place) {
    document.getElementById("place-name").textContent = "Place not found";
    return;
  }
  
  document.getElementById("place-name").textContent = place.title || "Unnamed Place";
  document.getElementById("place-price").textContent = `$${place.price || 0} / night`;
  document.getElementById("place-description").textContent = place.description || "No description available.";
  
  // Fetch and display host details
  if (place.owner_id) {
    const host = await fetchUserDetails(place.owner_id);
    document.getElementById("place-host").textContent = `${host.first_name} ${host.last_name}`;
  } else {
    document.getElementById("place-host").textContent = "Unknown";
  }
  
  // Fetch and display reviews
  const reviews = await fetchPlaceReviews(place.id);
  displayReviews(reviews);
}

function displayReviews(reviews) {
  const reviewsSection = document.getElementById("reviews");
  if (!reviewsSection) return;
  
  // Clear existing reviews
  const existingReviews = reviewsSection.querySelectorAll(".review-card");
  existingReviews.forEach(review => review.remove());
  
  if (reviews.length === 0) {
    const noReviewsMsg = document.createElement("p");
    noReviewsMsg.textContent = "No reviews yet. Be the first to review this place!";
    noReviewsMsg.style.margin = "20px";
    noReviewsMsg.style.color = "var(--muted)";
    reviewsSection.appendChild(noReviewsMsg);
    return;
  }
  
  // Display each review
  reviews.forEach(async (review) => {
    const reviewCard = document.createElement("article");
    reviewCard.className = "review-card";
    
    // Fetch user details for the review
    const user = await fetchUserDetails(review.user_id);
    
    reviewCard.innerHTML = `
      <h4>${review.title || "Review"}</h4>
      <p>by <strong>${user.first_name} ${user.last_name}</strong> • Rating: ${review.rating}/5</p>
      <p>${review.comment || "No comment provided."}</p>
    `;
    
    reviewsSection.appendChild(reviewCard);
  });
}

function setupPlacePage() {
  const token = checkAuthentication();
  const placeId = getPlaceIdFromURL();
  
  if (!placeId) {
    window.location.href = "index.html";
    return;
  }
  
  // Hide add review section if not authenticated
  const addReviewSection = document.querySelector(".add-review");
  const addReviewLink = document.getElementById("add-review-link");
  
  if (!token) {
    if (addReviewSection) {
      addReviewSection.style.display = "none";
    }
    if (addReviewLink) {
      addReviewLink.setAttribute("href", "login.html");
    }
  } else {
    if (addReviewLink && placeId) {
      addReviewLink.setAttribute("href", `add_review.html?id=${placeId}`);
    }
  }
  
  // Fetch and display place details
  fetchPlaceDetails(placeId).then(displayPlaceDetails);
}

// Task 5: Add review functionality
async function submitReview(placeId, reviewData) {
  try {
    const url = `${API_BASE}/v1/reviews/`;
    const headers = {
      "Content-Type": "application/json",
      ...getAuthHeaders()
    };
    
    const reviewPayload = {
      ...reviewData,
      place_id: placeId
    };
    
    const res = await fetch(url, {
      method: "POST",
      headers,
      body: JSON.stringify(reviewPayload)
    });
    
    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      throw new Error(errorData.error || "Failed to submit review");
    }
    
    return await res.json();
  } catch (error) {
    console.error("Error submitting review:", error);
    throw error;
  }
}

function setupReviewPage() {
  const token = checkAuthentication();
  
  if (!token) {
    window.location.href = "index.html";
    return;
  }
  
  const placeId = getPlaceIdFromURL();
  if (!placeId) {
    window.location.href = "index.html";
    return;
  }
  
  const reviewForm = document.getElementById("review-form");
  if (reviewForm) {
    reviewForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      
      const formData = new FormData(reviewForm);
      const reviewData = {
        title: formData.get("title"),
        rating: parseInt(formData.get("rating")),
        comment: formData.get("comment")
      };
      
      try {
        await submitReview(placeId, reviewData);
        alert("Review submitted successfully!");
        reviewForm.reset();
        // Redirect back to place details
        window.location.href = `place.html?id=${placeId}`;
      } catch (error) {
        alert("Failed to submit review: " + error.message);
      }
    });
  }
}

// Initialize page based on current location
function onDomReady(fn) {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", fn);
  } else {
    fn();
  }
}

onDomReady(() => {
  const currentPage = window.location.pathname.split('/').pop();
  
  switch (currentPage) {
    case "index.html":
    case "":
      // Task 3: Index page
      checkAuthentication();
      fetchPlaces().then(places => {
        displayPlaces(places);
        setupPriceFilter(places);
      });
      break;
      
    case "login.html":
      // Task 2: Login page
      const loginForm = document.getElementById("login-form");
      if (loginForm) {
        loginForm.addEventListener("submit", async (event) => {
          event.preventDefault();
          const email = document.getElementById("email").value.trim();
          const password = document.getElementById("password").value;
          const errorBox = document.getElementById("login-error");
          
          if (errorBox) errorBox.textContent = "";
          
          if (!email || !password) {
            if (errorBox) errorBox.textContent = "Please enter email and password.";
            return;
          }
          
          try {
            await loginUser(email, password);
            window.location.href = "index.html";
          } catch (err) {
            if (errorBox) errorBox.textContent = String(err.message || err);
          }
        });
      }
      break;
      
    case "place.html":
      // Task 4: Place details page
      setupPlacePage();
      break;
      
    case "add_review.html":
      // Task 5: Add review page
      setupReviewPage();
      break;
  }
});