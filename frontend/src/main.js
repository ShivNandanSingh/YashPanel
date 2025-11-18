import { createApp, reactive } from "vue";
import App from "./App.vue";
import router from "./router";
import api from "./api";

const app = createApp(App);

// simple global store
const store = reactive({
  user: null,
  loadingUser: true
});

async function init() {
  try {
    const data = await api.getMe();
    store.user = data.user;
  } catch (e) {
    console.error(e);
  } finally {
    store.loadingUser = false;
  }
}

app.provide("store", store);
app.provide("api", api);

init();

app.use(router);
app.mount("#app");
