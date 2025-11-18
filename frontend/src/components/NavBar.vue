<template>
  <header class="navbar">
    <div class="nav-left" @click="$router.push('/')">
      <span class="logo">YashPanel</span>
    </div>
    <nav class="nav-right">
      <router-link to="/" class="link">Home</router-link>
      <a href="#services" v-if="$route.path === '/'" class="link">Services</a>
      <a href="#faq" v-if="$route.path === '/'" class="link">FAQ</a>
      <router-link v-if="!store.user" to="/login" class="btn ghost">Login</router-link>
      <router-link v-if="!store.user" to="/register" class="btn primary">Register</router-link>

      <template v-else>
        <router-link to="/dashboard" class="link">{{ store.user.name }}</router-link>
        <router-link v-if="store.user.isAdmin" to="/admin" class="link">Admin</router-link>
        <button class="btn ghost" @click="handleLogout">Logout</button>
      </template>
    </nav>
  </header>
</template>

<script setup>
import { inject } from "vue";

const store = inject("store");
const api = inject("api");

const handleLogout = async () => {
  try {
    await api.logout();
    store.user = null;
    window.location.href = "/";
  } catch (e) {
    console.error(e);
  }
};
</script>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 10;
  background: #ffffffdd;
  backdrop-filter: blur(8px);
  border-bottom: 1px solid #e2e4f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.7rem 1.5rem;
}

.logo {
  font-weight: 700;
  font-size: 1.3rem;
  color: #4b5cff;
  cursor: pointer;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.link {
  text-decoration: none;
  color: #444;
  font-size: 0.95rem;
}

.link.router-link-active {
  color: #4b5cff;
}

.btn {
  border-radius: 999px;
  padding: 0.4rem 0.9rem;
  font-size: 0.9rem;
  cursor: pointer;
  border: 1px solid transparent;
  transition: transform 0.08s ease, box-shadow 0.08s ease, background 0.1s;
}

.btn.primary {
  background: #4b5cff;
  color: white;
  box-shadow: 0 4px 10px rgba(75, 92, 255, 0.3);
}

.btn.primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 14px rgba(75, 92, 255, 0.4);
}

.btn.ghost {
  background: #f4f5fb;
  border-color: #d0d2e6;
}

.btn.ghost:hover {
  background: #e6e8f5;
}
</style>
