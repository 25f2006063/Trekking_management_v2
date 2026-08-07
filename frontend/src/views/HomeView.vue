<template>
  <div>

    <!-- HERO SECTION -->
    <section class="hero" :style="heroStyle">
      
      <div class="overlay">
        <h1 class="brand">Trekker</h1>

        <h2>Find Your Next Trek</h2>
        <p>Explore, Book and Manage Treks Easily</p>

        <div class="buttons">
          <router-link to="/login" class="btn login">Login</router-link>
          <router-link to="/register" class="btn btn2">Register</router-link>
        </div>
      </div>

    </section>

    <!-- FEATURES -->
    <section class="features">
      <h2>Why Use Trekker?</h2>

      <div class="feature-grid">
        <div class="card">
          <h3>Explore Treks</h3>
          <p>Discover treks based on location & difficulty</p>
        </div>

        <div class="card">
          <h3>Easy Booking</h3>
          <p>Book treks in just one click</p>
        </div>

        <div class="card">
          <h3>Track History</h3>
          <p>View all your trekking experiences</p>
        </div>
      </div>
    </section>

  </div>
</template>

<script>
import bg from "@/assets/bg.png";   // ✅ THIS IS THE KEY FIX

export default {
  data() {
    return {
      heroStyle: {
        backgroundImage: `url(${bg})`
      }
    }
  }
}
</script>

<style scoped>

/* HERO */
.hero {
  height: 100vh;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

/* OVERLAY */
.overlay {
  height: 100%;
  background: linear-gradient(to right, rgba(0,0,0,0.7), rgba(0,0,0,0.2));
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-left: 80px;
  color: white;
}

/* BRAND */
.brand {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 10px;
  opacity: 0.9;
}

/* TEXT */
h2 {
  font-size: 48px;
  margin: 10px 0;
}

/* BUTTONS */
.buttons {
  margin-top: 20px;
}

.btn {
  padding: 10px 20px;
  margin-right: 10px;
  border-radius: 6px;
  text-decoration: none;
  color: white;
  font-weight: bold;
}

.login { background: green; }
.btn2 { background: blue; }

/* FEATURES */
.features {
  padding: 60px;
  text-align: center;
}

.feature-grid {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.card {
  padding: 20px;
  background: #f5f5f5;
  border-radius: 10px;
  width: 220px;
}

</style>