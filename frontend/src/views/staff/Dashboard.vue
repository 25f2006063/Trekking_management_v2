<template>
  <div>

    <h3 class="mb-4">My Dashboard</h3>

    <!-- 🔥 STATS -->
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

    <!-- 📋 TREK TABLE -->
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

            <td>{{ t.title }}</td>

            <td>
              {{ formatDate(t.start_date) }} -
              {{ formatDate(t.end_date) }}
            </td>

            <td>{{ getParticipants(t) }}</td>

            <td>
              {{ t.available_slots }} / {{ t.total_slots }}
            </td>

            <td>
              <span :class="getStatusClass(t.status)">
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
import axios from "axios"

export default {
  data() {
    return {
      treks: [],
      stats: {
        assigned_treks: 0,
        total_participants: 0,
        ongoing_treks: 0
      }
    }
  },

  methods: {

    async fetchDashboard() {
      try {
        const token = localStorage.getItem("token")

        const res = await axios.get(
          "http://127.0.0.1:5000/api/staff/dashboard",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        console.log("API DATA:", res.data)

        // ✅ FIX HERE
        this.treks = Array.isArray(res.data) ? res.data : res.data.treks || []

        // ✅ optional stats fallback
        if (res.data.stats) {
          this.stats = res.data.stats
        } else {
          this.stats.assigned_treks = this.treks.length
          this.stats.total_participants = this.treks.reduce(
            (sum, t) => sum + (t.total_slots - t.available_slots),
            0
          )
          this.stats.ongoing_treks = this.treks.filter(
            t => t.status === "approved"
          ).length
        }

      } catch (err) {
        console.error("Error loading dashboard", err)
      }
    },

    formatDate(date) {
      if (!date) return ""
      return new Date(date).toLocaleDateString()
    },

    getParticipants(trek) {
      // if backend sends participants count directly
      if (trek.participants !== undefined) {
        return trek.participants
      }

      // fallback calculation
      if (trek.total_slots && trek.available_slots !== undefined) {
        return trek.total_slots - trek.available_slots
      }

      return 0
    },

    getStatusClass(status) {
      if (status === "approved") return "badge bg-success"
      if (status === "pending") return "badge bg-warning text-dark"
      if (status === "rejected") return "badge bg-danger"
      return "badge bg-secondary"
    },

    viewBookings(id) {
      this.$router.push(`/staff/treks/${id}`);
    }

  },

  mounted() {
    this.fetchDashboard()
  }
}
</script>