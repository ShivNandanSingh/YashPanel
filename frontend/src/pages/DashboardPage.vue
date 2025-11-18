<template>
  <div v-if="!store.loadingUser">
    <div v-if="!store.user">
      <p>You must be logged in.</p>
      <router-link to="/login">Go to login</router-link>
    </div>
    <div v-else>
      <section class="top">
        <div class="welcome">
          <h2>Welcome, {{ store.user.name }}</h2>
          <p>Manage your demo balance and place mock orders.</p>
        </div>
        <div class="balance-card">
          <p>Current Balance</p>
          <h2>₹ {{ store.user.balance.toFixed(2) }}</h2>
          <button class="btn ghost" @click="requestTopup">
            Request Balance Top-up
          </button>
        </div>
      </section>

      <section class="section">
        <h3>Available Services</h3>
        <table class="table">
          <thead>
            <tr>
              <th>Service</th>
              <th>Description</th>
              <th>Rate / 1000</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="svc in services" :key="svc.id">
              <td>{{ svc.name }}</td>
              <td>{{ svc.description }}</td>
              <td>₹ {{ svc.ratePer1000 }}</td>
              <td><span class="badge">Active</span></td>
            </tr>
          </tbody>
        </table>
      </section>

      <section class="section">
        <h3>Place Order</h3>
        <form @submit.prevent="submitOrder" class="card">
          <div class="field">
            <label>Service</label>
            <select v-model="orderForm.serviceId">
              <option disabled value="">Select service</option>
              <option v-for="svc in services" :key="svc.id" :value="svc.id">
                {{ svc.name }}
              </option>
            </select>
          </div>
          <div class="field">
            <label>Quantity</label>
            <input type="number" v-model.number="orderForm.quantity" min="1" />
          </div>
          <div class="field">
            <label>Target (URL / Username)</label>
            <input v-model="orderForm.target" type="text" />
          </div>
          <p class="total">
            Total price:
            <b>₹ {{ totalPrice.toFixed(2) }}</b>
          </p>
          <button class="btn primary" :disabled="placing">
            {{ placing ? "Placing..." : "Place Order" }}
          </button>
          <p v-if="orderError" class="error">{{ orderError }}</p>
          <p v-if="orderSuccess" class="success">{{ orderSuccess }}</p>
        </form>
        <router-link to="/orders" class="small-link">View my orders →</router-link>
      </section>
    </div>
  </div>
</template>

<script setup>
import { inject, onMounted, reactive, ref, computed } from "vue";

const store = inject("store");
const api = inject("api");

const services = ref([]);
const orderForm = reactive({
  serviceId: "",
  quantity: 1000,
  target: ""
});
const placing = ref(false);
const orderError = ref("");
const orderSuccess = ref("");

onMounted(async () => {
  try {
    const s = await api.getServices();
    services.value = s.services;
  } catch (e) {
    console.error(e);
  }

  if (!store.user) {
    // try re-fetch user
    try {
      const m = await api.getMe();
      store.user = m.user;
    } catch {}
  }
});

const totalPrice = computed(() => {
  const svc = services.value.find((s) => s.id === orderForm.serviceId);
  const quantity = Number(orderForm.quantity) || 0;
  if (!svc || quantity <= 0) return 0;
  return (svc.ratePer1000 * quantity) / 1000;
});

const requestTopup = () => {
  alert(
    "Demo: In a real panel, this would open a payment/top-up modal. For now, you can manually edit balance in backend or via admin."
  );
};

const submitOrder = async () => {
  orderError.value = "";
  orderSuccess.value = "";

  if (!orderForm.serviceId || !orderForm.quantity || !orderForm.target.trim()) {
    orderError.value = "All fields are required.";
    return;
  }

  if (orderForm.quantity <= 0) {
    orderError.value = "Quantity must be positive.";
    return;
  }

  placing.value = true;
  try {
    const data = await api.createOrder({
      serviceId: orderForm.serviceId,
      quantity: orderForm.quantity,
      target: orderForm.target
    });
    store.user.balance = data.balance;
    orderSuccess.value = "Order placed successfully!";
  } catch (e) {
    orderError.value = e.message || "Failed to place order";
  } finally {
    placing.value = false;
  }
};
</script>

<style scoped>
.top {
  display: flex;
  flex-wrap: wrap;
  gap: 1.2rem;
  align-items: stretch;
}

.welcome {
  flex: 2;
}

.balance-card {
  flex: 1;
  background: white;
  border-radius: 1rem;
  padding: 1rem;
  box-shadow: 0 6px 18px rgba(15, 23, 42, 0.08);
}

.balance-card p {
  margin: 0;
  font-size: 0.9rem;
  color: #555;
}

.balance-card h2 {
  margin: 0.4rem 0 0.7rem;
}

.section {
  margin-top: 2rem;
}

.table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
}

th,
td {
  padding: 0.6rem 0.75rem;
  font-size: 0.9rem;
  border-bottom: 1px solid #e5e7f1;
}

th {
  text-align: left;
  background: #f5f6ff;
}

.badge {
  background: #e0fbea;
  color: #15803d;
  border-radius: 999px;
  padding: 0.15rem 0.6rem;
  font-size: 0.75rem;
}

.card {
  background: white;
  border-radius: 1rem;
  padding: 1rem;
  box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
}

.field {
  margin-bottom: 0.7rem;
}

label {
  display: block;
  font-size: 0.85rem;
  margin-bottom: 0.18rem;
}

select,
input {
  width: 100%;
  padding: 0.4rem 0.6rem;
  border-radius: 0.5rem;
  border: 1px solid #ccd0e5;
  font-size: 0.9rem;
}

.total {
  font-size: 0.9rem;
  margin: 0.4rem 0 0.8rem;
}

.error {
  color: #e11d48;
  font-size: 0.85rem;
  margin-top: 0.4rem;
}

.success {
  color: #16a34a;
  font-size: 0.85rem;
  margin-top: 0.4rem;
}

.small-link {
  display: inline-block;
  margin-top: 0.7rem;
  font-size: 0.9rem;
  color: #4b5cff;
}

.btn.primary {
  border-radius: 999px;
  border: none;
  padding: 0.45rem 1.2rem;
  color: white;
  background: #4b5cff;
  cursor: pointer;
}

.btn.ghost {
  border-radius: 999px;
  border: 1px solid #d0d2e6;
  padding: 0.4rem 0.9rem;
  background: #f4f5fb;
  cursor: pointer;
}
</style>
