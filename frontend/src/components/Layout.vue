<template>
  <div class="layout">
    <div class="sidebar">
      <h2>TrekApp</h2>

      <router-link to="/dashboard">Dashboard</router-link>
      <router-link to="/treks">Treks</router-link>
      <router-link to="/">Logout</router-link>
    </div>

    <div class="content">
      <!-- THIS IS THE FIX -->
      <router-view />
    </div>
  </div>
</template>

<style>
.layout {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 220px;
  background: #1e293b;
  color: white;
  padding: 20px;
}

.sidebar a {
  display: block;
  color: white;
  margin: 10px 0;
  text-decoration: none;
}

.content {
  flex: 1;
  padding: 20px;
  background: #f5f7f6;
}
</style>