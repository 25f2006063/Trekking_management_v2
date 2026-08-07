<template>
  <div class="register-container">
    <div class="card">
      <h2>Create Account</h2>

      <input v-model="name" placeholder="Full Name" />
      <input v-model="email" placeholder="Email" />
      <input v-model="password" type="password" placeholder="Password" />
      <input v-model="confirm" type="password" placeholder="Confirm Password" />

      <button @click="register">Register</button>

      <p>
        Already have an account?
        <router-link to="/login">Login</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import API from "../api";
import { useRouter } from "vue-router";

const name = ref("");
const email = ref("");
const password = ref("");
const confirm = ref("");

const router = useRouter();

const register = async () => {
  if (password.value !== confirm.value) {
    alert("Passwords do not match");
    return;
  }

  try {
    await API.post("/register", {
      name: name.value,
      email: email.value,
      password: password.value,
    });

    alert("Registered successfully");
    router.push("/login");
  } catch (err) {
    alert("Registration failed");
  }
};
</script>

<style>
.register-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.card {
  background: white;
  padding: 30px;
  width: 320px;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
}

button {
  width: 100%;
  padding: 10px;
  background: #1565c0;
  color: white;
  border: none;
}

p {
  margin-top: 10px;
  font-size: 14px;
}
</style>