<template>
  <div class="container mt-4">

    
    <button
      class="btn btn-secondary mb-3"
      @click="$router.push('/staff/treks')"
    >
      ← Back
    </button>

    <h4>Participants</h4>

    <table class="table table-bordered mt-3">
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="b in bookings" :key="b.id">
          <td>{{ b.name }}</td>
          <td>{{ b.email }}</td>
        </tr>

        <tr v-if="bookings.length === 0">
          <td colspan="2" class="text-center">
            No participants
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 🔥 STATUS UPDATE -->
    <div class="mt-3">
      <select v-model="status" class="form-control w-25 d-inline">
        <option value="pending">Pending</option>
        <option value="ongoing">Ongoing</option>
        <option value="completed">Completed</option>
      </select>

      <button
        class="btn btn-success ms-2"
        @click="updateStatus"
      >
        Update
      </button>
    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      bookings: [],
      status: "pending"
    };
  },

  methods: {
    async fetchBookings() {
      try {
        const token = localStorage.getItem("token");
        const id = this.$route.params.id;

        const res = await axios.get(
          `http://127.0.0.1:5000/api/staff/treks/${id}/bookings`,
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        );

        // ✅ FIX HERE
        this.bookings = res.data.bookings || res.data;

        // ✅ ALSO SET STATUS FROM BACKEND
        if (res.data.status) {
          this.status = res.data.status;
        }

      } catch (err) {
        console.error(err);
      }
    },

    async updateStatus() {
      try {
        const token = localStorage.getItem("token");
        const id = this.$route.params.id;

        await axios.put(
          `http://127.0.0.1:5000/api/staff/treks/${id}/status`,
          { status: this.status },
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        );

        alert("Status updated");
        this.fetchBookings();

      } catch (err) {
        console.error(err);
      }
    }
  },

  mounted() {
    this.fetchBookings();
  }
};
</script>