<template>
  <Layout>
    <h2>Dashboard</h2>

    <div class="cards">
      <div class="card">Total Treks: 25</div>
      <div class="card">My Bookings: 3</div>
      <div class="card">Upcoming: 1</div>
    </div>
  </Layout>
</template>

<script setup>
import Layout from "../components/Layout.vue";
</script>

<style>
.cards {
  display: flex;
  gap: 20px;
}

.card {
  background: white;
  padding: 20px;
  border-radius: 10px;
}
</style>