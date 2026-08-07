<template>
  <Layout>
    <h2>Browse Treks</h2>

    <div class="grid">
      <div class="card" v-for="trek in treks" :key="trek.id">
        <img src="https://picsum.photos/300/150" />
        <h3>{{ trek.name }}</h3>
        <p>{{ trek.location }}</p>

        <button @click="book(trek.id)">Book Now</button>
      </div>
    </div>
  </Layout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Layout from "../components/Layout.vue";
import API from "../api";

const treks = ref([]);

onMounted(async () => {
  const res = await API.get("/user/treks");
  treks.value = res.data;
});

const book = async (id) => {
  await API.post(`/user/book/${id}`);
  alert("Booked!");
};
</script>

<style>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.card {
  background: white;
  border-radius: 10px;
  overflow: hidden;
}

img {
  width: 100%;
}

button {
  margin: 10px;
  background: green;
  color: white;
  padding: 8px;
  border: none;
}
</style>