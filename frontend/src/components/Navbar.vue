<template>
  <nav class="navbar">
    <div class="logo">Trekker</div>

    <ul class="nav-links">
      <li><router-link to="/">Home</router-link></li>
      <li><router-link to="/dashboard">Dashboard</router-link></li>
      <li><router-link to="/treks">Treks</router-link></li>
      <li><router-link to="/about">About</router-link></li>
    </ul>

    <div class="auth-buttons">
      <router-link to="/login" class="btn login">Login</router-link>
      <router-link to="/register" class="btn register">Register</router-link>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  width: 100%;
  height: 70px;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(10px);
  color: white;

  display: flex;
  align-items: center;
  justify-content: space-between;

  padding: 0 40px;
  z-index: 1000;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  color: #00ff88;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 25px;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-size: 16px;
}

.nav-links a:hover {
  color: #00ff88;
}

.auth-buttons {
  display: flex;
  gap: 10px;
}

.btn {
  padding: 6px 14px;
  border-radius: 6px;
  text-decoration: none;
  font-size: 14px;
}

.login {
  background: green;
  color: white;
}

.register {
  background: blue;
  color: white;
}
</style>