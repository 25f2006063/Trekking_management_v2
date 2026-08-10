<template>
  <div class="card h-100">
    <img
      :src="trek.image || 'https://via.placeholder.com/300'"
      class="card-img-top"
      height="200"
    />

    <div class="card-body">
      <h5>{{ trek.title }}</h5>
      <p>{{ trek.location }}</p>
      <p>{{ trek.difficulty }}</p>

      <!-- ✅ BOOK BUTTON -->
      <button
        v-if="!isBooked && trek.available_slots > 0"
        @click="$emit('book', trek.id)"
        class="btn btn-primary w-100"
      >
        Book Now
      </button>

      <!-- ❌ FULL -->
      <button
        v-else-if="trek.available_slots === 0"
        class="btn btn-secondary w-100"
        disabled
      >
        Full
      </button>

      <!-- 🔴 CANCEL -->
      <button
        v-else
        @click="$emit('cancel', trek.id)"
        class="btn btn-danger w-100"
      >
        Cancel Booking
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: ["trek", "isBooked"]
};
</script>