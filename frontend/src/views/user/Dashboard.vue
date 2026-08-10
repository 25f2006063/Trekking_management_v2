<template>
  <div class="container mt-4">
    <h2>User Dashboard</h2>

    <div class="row mt-3">
      <div class="col-md-4">
        <div class="card p-3 text-center">
          <h5>Total Treks</h5>
          <h3>{{ totalTreks }}</h3>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card p-3 text-center">
          <h5>My Bookings</h5>
          <h3>{{ myBookings }}</h3>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      totalTreks: 0,
      myBookings: 0
    };
  },

  methods: {
    async fetchStats() {
      try {
        const token = localStorage.getItem("token");

        // ✅ GET ALL TREKS
        const treksRes = await axios.get(
          "http://127.0.0.1:5000/api/user/treks",
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        );

        // ✅ GET MY BOOKINGS
        const bookingsRes = await axios.get(
          "http://127.0.0.1:5000/api/user/bookings",
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        );

        // ✅ UPDATE VALUES
        this.totalTreks = treksRes.data.length;
        this.myBookings = bookingsRes.data.length;

      } catch (err) {
        console.error("Dashboard error:", err);
      }
    }
  },

  mounted() {
    this.fetchStats();
  }
};
</script>