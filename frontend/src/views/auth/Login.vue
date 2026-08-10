<template>
  <div class="container mt-5" style="max-width:400px">

    <h3 class="text-center mb-3">Login</h3>

    <input v-model="email" type="email" class="form-control mb-2" placeholder="Email" />
    <input v-model="password" type="password" class="form-control mb-3" placeholder="Password" />

    <p v-if="error" class="text-danger small">{{ error }}</p>

    <button @click="handleLogin" class="btn btn-primary w-100">
      Login
    </button>

    <p class="text-center mt-3 small">
      Don't have an account?
      <router-link to="/register">Register</router-link>
    </p>

  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      email: "",
      password: "",
      error: "",
    };
  },

  methods: {
    async handleLogin() {
      try {
        this.error = "";

        const res = await axios.post(
          "http://127.0.0.1:5000/api/auth/login",
          {
            email: this.email,
            password: this.password
          }
        );

        // ✅ save token
        localStorage.setItem("token", res.data.access_token);

        // 🔥 update navbar instantly
        window.dispatchEvent(new Event("storage"));

        // 🔥 REDIRECT BASED ON ROLE
        const role = res.data.user.role;

        if (role === "admin") {
          this.$router.push("/admin/dashboard");
        } else if (role === "staff") {
          this.$router.push("/staff/dashboard");
        } else {
          this.$router.push("/user/dashboard"); // normal user
        }

      } catch (err) {
        alert(err.response?.data?.message || "Login failed");
      }
    },
  },
};
</script>