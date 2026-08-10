<template>
  <div class="container mt-4">
    <h2>Browse Treks</h2>

    <div class="row">
      <div
        class="col-md-4 mb-3"
        v-for="trek in treks"
        :key="trek.id"
      >
        <TrekCard
          :trek="trek"
          :isBooked="isBooked(trek.id)"
          @book="bookTrek"
          @cancel="cancelBooking"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import TrekCard from "../../components/TrekCard.vue";

export default {
  components: { TrekCard },

  data() {
    return {
      treks: [],
      myBookings: []
    };
  },

  methods: {
    isBooked(trekId) {
      return this.myBookings.some(b => b.trek_id === trekId);
    },

    async fetchData() {
      const token = localStorage.getItem("token");

      const treksRes = await axios.get(
        "http://127.0.0.1:5000/api/user/treks",
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      const bookingsRes = await axios.get(
        "http://127.0.0.1:5000/api/user/bookings",
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      this.treks = treksRes.data;
      this.myBookings = bookingsRes.data;
    },

    async bookTrek(trekId) {
      try {
        const token = localStorage.getItem("token");

        await axios.post(
          "http://127.0.0.1:5000/api/user/bookings",
          { trek_id: trekId },
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        );

        alert("Booked!");
        this.fetchData();

      } catch (err) {
        alert(err.response?.data?.message || "Booking failed");
      }
    },

    async cancelBooking(trekId) {
      try {
        const token = localStorage.getItem("token");

        await axios.delete(
          `http://127.0.0.1:5000/api/user/bookings/${trekId}`,
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        );

        alert("Cancelled!");
        this.fetchData();

      } catch (err) {
        console.error(err);
      }
    }
  },

  mounted() {
    this.fetchData();
  }
};
</script>