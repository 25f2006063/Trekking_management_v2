<template>
<div class="container mt-4">
  <div class="row">

    <!-- CREATE TREK -->
    <div class="col-md-4">
      <h5>Create New Trek</h5>

      <input v-model="form.title" class="form-control mb-2" placeholder="Trek Name" />
      <input v-model="form.location" class="form-control mb-2" placeholder="Location" />
      <input v-model="form.description" class="form-control mb-2" placeholder="Description" />

      <select v-model="form.difficulty" class="form-control mb-2">
        <option value="">Select Difficulty</option>
        <option value="Easy">Easy</option>
        <option value="Moderate">Moderate</option>
        <option value="Hard">Hard</option>
      </select>

      <input v-model="form.price" type="number" class="form-control mb-2" placeholder="Price" />
      <input v-model="form.duration" type="number" class="form-control mb-2" placeholder="Duration" />
      <input v-model="form.total_slots" type="number" class="form-control mb-2" placeholder="Slots" />

      <input v-model="form.start_date" type="date" class="form-control mb-2" />
      <input v-model="form.end_date" type="date" class="form-control mb-3" />

      <div class="d-flex justify-content-between">
        <button @click="resetForm" class="btn btn-secondary">Cancel</button>
        <button @click="createTrek" class="btn btn-primary">Create Trek</button>
      </div>
    </div>

    <!-- TREK LIST -->
    <div class="col-md-8">
      <h5>Trek List</h5>

      <input v-model="search" class="form-control mb-3" placeholder="Search..." />

      <table class="table table-bordered">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Location</th>
            <th>Difficulty</th>
            <th>Slots</th>
            <th>Status</th>
            <th>Assign Staff</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="t in filteredTreks" :key="t.id">
            <td>{{ t.id }}</td>
            <td>{{ t.title }}</td>
            <td>{{ t.location }}</td>
            <td>{{ t.difficulty }}</td>
            <td>{{ t.available_slots }}/{{ t.total_slots }}</td>

            <!-- STATUS -->
            <td>
              <span
                :class="t.assigned_staff_id ? 'badge bg-success' : 'badge bg-secondary'"
              >
                {{ t.assigned_staff_id ? 'Open' : 'Pending' }}
              </span>
            </td>

            <!-- ASSIGN STAFF -->
            <td>
              <select v-model="t.selected_staff" class="form-select form-select-sm mb-1">
                <option disabled value="">Select Staff</option>
                <option v-for="s in staffList" :key="s.id" :value="s.id">
                  {{ s.name }}
                </option>
              </select>

              <button
                class="btn btn-sm btn-primary"
                @click="assignStaff(t.id, t.selected_staff)"
              >
                Assign
              </button>
            </td>

            <!-- DELETE -->
            <td>
              <button class="btn btn-sm btn-danger" @click="deleteTrek(t.id)">
                Delete
              </button>
            </td>
          </tr>

          <tr v-if="treks.length === 0">
            <td colspan="8" class="text-center">No treks found</td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      treks: [],
      staffList: [],
      search: "",
      errorMessage: "",

      form: {
        title: "",
        location: "",
        description: "",
        difficulty: "",
        price: "",
        duration: "",
        total_slots: "",
        start_date: "",
        end_date: ""
      }
    };
  },

  computed: {
    filteredTreks() {
      return this.treks.filter(t =>
        t.title.toLowerCase().includes(this.search.toLowerCase())
      );
    }
  },

  methods: {
    async getTreks() {
      const res = await axios.get("http://127.0.0.1:5000/api/admin/treks", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`
        }
      });

      this.treks = res.data;
    },

    async getStaff() {
      const res = await axios.get("http://127.0.0.1:5000/api/admin/staff", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`
        }
      });

      this.staffList = res.data;
    },

    async createTrek() {
      await axios.post(
        "http://127.0.0.1:5000/api/admin/treks",
        this.form,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`
          }
        }
      );

      this.resetForm();
      this.getTreks();
    },

    async deleteTrek(id) {
      await axios.delete(
        `http://127.0.0.1:5000/api/admin/treks/${id}`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`
          }
        }
      );

      this.getTreks();
    },

    async assignStaff(trekId, staffId) {
      try {
        this.errorMessage = "";

        if (!staffId) {
          this.errorMessage = "Please select staff";
          return;
        }

        const token = localStorage.getItem("token");

        const res = await axios.put(
          `http://127.0.0.1:5000/api/admin/assign-staff/${trekId}`,
          { staff_id: staffId },
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        alert(res.data.message);
        this.getTreks();

      } catch (err) {
        console.error(err);

        // 🔥 THIS SHOWS YOUR CONFLICT MESSAGE
        this.errorMessage =
          err.response?.data?.message || "Assignment failed"; 
        alert(err.response?.data?.message || "Assignment failed");
      }
    },

    resetForm() {
      this.form = {
        title: "",
        location: "",
        description: "",
        difficulty: "",
        price: "",
        duration: "",
        total_slots: "",
        start_date: "",
        end_date: ""
      };
    }
  },

  mounted() {
    this.getTreks();
    this.getStaff();
  }
};
</script>