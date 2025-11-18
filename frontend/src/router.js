import { createRouter, createWebHistory } from "vue-router";
import LandingPage from "./pages/LandingPage.vue";
import RegisterPage from "./pages/RegisterPage.vue";
import LoginPage from "./pages/LoginPage.vue";
import DashboardPage from "./pages/DashboardPage.vue";
import OrdersPage from "./pages/OrdersPage.vue";
import AdminPage from "./pages/AdminPage.vue";

const routes = [
  { path: "/", name: "home", component: LandingPage },
  { path: "/register", name: "register", component: RegisterPage },
  { path: "/login", name: "login", component: LoginPage },
  { path: "/dashboard", name: "dashboard", component: DashboardPage },
  { path: "/orders", name: "orders", component: OrdersPage },
  { path: "/admin", name: "admin", component: AdminPage }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
