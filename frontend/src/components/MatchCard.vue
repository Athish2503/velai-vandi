<template>
  <div
    class="card relative overflow-hidden flex flex-col md:flex-row gap-6 items-start md:items-center border-brand-lavender hover:border-brand-taupe transition-all duration-300 group shadow-sm hover:shadow-md"
    :style="`animation-delay: ${index * 150}ms;`"
    v-bind:class="{ 'animate-slide-in-right': true }"
  >
    <div class="absolute -right-10 -top-10 w-32 h-32 bg-brand-blush rounded-full opacity-50 group-hover:scale-150 transition-transform duration-700"></div>

    <div class="flex-1 z-10 w-full">
      <div class="flex justify-between items-start w-full">
        <div>
          <h3 class="text-2xl font-extrabold text-brand-mocha">
            {{ data.employer_name || data.name }}
          </h3>
          <p class="text-brand-taupe font-bold text-sm mt-1 uppercase tracking-wide">
            {{ data.employer_name ? 'Hiring for: ' : 'Skills: ' }}
            <span class="text-brand-charcoal underline decoration-brand-lavender underline-offset-2">{{ data.skills_required || data.skills }}</span>
          </p>
        </div>

        <div class="flex flex-col items-end">
          <div class="bg-brand-blush text-brand-mocha px-3 py-1 rounded-xl font-extrabold text-sm border-2 border-brand-lavender shadow-sm flex items-center gap-1">
            <span class="text-lg">🎯</span> {{ Math.round(data.score * 100) }}% Match
          </div>
        </div>
      </div>

      <div class="mt-4 flex flex-wrap gap-4 text-sm font-bold text-brand-taupe bg-brand-blush/50 p-4 rounded-xl border border-brand-lavender">
        <div v-if="data.salary" class="flex items-center gap-2">
          <span class="text-xl grayscale opacity-80">💰</span> ₹{{ data.salary }}
        </div>
        <div v-if="data.experience !== undefined" class="flex items-center gap-2">
          <span class="text-xl grayscale opacity-80">🛠️</span> {{ data.experience }} yrs exp
        </div>
        <div class="flex items-center gap-2">
          <span class="text-xl grayscale opacity-80">📍</span> <span class="text-brand-charcoal underline decoration-dotted underline-offset-4 cursor-help" title="Location coords">{{ data.lat.toFixed(2) }}, {{ data.lon.toFixed(2) }}</span>
        </div>
      </div>
    </div>

    <div class="w-full md:w-auto mt-4 md:mt-0 z-10 flex justify-end">
       <button class="btn btn-primary text-sm px-8 py-4 w-full md:w-auto shadow-sm">
         Connect
       </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  data: Object,
  index: {
    type: Number,
    default: 0
  }
})
</script>

<style scoped>
.animate-slide-in-right {
  animation: slideInRight 0.5s ease-out both;
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>