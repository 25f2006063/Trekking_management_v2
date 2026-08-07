import { createRouter, createWebHistory } from "vue-router";

// Import views
import HomeView from "../views/HomeView.vue";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import Dashboard from "../views/Dashboard.vue";
import Treks from "../views/Treks.vue";
import AboutView from "../views/AboutView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,   // Landing page
  },
  {
    path: "/login",
    name: "login",
    component: Login,
  },
  {
    path: "/register",
    name: "register",
    component: Register,
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: Dashboard,
  },
  {
    path: "/treks",
    name: "treks",
    component: Treks,
  },
  {
    path: "/about",
    name: "about",
    component: AboutView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;