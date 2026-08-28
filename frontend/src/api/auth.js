import apiClient from "./client";

export async function loginUser(email, password) {
  const response = await apiClient.post("/auth/login", {
    email,
    password,
  });

  return response.data;
}

export async function registerUser(payload) {
  const response = await apiClient.post("/auth/register", payload);
  return response.data;
}

export async function getCurrentUser() {
  const response = await apiClient.get("/auth/me");
  return response.data;
}

export function saveAuthTokens(tokens) {
  localStorage.setItem(
    "bhudrishti_access_token",
    tokens.access_token
  );

  localStorage.setItem(
    "bhudrishti_refresh_token",
    tokens.refresh_token
  );
}

export function clearAuthTokens() {
  localStorage.removeItem("bhudrishti_access_token");
  localStorage.removeItem("bhudrishti_refresh_token");
}

export function getStoredAccessToken() {
  return localStorage.getItem("bhudrishti_access_token");
}
