<template>
  <div>
    <h2>My Orders</h2>
    <p class="small">
      View all your mock orders and simulate processing.
    </p>
    <button class="btn ghost" @click="simulate" :disabled="simulating">
      {{ simulating ? "Simulating..." : "Simulate Processing" }}
    </button>
    <p v-if="message" class="info">{{ message }}</p>

    <table v-if="orders.length" class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Service</th>
          <th>Qty</th>
          <th>Target</th>
          <th>Total (₹)</th>
          <th>Status</th>
          <th>Created At</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="o in orders" :key="o.id">
          <td class="mono">{{ o.id.slice(0, 8) }}…</td>
          <td>{{ o.serviceName }}</td>
          <td>{{ o.quantity }}</td>
          <td>{{ o.target }}</td>
          <td>{{ o.totalPrice.toFixed(2) }}</td>
          <td>
            <span class="badge" :class="o.status">{{ o.status }}</span>
          </td>
          <td>{{ o.createdAt }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>No orders yet. Go to the dashboard and place one!</p>
  </div>
</template>

<script setup>
import { inject, onMounted, ref } from "vue";

const api = inject("api");
const store = inject("store");

const orders = ref([]);
const simulating = ref(false);
const message = ref("");

onMounted(async () => {
  if (!store.user) {
    try {
      const m = await api.getMe();
      store.user = m.user;
    } catch {}
  }
  await loadOrders();
});

async function loadOrders() {
  try {
    const data = await api.getOrders();
    orders.value = data.orders || [];
  } catch (e) {
    message.value = e.message;
  }
}

async function simulate() {
  simulating.value = true;
  message.value = "";
  try {
    const data = await api.simulateOrder();
    if (data.order) {
      message.value = `Order ${data.order.id.slice(0, 8)}… marked completed.`;
      await loadOrders();
    } else {
      message.value = data.message || "No pending orders.";
    }
  } catch (e) {
    message.value = e.message || "Simulation failed.";
  } finally {
    simulating.value = false;
  }
}
</script>

<style scoped>
.small {
  font-size: 0.9rem;
  color: #555;
}

.info {
  margin-top: 0.4rem;
  font-size: 0.9rem;
}

.table {
  margin-top: 1rem;
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
}

th,
td {
  padding: 0.55rem 0.7rem;
  border-bottom: 1px solid #e5e7f1;
  font-size: 0.85rem;
}

th {
  text-align: left;
  background: #f5f6ff;
}

.mono {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas,
    "Liberation Mono", "Courier New", monospace;
}

.badge {
  border-radius: 999px;
  padding: 0.1rem 0.5rem;
  font-size: 0.75rem;
  text-transform: capitalize;
}

.badge.pending {
  background: #fef3c7;
  color: #92400e;
}

.badge.processing {
  background: #dbeafe;
  color: #1d4ed8;
}

.badge.completed {
  background: #dcfce7;
  color: #166534;
}

.badge.cancelled {
  background: #fee2e2;
  color: #991b1b;
}

.btn.ghost {
  margin-top: 0.4rem;
  border-radius: 999px;
  padding: 0.4rem 0.9rem;
  border: 1px solid #d0d2e6;
  background: #f4f5fb;
  cursor: pointer;
}
</style>
