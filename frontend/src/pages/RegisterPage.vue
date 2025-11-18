<template>
  <div class="auth-container">
    <h2>Create an account</h2>
    <form @submit.prevent="handleSubmit" class="card">
      <div class="field">
        <label>Name</label>
        <input v-model="form.name" type="text" />
        <p v-if="errors.name" class="error">{{ errors.name }}</p>
      </div>

      <div class="field">
        <label>Email</label>
        <input v-model="form.email" type="email" />
        <p v-if="errors.email" class="error">{{ errors.email }}</p>
      </div>

      <div class="field">
        <label>Password</label>
        <input v-model="form.password" type="password" />
        <p v-if="errors.password" class="error">{{ errors.password }}</p>
      </div>

      <div class="field">
        <label>Confirm Password</label>
        <input v-model="form.confirmPassword" type="password" />
        <p v-if="errors.confirmPassword" class="error">{{ errors.confirmPassword }}</p>
      </div>

      <button class="btn primary" :disabled="loading">
        {{ loading ? "Creating..." : "Register" }}
      </button>

      <p v-if="serverError" class="error server">{{ serverError }}</p>

      <p class="small">
        Already have an account?
        <router-link to="/login">Login</router-link>
      </p>
    </form>
  </div>
</template>

<script setup>
import { inject, reactive, ref } from "vue";
import { useRouter } from "vue-router";

const api = inject("api");
const router = useRouter();

const form = reactive({
  name: "",
  email: "",
  password: "",
  confirmPassword: ""
});

const errors = reactive({});
const loading = ref(false);
const serverError = ref("");

function validate() {
  // clear previous errors
  Object.keys(errors).forEach((k) => delete errors[k]);

  if (!form.name.trim()) errors.name = "Name is required";

  if (!form.email.trim()) {
    errors.email = "Email is required";
  } else if (!form.email.includes("@")) {
    errors.email = "Invalid email";
  }

  if (!form.password) {
    errors.password = "Password is required";
  } else if (form.password.length < 6) {
    errors.password = "Password must be at least 6 characters";
  }

  if (!form.confirmPassword) {
    errors.confirmPassword = "Please confirm your password";
  } else if (form.password !== form.confirmPassword) {
    errors.confirmPassword = "Passwords do not match";
  }

  return Object.keys(errors).length === 0;
}

const handleSubmit = async () => {
  serverError.value = "";
  if (!validate()) return;

  loading.value = true;
  try {
    await api.register({
      name: form.name,
      email: form.email,
      password: form.password
    });
    router.push("/login");
  } catch (e) {
    serverError.value = e.message || "Registration failed";
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

h2 {
  text-align: center;
  margin-bottom: 1rem;
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
  font-size: 0.8rem;
  margin-top: 0.15rem;
}

.server {
  margin-top: 0.6rem;
}

.small {
  margin-top: 0.8rem;
  font-size: 0.85rem;
  text-align: center;
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
  transition: background 0.1s ease, transform 0.08s ease,
    box-shadow 0.08s ease;
}

.btn.primary:hover {
  background: #3b4ae0;
  transform: translateY(-1px);
  box-shadow: 0 6px 14px rgba(59, 74, 224, 0.4);
}

.btn.primary:disabled {
  opacity: 0.7;
  cursor: default;
  box-shadow: none;
}
</style>
