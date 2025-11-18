<template>
  <div class="app">
    <NavBar />
    <main class="main">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import NavBar from "./components/NavBar.vue";
</script>

<style>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.app {
  min-height: 100vh;
  background: #f4f5fb;
  color: #222;
}

.main {
  max-width: 1100px;
  margin: 0 auto;
  padding: 1.5rem;
}
</style>
