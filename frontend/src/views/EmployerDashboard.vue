<template>
  <div class="max-w-3xl mx-auto my-10 p-4">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-3xl font-extrabold text-[#4b4b4b]">Top Candidate Matches</h1>
        <p class="text-gray-500 font-bold mt-1">Here are the best workers for your job.</p>
      </div>
      <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center shadow-inner">
        <span class="text-3xl">👥</span>
      </div>
    </div>

    <div v-if="loading" class="text-center py-20">
      <div class="inline-block w-12 h-12 border-4 border-t-[#1cb0f6] border-[#e5e5e5] rounded-full animate-spin"></div>
      <p class="mt-4 font-bold text-gray-400">Searching nearby workers...</p>
    </div>

    <div v-else-if="matches.length === 0" class="text-center py-20 card">
      <span class="text-5xl mb-4 block opacity-50">🤷‍♂️</span>
      <h3 class="text-xl font-bold text-gray-600">No candidates found yet</h3>
      <p class="text-gray-400 font-medium">Try broadening your required skills.</p>
    </div>

    <div v-else class="space-y-6">
      <div class="card bg-gray-50 border-gray-200 !p-2 mb-6 shadow-none">
        <MapView :markers="matches" />
      </div>

      <div class="space-y-4">
        <MatchCard v-for="(worker, index) in matches" :key="worker.worker_id" :data="worker" :index="index" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import MatchCard from '../components/MatchCard.vue'
import MapView from '../components/MapView.vue'

const props = defineProps(['id'])
const matches = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await axios.get(`http://localhost:8000/jobs/match_workers/${props.id}`)
    matches.value = res.data
  } catch (err) {
    console.error("Failed to load matches", err)
  } finally {
    loading.value = false
  }
})
</script>