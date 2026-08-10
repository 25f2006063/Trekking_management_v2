<template>
  <div class="container mt-4">
    <h3>My Treks</h3>

    <table class="table table-bordered mt-3">
      <thead>
        <tr>
          <th>Title</th>
          <th>Location</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="t in treks" :key="t.id">
          <td>{{ t.title }}</td>
          <td>{{ t.location }}</td>
          <td>
            <span class="badge bg-info text-dark">
              {{ t.status }}
            </span>
          </td>

          <td>
            <!-- ✅ MANAGE BUTTON -->
            <router-link
              :to="`/staff/treks/${t.id}`"
              class="btn btn-primary btn-sm"
            >
              Manage
            </router-link>
          </td>
        </tr>

        <tr v-if="treks.length === 0">
          <td colspan="4" class="text-center">No treks assigned</td>
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
      treks: []
    };
  },

  async mounted() {
    try {
      const token = localStorage.getItem("token");

      const res = await axios.get(
        "http://127.0.0.1:5000/api/staff/treks",
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      this.treks = res.data.treks || res.data;

    } catch (err) {
      console.error(err);
    }
  }
};
</script>