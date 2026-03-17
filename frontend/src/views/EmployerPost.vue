<template>
  <div class="max-w-md mx-auto my-10 card animate-fade-in-up shadow-xl shadow-blue-100">
    <div class="text-center mb-8">
      <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-100 mb-4 animate-pulse">
        <span class="text-3xl text-blue-500">🏢</span>
      </div>
      <h2 class="text-2xl font-extrabold text-[#4b4b4b]">Post a Job</h2>
      <p class="text-gray-500 mt-1 font-medium">Find the right worker nearby!</p>
    </div>

    <form @submit.prevent="submit" class="space-y-5">
      <div>
        <label class="input-label">Employer / Business Name</label>
        <input v-model="form.employer_name" class="input-field" placeholder="E.g., RS Auto Works" required />
      </div>

      <div>
        <label class="input-label">Required Skills</label>
        <input v-model="form.skills_required" class="input-field" placeholder="E.g., bike mechanic, wiring" required />
        <p class="text-xs text-gray-400 mt-1 font-bold">Separate skills with commas</p>
      </div>

      <div>
        <label class="input-label">Salary (₹)</label>
        <input type="number" v-model.number="form.salary" class="input-field" placeholder="E.g., 15000" min="0" required />
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

      <button type="submit" class="btn btn-secondary w-full mt-6 text-lg" :disabled="loading">
        <span v-if="loading" class="animate-pulse">Loading...</span>
        <span v-else>Post Job ✨</span>
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
  employer_name: '',
  skills_required: '',
  salary: null,
  lat: 11.0168,
  lon: 76.9558,
  urgency: 1
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
    const res = await axios.post('http://localhost:8000/jobs/post', form)
    setTimeout(() => {
      router.push(`/employer/dashboard/${res.data.job_id}`)
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