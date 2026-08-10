<template>
  <div class="container mt-4">
    <h5>Users (Trekkers)</h5>

    <input v-model="search" class="form-control mb-3" placeholder="Search users..." />

    <table class="table table-bordered">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Email</th>
          <th>Contact</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="u in filteredUsers" :key="u.id">
          <td>{{ u.id }}</td>
          <td>{{ u.name }}</td>
          <td>{{ u.email }}</td>
          <td>{{ u.phone || 'Not provided' }}</td>

          <td>
            <span :class="u.is_blocked ? 'badge bg-danger' : 'badge bg-success'">
              {{ u.is_blocked ? "Blacklisted" : "Active" }}
            </span>
          </td>

          <td>
            <button
              v-if="!u.is_blocked"
              class="btn btn-sm btn-danger"
              @click="toggleStatus(u.id)"
            >
              Blacklist
            </button>

            <button
              v-else
              class="btn btn-sm btn-success"
              @click="toggleStatus(u.id)"
            >
              Whitelist
            </button>
          </td>
        </tr>

        <tr v-if="users.length === 0">
          <td colspan="6" class="text-center">No users found</td>
        </tr>
      </tbody>
    </table>

    <div class="alert alert-info mt-3">
      Blacklisted users cannot login or book treks.
    </div>
  </div>
</template>  

<script>
import axios from "axios";

export default {
  data() {
    return {
      users: [],
      search: ""
    };
  },

  computed: {
    filteredUsers() {
      return this.users.filter(u =>
        u.name.toLowerCase().includes(this.search.toLowerCase())
      );
    }
  },

  methods: {
    async getUsers() {
      const res = await axios.get("http://127.0.0.1:5000/api/admin/users", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`
        }
      });

      this.users = res.data;
    },

    async toggleStatus(id) {
      await axios.put(
        `http://127.0.0.1:5000/api/admin/users/${id}/status`,
        {},
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`
          }
        }
      );

      this.getUsers();
    }
  },

  mounted() {
    this.getUsers();
  }
};
</script>