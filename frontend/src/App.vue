<script setup>
import { RouterView, RouterLink } from 'vue-router'
</script>

<template>
  <div class="min-h-screen bg-[#ffffff] text-[#4b4b4b] font-sans selection:bg-green-200">
    <header class="border-b-2 border-[#e5e5e5] bg-white sticky top-0 z-50">
      <div class="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-green-500 rounded-xl flex items-center justify-center shadow-sm rotate-3 hover:rotate-6 transition-transform cursor-pointer">
            <span class="text-white font-black text-xl">V</span>
          </div>
          <h1 class="text-2xl font-extrabold tracking-tight text-[#4b4b4b]">
            Velai<span class="text-green-500">Vandi</span>
          </h1>
        </div>

        <nav class="flex gap-4">
          <RouterLink to="/worker/register" class="font-bold text-gray-500 hover:text-green-500 transition-colors py-2 px-3 rounded-xl hover:bg-green-50" active-class="!text-green-500 bg-green-50 shadow-inner">Worker</RouterLink>
          <RouterLink to="/employer/post" class="font-bold text-gray-500 hover:text-blue-500 transition-colors py-2 px-3 rounded-xl hover:bg-blue-50" active-class="!text-blue-500 bg-blue-50 shadow-inner">Employer</RouterLink>
        </nav>
      </div>
    </header>

    <main class="max-w-4xl mx-auto p-4 md:p-8">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(10px) scale(0.98);
}
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.98);
}
</style>