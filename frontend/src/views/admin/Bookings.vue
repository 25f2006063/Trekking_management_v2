<template>
  <div>
    <h2>All Bookings</h2>

    <table v-if="bookings.length" border="1" cellpadding="10">
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

    <p v-else>No bookings found</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      bookings: []
    };
  },

  mounted() {
    this.fetchBookings();
  },

  methods: {
    async fetchBookings() {
      try {
        
        const token = localStorage.getItem("token");

        const res = await axios.get(
          "http://127.0.0.1:5000/api/admin/bookings",
          {
            headers: {
              Authorization: `Bearer ${token}` // 🔥 THIS FIXES 401
            }
          }
        );

        this.bookings = res.data;
      } catch (err) {
        console.error("Error fetching bookings:", err);
      }
    }
  }
};
</script>