<template>
  <div class="max-w-md mx-auto my-10 card animate-fade-in-up shadow-xl shadow-green-100">
    <div class="text-center mb-8">
      <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-green-100 mb-4 animate-bounce">
        <span class="text-3xl text-green-500">👷</span>
      </div>
      <h2 class="text-2xl font-extrabold text-[#4b4b4b]">Join Velai Vandi</h2>
      <p class="text-gray-500 mt-1 font-medium">Find local jobs that match your skills!</p>
    </div>

    <form @submit.prevent="submit" class="space-y-5">
      <div>
        <label class="input-label">Full Name</label>
        <input v-model="form.name" class="input-field" placeholder="E.g., Ramesh K" required />
      </div>

      <div>
        <label class="input-label">Your Skills</label>
        <input v-model="form.skills" class="input-field" placeholder="E.g., mechanic, electrician, plumber" required />
        <p class="text-xs text-gray-400 mt-1 font-bold">Separate skills with commas</p>
      </div>

      <div>
        <label class="input-label">Years of Experience</label>
        <input type="number" v-model.number="form.experience" class="input-field" placeholder="E.g., 5" min="0" required />
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="input-label">Latitude</label>
          <input type="number" step="0.000001" v-model.number="form.lat" class="input-field" placeholder="11.0168" required />
        </div>
        <div>
          <label class="input-label">Longitude</label>
          <input type="number" step="0.000001" v-model.number="form.lon" class="input-field" placeholder="76.9558" required />
        </div>
      </div>
      <div class="text-right">
        <button type="button" @click="getLocation" class="text-sm font-bold text-blue-500 hover:text-blue-600 transition-colors">
          📍 Use My Location
        </button>
      </div>

      <button type="submit" class="btn btn-primary w-full mt-6 text-lg" :disabled="loading">
        <span v-if="loading" class="animate-pulse">Loading...</span>
        <span v-else>Start Matching 🚀</span>
      </button>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(false)

const form = reactive({
  name: '',
  skills: '',
  experience: null,
  lat: 11.0168,
  lon: 76.9558
})

const getLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        form.lat = position.coords.latitude;
        form.lon = position.coords.longitude;
      },
      (error) => {
        alert("Couldn't get your location. Please enter manually.");
      }
    );
  } else {
    alert("Geolocation is not supported by this browser.");
  }
}

const submit = async () => {
  loading.value = true
  try {
    const res = await axios.post('http://localhost:8000/workers/register', form)
    // Add a slight delay for emotional design (gives a feeling of work being done)
    setTimeout(() => {
      router.push(`/worker/dashboard/${res.data.worker_id}`)
    }, 800)
  } catch (err) {
    alert("Oops! Something went wrong.")
    console.error(err)
    loading.value = false
  }
}
</script>

<style scoped>
.animate-fade-in-up {
  animation: fadeInUp 0.6s ease-out;
}
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>