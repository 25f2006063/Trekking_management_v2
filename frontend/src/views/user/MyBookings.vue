<template>
  <div class="container mt-4">
    <h2>My Bookings</h2>

    <table class="table table-bordered mt-3">
      <thead>
        <tr>
          <th>Trek</th>
          <th>Location</th>
          <th>Dates</th>
          <th>Status</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="b in bookings" :key="b.id">
          <td>{{ b.trek_title }}</td>
          <td>{{ b.trek_location }}</td>
          <td>
            {{ formatDate(b.start_date) }} -
            {{ formatDate(b.end_date) }}
          </td>

          <td>
            <span class="badge bg-info">
              {{ b.status }}
            </span>
          </td>

        
        </tr>

        <tr v-if="bookings.length === 0">
          <td colspan="5" class="text-center">
            No bookings
          </td>
        </tr>
      </tbody>
    </table>
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

  methods: {
    async fetchBookings() {
      const token = localStorage.getItem("token");

      const res = await axios.get(
        "http://127.0.0.1:5000/api/user/bookings",
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      this.bookings = res.data;
    },

    async cancelBooking(trekId) {
      const token = localStorage.getItem("token");

      await axios.delete(
        `http://127.0.0.1:5000/api/bookings/${trekId}`,
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      alert("Cancelled!");
      this.fetchBookings();
    },

    formatDate(date) {
      return new Date(date).toLocaleDateString();
    }
  },

  mounted() {
    this.fetchBookings();
  }
};
</script>