<template>
  <div>
    <h2>Admin Panel</h2>
    <p class="small">
      View all users and orders. Change order status for demo.
    </p>

    <div v-if="error" class="error">{{ error }}</div>

    <section class="section">
      <h3>Users</h3>
      <table class="table" v-if="users.length">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Balance (₹)</th>
            <th>Admin</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in users" :key="u.id">
            <td>{{ u.name }}</td>
            <td>{{ u.email }}</td>
            <td>{{ u.balance.toFixed(2) }}</td>
            <td>{{ u.isAdmin ? "Yes" : "No" }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else>No users loaded.</p>
    </section>

    <section class="section">
      <h3>Orders</h3>
      <table class="table" v-if="orders.length">
        <thead>
          <tr>
            <th>ID</th>
            <th>User ID</th>
            <th>Service</th>
            <th>Qty</th>
            <th>Total (₹)</th>
            <th>Status</th>
            <th>Change Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="o in orders" :key="o.id">
            <td class="mono">{{ o.id.slice(0, 8) }}…</td>
            <td class="mono">{{ o.userId.slice(0, 8) }}…</td>
            <td>{{ o.serviceName }}</td>
            <td>{{ o.quantity }}</td>
            <td>{{ o.totalPrice.toFixed(2) }}</td>
            <td>
              <span class="badge" :class="o.status">{{ o.status }}</span>
            </td>
            <td>
              <select v-model="o._newStatus">
                <option value="pending">pending</option>
                <option value="processing">processing</option>
                <option value="completed">completed</option>
                <option value="cancelled">cancelled</option>
              </select>
              <button class="btn small" @click="updateStatus(o)">Save</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>No orders yet.</p>
    </section>
  </div>
</template>

<script setup>
import { inject, onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const api = inject("api");
const store = inject("store");
const router = useRouter();

const users = ref([]);
const orders = ref([]);
const error = ref("");

onMounted(async () => {
  try {
    const m = await api.getMe();
    store.user = m.user;
    if (!store.user || !store.user.isAdmin) {
      router.push("/login");
      return;
    }
    const u = await api.adminGetUsers();
    users.value = u.users || [];
    const o = await api.adminGetOrders();
    orders.value = (o.orders || []).map((ord) => ({
      ...ord,
      _newStatus: ord.status
    }));
  } catch (e) {
    error.value = e.message || "Failed to load admin data.";
  }
});

async function updateStatus(order) {
  try {
    await api.adminUpdateOrder(order.id, order._newStatus);
    order.status = order._newStatus;
  } catch (e) {
    alert(e.message || "Update failed");
  }
}
</script>

<style scoped>
.small {
  font-size: 0.9rem;
  color: #555;
}

.section {
  margin-top: 1.8rem;
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

select {
  font-size: 0.8rem;
  padding: 0.25rem 0.4rem;
  border-radius: 0.4rem;
  border: 1px solid #ccd0e5;
}

.btn.small {
  margin-left: 0.4rem;
  border-radius: 999px;
  padding: 0.25rem 0.6rem;
  border: none;
  background: #4b5cff;
  color: white;
  font-size: 0.75rem;
  cursor: pointer;
}

.error {
  color: #e11d48;
  font-size: 0.9rem;
}
</style>
