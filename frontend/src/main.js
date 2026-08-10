import axios from "axios";
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Bootstrap
import "bootstrap/dist/css/bootstrap.min.css";
import 'bootstrap/dist/js/bootstrap.bundle.min.js'; 


// 🔥 ADD THIS BLOCK HERE
axios.interceptors.response.use(
  (res) => res,
  (err) => {

    if (err.response?.status === 403) {
      alert(err.response.data.message || "Access denied");

      //  logout user
      localStorage.removeItem("token");

      
      window.location.href = "/login";
    }

    return Promise.reject(err);
  }
);


createApp(App).use(router).mount('#app')