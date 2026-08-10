<template>
  <div class="container mt-4">

    <h3 class="mb-4">My Dashboard</h3>

    <!-- 🔥 STATS CARDS -->
    <div class="row mb-4">

      <div class="col-md-4">
        <div class="card p-3 shadow-sm text-center">
          <h6>Assigned Treks</h6>
          <h3>{{ stats.assigned_treks }}</h3>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card p-3 shadow-sm text-center">
          <h6>Total Participants</h6>
          <h3>{{ stats.total_participants }}</h3>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card p-3 shadow-sm text-center">
          <h6>Ongoing Treks</h6>
          <h3>{{ stats.ongoing_treks }}</h3>
        </div>
      </div>

    </div>

    <!-- 🔥 ASSIGNED TREKS TABLE -->
    <div class="card p-3 shadow-sm">

      <h5 class="mb-3">My Assigned Treks</h5>

      <table class="table table-bordered">
        <thead>
          <tr>
            <th>Name</th>
            <th>Dates</th>
            <th>Participants</th>
            <th>Slots</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="t in treks" :key="t.id">
            <td>{{ t.name }}</td>

            <td>
              {{ formatDate(t.start_date) }} -
              {{ formatDate(t.end_date) }}
            </td>

            <td>{{ t.participants }}</td>
            <td>{{ t.slots }}</td>

            <td>
              <span
                :class="getStatusClass(t.status)"
              >
                {{ t.status }}
              </span>
            </td>

            <td>
              <button
                class="btn btn-sm btn-primary"
                @click="viewBookings(t.id)"
              >
                Manage
              </button>
            </td>
          </tr>

          <tr v-if="treks.length === 0">
            <td colspan="6" class="text-center">
              No treks assigned
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
      stats: {
        assigned_treks: 0,
        total_participants: 0,
        ongoing_treks: 0
      },
      treks: []
    };
  },

  methods: {
    async fetchDashboard() {
      const token = localStorage.getItem("token");

      const res = await axios.get(
        "http://127.0.0.1:5000/api/staff/dashboard",
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      this.stats = res.data;
    },

    async fetchTreks() {
      const token = localStorage.getItem("token");

      const res = await axios.get(
        "http://127.0.0.1:5000/api/staff/treks",
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      this.treks = res.data;
    },

    formatDate(date) {
      return new Date(date).toLocaleDateString();
    },

    getStatusClass(status) {
      if (status === "ongoing") return "badge bg-success";
      if (status === "completed") return "badge bg-secondary";
      return "badge bg-warning";
    },

    viewBookings(trekId) {
      this.$router.push(`/staff/treks/${trekId}`);
    }
  },

  mounted() {
    this.fetchDashboard();
    this.fetchTreks();
  }
};
</script>