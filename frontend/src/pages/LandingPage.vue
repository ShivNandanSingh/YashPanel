<template>
  <div>
    <section class="hero">
      <div class="hero-text">
        <h1>Fast, Simple Social Growth Dashboard</h1>
        <p>
          A panel where users can sign up, add balance, and place mock orders
          for social growth services. <b>Demo only, no real social APIs used.</b>
        </p>
        <button class="btn primary" @click="$router.push('/register')">
          Get Started
        </button>
      </div>
      <div class="hero-card">
        <h3>Demo Summary</h3>
        <ul>
          <li>Register & log in as a normal user</li>
          <li>Admin demo: admin@example.com / Admin@123</li>
          <li>Place mock orders with fake services</li>
        </ul>
      </div>
    </section>

    <section id="how" class="section">
      <h2>How It Works</h2>
      <div class="grid">
        <div class="card">
          <h3>1. Register & Log in</h3>
          <p>Create a free demo account in seconds.</p>
        </div>
        <div class="card">
          <h3>2. Add Funds (Demo)</h3>
          <p>We simulate balance on the backend for testing.</p>
        </div>
        <div class="card">
          <h3>3. Place Orders</h3>
          <p>Select any mock service and submit your details.</p>
        </div>
        <div class="card">
          <h3>4. Track Orders</h3>
          <p>See your order history and statuses instantly.</p>
        </div>
      </div>
    </section>

    <section id="services" class="section">
      <h2>Why Choose YashPanel?</h2>
      <div class="grid">
        <div class="card">
          <h3>Instant Demo Orders</h3>
          <p>Orders are created instantly so you can test flows.</p>
        </div>
        <div class="card">
          <h3>Simple Interface</h3>
          <p>Clean, card-based UI inspired by real SMM panels.</p>
        </div>
        <div class="card">
          <h3>Mock Data Only</h3>
          <p>No real followers, likes, or APIs. Safe for learning.</p>
        </div>
        <div class="card">
          <h3>Educational Project</h3>
          <p>Perfect reference for full-stack learning with Vue + Flask.</p>
        </div>
      </div>
    </section>

    <section id="faq" class="section">
      <h2>FAQ</h2>
      <div class="faq">
        <details>
          <summary>Is YashPanel a real SMM service?</summary>
          <p>No. This is a demo panel for educational purposes only.</p>
        </details>
        <details>
          <summary>Will it affect my social media account?</summary>
          <p>No. It does not call any social media APIs or perform real actions.</p>
        </details>
        <details>
          <summary>Can I use this code in my own project?</summary>
          <p>
            Yes, you can adapt it as a starting point. Always respect platform
            terms of service.
          </p>
        </details>
        <details>
          <summary>How do I access the admin panel?</summary>
          <p>
            Log in with <b>admin@example.com</b> and password <b>Admin@123</b>,
            then open the Admin page.
          </p>
        </details>
        <details>
          <summary>Where is data stored?</summary>
          <p>
            In-memory lists on the Flask backend (no real database; resets on restart).
          </p>
        </details>
      </div>
    </section>
  </div>
</template>

<script setup></script>

<style scoped>
.hero {
  display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(0, 1.4fr);
  gap: 2rem;
  padding: 2rem 0 1rem;
  align-items: center;
}

.hero-text h1 {
  font-size: 2.5rem;
  margin-bottom: 0.7rem;
}

.hero-text p {
  font-size: 1rem;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.hero-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.1);
}

.hero-card h3 {
  margin-top: 0;
}

.hero-card ul {
  padding-left: 1.2rem;
}

.section {
  margin-top: 2.5rem;
}

.section h2 {
  margin-bottom: 1rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 1.1rem;
}

.card {
  background: white;
  padding: 1.1rem;
  border-radius: 1rem;
  box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
  transition: transform 0.1s ease, box-shadow 0.1s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 26px rgba(15, 23, 42, 0.12);
}

.faq details {
  background: white;
  margin-bottom: 0.7rem;
  padding: 0.8rem 1rem;
  border-radius: 0.8rem;
  cursor: pointer;
  box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
}

.faq summary {
  font-weight: 500;
}

.btn.primary {
  border-radius: 999px;
  padding: 0.5rem 1.4rem;
  font-size: 0.95rem;
  background: #4b5cff;
  color: white;
  border: none;
  cursor: pointer;
}

@media (max-width: 768px) {
  .hero {
    grid-template-columns: 1fr;
  }
}
</style>
