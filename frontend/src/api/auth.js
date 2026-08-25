import api from "./client";

export async function register(username, email, password) {
  const res = await api.post("/api/v1/auth/register", {
    username,
    email,
    password,
  });
  return res.data;
}

export async function login(email, password) {
  const res = await api.post("/api/v1/auth/login", { email, password });
  sessionStorage.setItem("token", res.data.access_token);
  return res.data;
}

export function logout() {
  sessionStorage.removeItem("token");
}

export function isLoggedIn() {
  return Boolean(sessionStorage.getItem("token"));
}