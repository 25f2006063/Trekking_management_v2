<template>
  <nav class="navbar navbar-dark bg-dark px-3">

    <!-- LOGO -->
    <span class="navbar-brand text-success fw-bold">
      Trekker
    </span>

    <div>
      <!-- HOME -->
      <router-link to="/" class="btn btn-light btn-sm me-2">
        Home
      </router-link>

      <!-- LOGIN (ONLY IF NOT LOGGED IN) -->
      <router-link
        v-if="!isLoggedIn"
        to="/login"
        class="btn btn-light btn-sm me-2"
      >
        Login
      </router-link>

      <!-- REGISTER -->
      <router-link
        v-if="!isLoggedIn"
        to="/register"
        class="btn btn-primary btn-sm me-2"
      >
        Register
      </router-link>

      <!-- LOGOUT -->
      <button
        v-if="isLoggedIn"
        @click="logout"
        class="btn btn-danger btn-sm"
      >
        Logout
      </button>
    </div>

  </nav>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()

// ✅ reactive login state
const isLoggedIn = ref(false)

// ✅ function to update login state
const updateAuth = () => {
  isLoggedIn.value = !!localStorage.getItem("token")
}

// ✅ run when component loads
onMounted(() => {
  updateAuth()

  // 🔥 listen for login/logout changes
  window.addEventListener("storage", updateAuth)
})

// ✅ logout function
const logout = () => {
  localStorage.removeItem("token")

  isLoggedIn.value = false

  router.push("/login")
}
</script>

<style scoped>
.navbar {
  height: 60px;
}
</style>