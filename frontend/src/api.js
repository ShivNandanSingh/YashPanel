// const API_URL = "http://localhost:5000";
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";

async function apiFetch(path, options = {}) {
  const res = await fetch(API_URL + path, {
    credentials: "include", // important for session cookie
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    },
    ...options
  });

  const text = await res.text();
  let data;
  try {
    data = text ? JSON.parse(text) : {};
  } catch {
    data = { raw: text };
  }

  if (!res.ok) {
    const err = (data && data.error) || res.statusText || "Error";
    throw new Error(err);
  }
  return data;
}

export default {
  getMe() {
    return apiFetch("/api/me");
  },
  register(payload) {
    return apiFetch("/api/register", {
      method: "POST",
      body: JSON.stringify(payload)
    });
  },
  login(payload) {
    return apiFetch("/api/login", {
      method: "POST",
      body: JSON.stringify(payload)
    });
  },
  logout() {
    return apiFetch("/api/logout", { method: "POST" });
  },
  getServices() {
    return apiFetch("/api/services");
  },
  getOrders() {
    return apiFetch("/api/orders");
  },
  createOrder(payload) {
    return apiFetch("/api/orders", {
      method: "POST",
      body: JSON.stringify(payload)
    });
  },
  simulateOrder() {
    return apiFetch("/api/orders/simulate", { method: "POST" });
  },
  adminGetUsers() {
    return apiFetch("/api/admin/users");
  },
  adminGetOrders() {
    return apiFetch("/api/admin/orders");
  },
  adminUpdateOrder(id, status) {
    return apiFetch(`/api/admin/orders/${id}`, {
      method: "PATCH",
      body: JSON.stringify({ status })
    });
  }
};
