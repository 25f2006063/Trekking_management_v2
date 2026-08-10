<template>
  <div class="container mt-5" style="max-width:400px">

    <h3 class="text-center mb-3">Register</h3>

    <input v-model="name" class="form-control mb-2" placeholder="Name" />
    <input v-model="email" class="form-control mb-2" placeholder="Email" />
    <input v-model="password" type="password" class="form-control mb-2" placeholder="Password" />
    <input v-model="phone" class="form-control mb-3" placeholder="Phone (optional)" />

    <p v-if="message" class="text-success small">{{ message }}</p>
    <p v-if="error" class="text-danger small">{{ error }}</p>

    <button @click="handleRegister" class="btn btn-success w-100">
      Register
    </button>

    <p class="text-center mt-3 small">
      Already have an account?
      <router-link to="/login">Login</router-link>
    </p>

  </div>
</template>

<script>
import { registerUser } from "../../services/auth_service";

export default {
  data() {
    return {
      name: "",
      email: "",
      password: "",
      phone: "",
      message: "",
      error: "",
    };
  },

  methods: {
    async handleRegister() {
      this.error = "";
      this.message = "";

      try {
        const res = await registerUser({
          name: this.name,
          email: this.email,
          password: this.password,
          phone: this.phone,
        });

        this.message = res.data.message;

        // redirect after register
        setTimeout(() => {
          this.$router.push("/login");
        }, 1500);

      } catch (err) {
        this.error = err.response?.data?.message || "Registration failed";
      }
    },
  },
};
</script>