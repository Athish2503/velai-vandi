<script setup>
import { RouterView, RouterLink } from 'vue-router'
</script>

<template>
  <div class="min-h-screen bg-brand-blush text-brand-mocha font-sans selection:bg-brand-lavender selection:text-brand-charcoal">
    <header class="border-b-2 border-brand-lavender bg-white sticky top-0 z-50">
      <div class="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-brand-charcoal rounded-xl flex items-center justify-center shadow-sm rotate-3 hover:rotate-6 transition-transform cursor-pointer">
            <span class="text-white font-black text-xl">V</span>
          </div>
          <h1 class="text-2xl font-extrabold tracking-tight text-brand-mocha">
            Velai<span class="text-brand-taupe">Vandi</span>
          </h1>
        </div>

        <div class="flex items-center gap-4">
          <nav class="flex gap-2">
            <RouterLink to="/worker/register" class="font-bold text-brand-taupe hover:text-brand-charcoal transition-colors py-2 px-3 rounded-xl hover:bg-brand-blush" active-class="!text-brand-charcoal bg-brand-blush shadow-inner">{{ $t('app.worker') }}</RouterLink>
            <RouterLink to="/employer/post" class="font-bold text-brand-taupe hover:text-brand-charcoal transition-colors py-2 px-3 rounded-xl hover:bg-brand-blush" active-class="!text-brand-charcoal bg-brand-blush shadow-inner">{{ $t('app.employer') }}</RouterLink>
          </nav>
          <div class="flex items-center gap-2 border-l-2 border-brand-lavender pl-4 ml-2">
            <select v-model="$i18n.locale" class="bg-brand-blush border-2 border-brand-lavender text-brand-mocha text-sm rounded-lg focus:ring-brand-charcoal focus:border-brand-charcoal block p-2.5 font-bold cursor-pointer outline-none">
              <option value="en">English</option>
              <option value="ta">தமிழ்</option>
              <option value="hi">हिंदी</option>
            </select>
          </div>
        </div>
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