<template>
  <div class="d-flex">

    <!-- Sidebar -->
    <div class="bg-dark text-white p-3" style="width:250px; min-height:100vh;">
      <h4 class="mb-4">Trekker</h4>

      <ul class="nav flex-column">
        <li><router-link to="/admin/dashboard" class="nav-link text-white">Dashboard</router-link></li>
        <li><router-link to="/admin/treks" class="nav-link text-white">Treks</router-link></li>
        <li><router-link to="/admin/staff" class="nav-link text-white">Staff</router-link></li>
        <li><router-link to="/admin/users" class="nav-link text-white">Users</router-link></li>
        <li><router-link to="/admin/bookings" class="nav-link text-white">Bookings</router-link></li>
      </ul>
    </div>

    <!-- Page Content -->
    <div class="flex-grow-1 p-4">
      <router-view />
    </div>

  </div>
</template>