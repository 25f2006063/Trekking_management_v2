import { createRouter, createWebHistory } from "vue-router";

import Login from "../views/auth/Login.vue";
import Register from "../views/auth/Register.vue";

import AdminDashboard from "../views/admin/Dashboard.vue";
import Treks from "../views/admin/Treks.vue";

import UserDashboard from "../views/user/Dashboard.vue";
import BrowseTreks from "../views/user/BrowseTreks.vue";

import StaffDashboard from "../views/staff/Dashboard.vue";
import AssignedTreks from "../views/staff/AssignedTreks.vue";

import Home from "../views/Home.vue";

import AdminLayout from "../layouts/AdminLayout.vue"; 
import StaffLayout from "../layouts/StaffLayout.vue";
import UserLayout from "../layouts/UserLayout.vue"; 

import MyBookings from "../views/user/MyBookings.vue";



const routes = [
  { path: "/", component: Home },

  { path: "/login", component: Login },
  { path: "/register", component: Register },

  // ADMIN NESTED ROUTES
  {
    path: "/admin",
    component: AdminLayout,
    children: [
      { path: "dashboard", component: AdminDashboard },
      { path: "treks", component: Treks },
      { path: "staff", component: () => import("../views/admin/Staff.vue") },
      { path: "users", component: () => import("../views/admin/Users.vue") },
      { path: "bookings", component: () => import("../views/admin/Bookings.vue") },
    ],
  },

  // USER (WITH LAYOUT)
  {
  path: "/user",
  component: UserLayout,
  children: [
    { path: "dashboard", component: UserDashboard },
    { path: "treks", component: BrowseTreks },
    { path: "bookings", component: MyBookings }, // ✅ FIXED
  ]
},

  // STAFF (WITH LAYOUT)
  // STAFF (FIXED)
  {
    path: "/staff",
    component: StaffLayout,
    children: [
      { path: "dashboard", component: StaffDashboard },
      { path: "treks", component: AssignedTreks },      // list page
      { path: "treks/:id", component: () => import("../views/staff/TrekDetails.vue") } // details page
    ]
  }
];

export default createRouter({
  history: createWebHistory(),
  routes,
});