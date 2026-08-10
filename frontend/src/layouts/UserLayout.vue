<template>
  <div class="d-flex">

    <!-- SIDEBAR -->
    <div class="bg-dark text-white p-3" style="width: 220px; min-height: 100vh;">
      <h4 class="text-success">Trekker</h4>
      <hr />

      <ul class="nav flex-column">

        <li class="nav-item mb-2">
          <router-link to="/user/dashboard" class="nav-link text-white">
            Dashboard
          </router-link>
        </li>

        <li class="nav-item mb-2">
          <router-link to="/user/treks" class="nav-link text-white">
            Browse Treks
          </router-link>
        </li>

        <li class="nav-item mb-2">
          <router-link to="/user/bookings" class="nav-link text-white">
            My Bookings
          </router-link>
        </li>

        <li class="nav-item mt-4">
          <button @click="logout" class="btn btn-danger w-100">
            Logout
          </button>
        </li>

      </ul>
    </div>

    <!-- CONTENT -->
    <div class="flex-grow-1 p-4">
      <router-view />
    </div>

  </div>
</template>

<script>
export default {
  methods: {
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/");
    }
  }
};
</script>