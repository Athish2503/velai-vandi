import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import './style.css'
import App from './App.vue'
import router from './router'
import messages from './locales'

const pinia = createPinia()

const i18n = createI18n({
  locale: 'en',
  fallbackLocale: 'en',
  messages,
})

const app = createApp(App)
app.use(pinia)
app.use(i18n)
app.use(router)
app.mount('#app')