<template>
  <div class="hero">
    <div class="overlay">
      <div class="content text-center">
        <h1 class="title">Explore the World with Trekker</h1>
        <p class="subtitle">
          Discover amazing trekking adventures, book easily, and track your journey.
        </p>

        <div class="mt-4">
          <router-link to="/user/treks" class="btn btn-success btn-lg me-3">
            Explore Treks
          </router-link>

          <router-link to="/login" class="btn btn-outline-light btn-lg">
            Login
          </router-link>
          
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.hero {
  height: 100vh;
  background: url("../assets/bg.png") no-repeat center center/cover;
  position: relative;
}

.overlay {
  background: rgba(0, 0, 0, 0.6);
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.content {
  max-width: 700px;
}

.title {
  font-size: 3rem;
  font-weight: bold;
  color: #fff;
}

.subtitle {
  color: #ddd;
  font-size: 1.2rem;
}

.btn {
  padding: 12px 30px;
  font-size: 1.1rem;
}
</style>