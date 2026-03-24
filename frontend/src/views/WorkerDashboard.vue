<template>
  <div class="max-w-5xl mx-auto my-6 px-4 flex flex-col md:flex-row gap-6">

    <!-- Sidebar: Filters (Mock) -->
    <aside class="w-full md:w-1/4">
      <div class="card sticky top-24 bg-white border-brand-lavender shadow-sm border-2">
        <h3 class="text-xl font-extrabold text-brand-mocha mb-4 flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-brand-taupe" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
          {{ $t('dashboard.filters') }}
        </h3>

        <div class="space-y-4">
          <div>
            <label class="input-label">{{ $t('dashboard.distance') }}</label>
            <input type="range" min="1" max="50" class="w-full accent-brand-charcoal" />
            <div class="flex justify-between text-xs text-brand-taupe font-bold">
              <span>1 km</span>
              <span>50 km</span>
            </div>
          </div>

          <div>
            <label class="input-label">{{ $t('dashboard.salary') }}</label>
            <div class="flex items-center gap-2">
              <input type="number" class="input-field !py-2 !px-3 text-sm" placeholder="Min" />
              <span class="text-brand-taupe font-bold">-</span>
              <input type="number" class="input-field !py-2 !px-3 text-sm" placeholder="Max" />
            </div>
          </div>

          <button class="btn btn-primary w-full text-sm py-2 mt-4">{{ $t('dashboard.apply') }}</button>
        </div>
      </div>
    </aside>

    <!-- Main Content: Matches -->
    <main class="w-full md:w-3/4">
      <div class="flex items-center justify-between mb-8 bg-brand-blush p-6 rounded-2xl border-2 border-brand-lavender shadow-sm">
        <div>
          <h1 class="text-3xl font-extrabold text-brand-mocha">{{ $t('dashboard.matches') }}</h1>
          <p class="text-brand-taupe font-bold mt-1">{{ $t('dashboard.matchesSubtitle') }}</p>
        </div>
        <div class="w-16 h-16 bg-white rounded-full flex items-center justify-center shadow-md border-2 border-brand-lavender rotate-12 hover:rotate-0 transition-transform">
          <span class="text-3xl">🎯</span>
        </div>
      </div>

      <div v-if="loading" class="text-center py-20">
        <div class="inline-block w-12 h-12 border-4 border-t-brand-charcoal border-brand-lavender rounded-full animate-spin"></div>
        <p class="mt-4 font-bold text-brand-taupe">{{ $t('dashboard.findingPerfect') }}</p>
      </div>

      <div v-else-if="matches.length === 0" class="text-center py-20 card border-brand-lavender bg-white">
        <span class="text-5xl mb-4 block opacity-50">😢</span>
        <h3 class="text-xl font-bold text-brand-mocha">{{ $t('dashboard.noMatches') }}</h3>
        <p class="text-brand-taupe font-medium">{{ $t('dashboard.tryAddingSkills') }}</p>
      </div>

      <div v-else class="space-y-6">
        <div class="card bg-white border-brand-lavender !p-2 mb-6 shadow-sm overflow-hidden border-2">
          <MapView :markers="matches" />
        </div>

        <div class="space-y-4">
          <MatchCard v-for="(job, index) in matches" :key="job.job_id" :data="job" :index="index" />
        </div>
      </div>
    </main>
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
    const res = await axios.get(`http://localhost:8000/jobs/match_jobs/${props.id}`)
    matches.value = res.data
  } catch (err) {
    console.error("Failed to load matches", err)
  } finally {
    loading.value = false
  }
})
</script>