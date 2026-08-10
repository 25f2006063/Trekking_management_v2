<template>
  <div class="container mt-4">
    <h2 class="mb-4">📋 All Bookings</h2>

    <!-- Summary Cards -->
    <div class="row mb-4">
      <div class="col-md-4">
        <div class="card text-center p-3 shadow-sm">
          <h5>Total Bookings</h5>
          <h3>{{ bookings.length }}</h3>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card text-center p-3 shadow-sm">
          <h5>Confirmed</h5>
          <h3 class="text-success">{{ confirmedCount }}</h3>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card text-center p-3 shadow-sm">
          <h5>Cancelled</h5>
          <h3 class="text-danger">{{ cancelledCount }}</h3>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="card shadow-sm p-3">
      <table class="table table-hover align-middle">
        <thead class="table-dark">
          <tr>
            <th>#</th>
            <th>User</th>
            <th>Trek</th>
            <th>Date</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="(b, index) in bookings" :key="b.id">
            <td>{{ index + 1 }}</td>
            <td>{{ b.user_name }}</td>
            <td>{{ b.trek_title }}</td>
            <td>{{ formatDate(b.date) }}</td>

            <td>
              <span
                class="badge"
                :class="{
                  'bg-success': b.status === 'confirmed',
                  'bg-danger': b.status === 'cancelled',
                  'bg-warning': b.status === 'pending'
                }"
              >
                {{ b.status }}
              </span>
            </td>
          </tr>

          <tr v-if="bookings.length === 0">
            <td colspan="5" class="text-center text-muted">
              No bookings found
            </td>
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
      bookings: []
    };
  },

  computed: {
    confirmedCount() {
      return this.bookings.filter(b => b.status === "confirmed").length;
    },
    cancelledCount() {
      return this.bookings.filter(b => b.status === "cancelled").length;
    }
  },

  mounted() {
    this.fetchBookings();
  },

  methods: {
    async fetchBookings() {
      try {
        const res = await axios.get(
          "http://127.0.0.1:5000/api/admin/bookings",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`
            }
          }
        );

        this.bookings = res.data;
      } catch (err) {
        console.error(err);
      }
    },

    formatDate(date) {
      return new Date(date).toLocaleDateString();
    }
  }
};
</script>

<style scoped>
.card {
  border-radius: 10px;
}

.table th,
.table td {
  vertical-align: middle;
}
</style>