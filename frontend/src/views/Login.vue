<template>
  <div class="login-container">
    <div class="card">
      <h2>Login</h2>

      <input v-model="email" placeholder="Email" />
      <input v-model="password" type="password" placeholder="Password" />

      <button @click="login">Login</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import API from "../api";
import { useRouter } from "vue-router";

const email = ref("");
const password = ref("");
const router = useRouter();

const login = async () => {
  try {
    await API.post("/login", {
      email: email.value,
      password: password.value,
    });
    router.push("/dashboard");
  } catch {
    alert("Login failed");
  }
};
</script>

<style>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.card {
  background: white;
  padding: 30px;
  width: 300px;
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
  background: #2e7d32;
  color: white;
  border: none;
  cursor: pointer;
}
</style>