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

async function loginUser(email, password) {
  const url = `${API_BASE}/login`;
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || "Login failed");
  }
  const data = await res.json();
  if (!data || !data.access_token) {
    throw new Error("Missing access_token in response");
  }
  setCookie("token", data.access_token, 60 * 60 * 4);
}

function hasToken() {
  return getCookie("token") !== "";
}

function requireAuthOrRedirect() {
  if (!hasToken()) {
    window.location.href = "index.html";
  }
}

function onDomReady(fn) {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", fn);
  } else {
    fn();
  }
}

onDomReady(() => {
  const loginForm = document.getElementById("login-form");
  if (loginForm) {
    loginForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const email = document.getElementById("email").value.trim();
      const password = document.getElementById("password").value;
      const errorBox = document.getElementById("login-error");
      errorBox.textContent = "";
      if (!email || !password) {
        errorBox.textContent = "Please enter email and password.";
        return;
      }
      try {
        await loginUser(email, password);
        window.location.href = "index.html";
      } catch (err) {
        errorBox.textContent = String(err.message || err);
      }
    });
  }

  const addReviewLink = document.getElementById("add-review-link");
  if (addReviewLink && !hasToken()) {
    addReviewLink.setAttribute("href", "login.html");
  }
});