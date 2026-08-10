<template>
  <div>

    <h2 class="mb-4">Dashboard</h2>

    <!-- Cards -->
    <div class="row">
      <div class="col-md-3" v-for="card in stats" :key="card.title">
        <div class="card p-3 text-center shadow-sm">
          <h6>{{ card.title }}</h6>
          <h3>{{ card.value }}</h3>
        </div>
      </div>
    </div>

    <!-- Recent Bookings -->
    <div class="mt-5">
      <h5>Recent Bookings</h5>

      <table class="table mt-3">
        <thead>
          <tr>
            <th>ID</th>
            <th>User</th>
            <th>Trek</th>
            <th>Date</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="b in bookings" :key="b.id">
            <td>{{ b.id }}</td>
            <td>{{ b.user }}</td>
            <td>{{ b.trek }}</td>
            <td>{{ b.date }}</td>
            <td>{{ b.status }}</td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      stats: [],
      bookings: []
    };
  },

  methods: {
    async loadDashboard() {
      try {
        const res = await axios.get(
          "http://127.0.0.1:5000/api/admin/dashboard",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`
            }
          }
        );

        // 🔥 Convert stats object → array for cards
        this.stats = Object.entries(res.data.stats).map(([key, value]) => ({
          title: key,
          value: value
        }));

        this.bookings = res.data.recent_bookings;

      } catch (err) {
        console.error(err);
      }
    }
  },

  mounted() {
    this.loadDashboard();
  }
};
</script>