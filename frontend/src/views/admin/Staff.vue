<template>
  <div>
    <h3 class="mb-4">Trekking Staff Management</h3>

    <div class="row">

      <!-- CREATE STAFF -->
      <div class="col-md-5">
        <div class="card p-3 shadow-sm">

          <h5>Create New Staff</h5>

          <input v-model="form.name" class="form-control mb-2" placeholder="Full Name" />
          <input v-model="form.email" class="form-control mb-2" placeholder="Email" />
          <input v-model="form.phone" class="form-control mb-2" placeholder="Contact Number" />

          <input v-model="form.password" type="password" class="form-control mb-2" placeholder="Password" />
          <input v-model="form.confirm" type="password" class="form-control mb-2" placeholder="Confirm Password" />

          <input v-model="form.experience" class="form-control mb-2" placeholder="Experience" />
          <input v-model="form.specialization" class="form-control mb-2" placeholder="Specialization" />

          <select v-model="form.status" class="form-control mb-3">
            <option value="active">Active</option>
            <option value="blacklisted">Blacklisted</option>
          </select>

          <div class="d-flex justify-content-between">
            <button @click="resetForm" class="btn btn-secondary">Cancel</button>
            <button @click="createStaff" class="btn btn-primary">Create Staff</button>
          </div>

        </div>
      </div>

      <!-- STAFF LIST -->
      <div v-if="errorMessage" class="alert alert-danger">
        {{ errorMessage }}
      </div>
      <div class="col-md-7">
        <div class="card p-3 shadow-sm">

          <h5>Staff List</h5>

          <input v-model="search" class="form-control mb-3" placeholder="Search..." />

          <table class="table table-bordered">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Status</th>
                <th>Action</th> <!-- 🔥 ADD -->
              </tr>
            </thead>

            <tbody>
              <tr v-for="s in filteredStaff" :key="s.id">
                <td>{{ s.id }}</td>
                <td>{{ s.name }}</td>
                <td>{{ s.email }}</td>
                <td>{{ s.phone }}</td>

                <!-- STATUS BADGE -->
                <td>
                  <span
                    :class="s.is_blocked ? 'badge bg-danger' : 'badge bg-success'"
                  >
                    {{ s.is_blocked ? 'blacklisted' : 'active' }}
                  </span>
                </td>
                <!-- 🔥 ACTION BUTTON -->
                <td>
                  <button
                    v-if="!s.is_blocked"
                    @click="toggleStatus(s.id)"
                    class="btn btn-sm btn-danger"
                  >
                    Blacklist
                  </button>

                  <button
                    v-else
                    @click="toggleStatus(s.id)"
                    class="btn btn-sm btn-success"
                  >
                    Whitelist
                  </button>
                </td>
              </tr>

              <tr v-if="staff.length === 0">
                <td colspan="6" class="text-center">No staff found</td>
              </tr>
            </tbody>
          </table>

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
      staff: [],
      search: "",
      errorMessage: "", 
      form: {
        name: "",
        email: "",
        phone: "",
        password: "",
        confirm: "",
        status: "active"
      }
    };
  },

  computed: {
    filteredStaff() {
      return this.staff.filter(s =>
        s.name.toLowerCase().includes(this.search.toLowerCase())
      );
    }
  },

  methods: {

    async getStaff() {
      try {
        const token = localStorage.getItem("token");

        const res = await axios.get(
          "http://127.0.0.1:5000/api/admin/staff",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        console.log("STAFF DATA:", res.data); // 🔥 DEBUG

        this.staff = res.data;

      } catch (err) {
        console.error("GET ERROR:", err);
      }
    },

    async createStaff() {
      try {
        const token = localStorage.getItem("token");

        await axios.post(
          "http://127.0.0.1:5000/api/admin/staff",
          this.form,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        alert("Staff Created");

        this.getStaff();   // 🔥 refresh
      } catch (err) {
        alert(err.response?.data?.message);
      }
    },

    async toggleStatus(id) {
      try {
        const token = localStorage.getItem("token");

        const res = await axios.put(
          `http://127.0.0.1:5000/api/admin/staff/${id}/status`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        alert(res.data.message);   

        await this.getStaff();

      } catch (err) {
        console.error(err);
        alert(err.response?.data?.message || "Error updating");
      }
}
  },

  mounted() {
    this.getStaff(); // 🔥 VERY IMPORTANT
  }
};
</script>