<template>
  <div class="auth-container">
    <h2>Login</h2>
    <form @submit.prevent="handleSubmit" class="card">
      <div class="field">
        <label>Email</label>
        <input v-model="email" type="email" />
      </div>
      <div class="field">
        <label>Password</label>
        <input v-model="password" type="password" />
      </div>
      <button class="btn primary" :disabled="loading">
        {{ loading ? "Logging in..." : "Login" }}
      </button>
      <p v-if="error" class="error">{{ error }}</p>
      <p class="small">
        No account yet?
        <router-link to="/register">Register</router-link>
      </p>
    </form>
  </div>
</template>

<script setup>
import { inject, ref } from "vue";
import { useRouter } from "vue-router";

const api = inject("api");
const store = inject("store");
const router = useRouter();

const email = ref("");
const password = ref("");
const loading = ref(false);
const error = ref("");

const handleSubmit = async () => {
  error.value = "";
  loading.value = true;
  try {
    const data = await api.login({
      email: email.value,
      password: password.value
    });
    store.user = data.user;
    router.push("/dashboard");
  } catch (e) {
    error.value = e.message || "Login failed";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 2rem auto;
}

.card {
  background: white;
  padding: 1.3rem;
  border-radius: 1rem;
  box-shadow: 0 6px 18px rgba(15, 23, 42, 0.08);
}

.field {
  margin-bottom: 0.7rem;
}

label {
  display: block;
  font-size: 0.9rem;
  margin-bottom: 0.2rem;
}

input {
  width: 100%;
  padding: 0.45rem 0.6rem;
  border-radius: 0.5rem;
  border: 1px solid #ccd0e5;
  font-size: 0.9rem;
}

input:focus {
  outline: none;
  border-color: #4b5cff;
}

.error {
  color: #e11d48;
  font-size: 0.85rem;
  margin-top: 0.4rem;
}

.small {
  margin-top: 0.8rem;
  font-size: 0.85rem;
}

.btn.primary {
  margin-top: 0.4rem;
  width: 100%;
  background: #4b5cff;
  color: white;
  border-radius: 999px;
  padding: 0.5rem;
  border: none;
  cursor: pointer;
}
</style>
