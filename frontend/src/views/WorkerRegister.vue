<template>
  <div class="max-w-xl mx-auto my-6 card animate-fade-in-up shadow-xl shadow-brand-lavender border-brand-lavender">

    <!-- Header / Progress Bar -->
    <div class="mb-8">
      <div class="text-center mb-6">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-brand-blush mb-4 animate-bounce border-2 border-brand-lavender shadow-sm">
          <span class="text-3xl text-brand-charcoal">👷</span>
        </div>
        <h2 class="text-2xl font-extrabold text-brand-mocha">{{ $t('onboarding.welcome') }}</h2>
        <p class="text-brand-taupe mt-1 font-medium">{{ $t('onboarding.subtitle') }}</p>
      </div>

      <!-- Gamified Progress -->
      <div class="flex items-center justify-between relative px-2">
        <div class="absolute left-0 top-1/2 transform -translate-y-1/2 w-full h-2 bg-brand-blush rounded-full -z-10"></div>
        <div class="absolute left-0 top-1/2 transform -translate-y-1/2 h-2 bg-brand-charcoal rounded-full -z-10 transition-all duration-500 ease-out" :style="{ width: progressWidth }"></div>

        <div v-for="s in 4" :key="s" class="relative flex flex-col items-center">
          <div
            class="w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm border-2 transition-colors duration-300"
            :class="[
              store.step >= s ? 'bg-brand-charcoal border-brand-charcoal text-white shadow-md' : 'bg-white border-brand-lavender text-brand-taupe',
              store.step === s ? 'ring-4 ring-brand-blush scale-110' : ''
            ]"
          >
            <span v-if="store.step > s">✓</span>
            <span v-else>{{ s }}</span>
          </div>
          <span class="absolute -bottom-6 text-xs font-bold text-center w-24 -ml-8" :class="store.step >= s ? 'text-brand-charcoal' : 'text-brand-taupe'">
            {{ getStepName(s) }}
          </span>
        </div>
      </div>
    </div>

    <!-- Step 1: Basic Info -->
    <div v-show="store.step === 1" class="space-y-5 mt-10 animate-fade-in">
      <div>
        <label class="input-label">{{ $t('onboarding.fullName') }}</label>
        <input v-model="store.formData.name" class="input-field" :placeholder="$t('onboarding.fullName')" required />
      </div>
      <div>
        <label class="input-label">{{ $t('onboarding.phone') }}</label>
        <input v-model="store.formData.phone" class="input-field" placeholder="123-456-7890" />
      </div>
      <div class="pt-4 flex justify-end">
        <button @click="nextStep" class="btn btn-primary w-full text-lg" :disabled="!store.formData.name">
          {{ $t('onboarding.next') }}
        </button>
      </div>
    </div>

    <!-- Step 2: Voice Resume -->
    <div v-show="store.step === 2" class="space-y-5 mt-10 animate-fade-in">
      <div>
        <label class="input-label flex justify-between items-end">
          <span>{{ $t('onboarding.bioLabel') }}</span>
          <button @click="toggleVoice" type="button" class="flex items-center gap-1 text-sm bg-brand-blush text-brand-charcoal px-3 py-1 rounded-full hover:bg-brand-lavender transition-colors shadow-sm border border-brand-lavender">
            <span v-if="!isListening">🎤 {{ $t('onboarding.voiceStart') }}</span>
            <span v-else class="text-danger flex items-center gap-1">
              <span class="w-2 h-2 rounded-full bg-danger animate-ping"></span> {{ $t('onboarding.voiceStop') }}
            </span>
          </button>
        </label>

        <div class="relative">
          <textarea
            v-model="store.formData.bio"
            class="input-field min-h-[150px] resize-y"
            :placeholder="$t('onboarding.bioPlaceholder')"
            :class="{'border-brand-charcoal ring-2 ring-brand-blush': isListening}"
          ></textarea>
          <div v-if="isListening" class="absolute bottom-3 right-3 text-xs font-bold text-brand-charcoal animate-pulse flex items-center gap-1 bg-white px-2 py-1 rounded-md shadow-sm">
            <span>{{ $t('onboarding.voiceProcessing') }}</span>
          </div>
        </div>
        <p class="text-xs text-brand-taupe mt-2 font-medium">You can also type your experience directly.</p>
      </div>

      <div class="pt-4 flex gap-3">
        <button @click="prevStep" class="btn btn-outline w-1/3">{{ $t('onboarding.back') }}</button>
        <button @click="nextStep" class="btn btn-primary w-2/3 text-lg">{{ $t('onboarding.next') }}</button>
      </div>
    </div>

    <!-- Step 3: Skills & Experience -->
    <div v-show="store.step === 3" class="space-y-5 mt-10 animate-fade-in">
      <div>
        <label class="input-label">{{ $t('onboarding.skillsLabel') }}</label>
        <div class="flex flex-wrap gap-2 mb-3">
          <span
            v-for="(skill, index) in parsedSkills"
            :key="index"
            class="bg-brand-lavender text-brand-mocha px-3 py-1 rounded-full text-sm font-bold flex items-center gap-1 shadow-sm border border-brand-taupe/20"
          >
            {{ skill }}
            <button @click="removeSkill(index)" class="hover:text-danger rounded-full w-4 h-4 flex items-center justify-center leading-none">&times;</button>
          </span>
        </div>

        <div class="flex gap-2">
          <input
            v-model="currentSkill"
            @keydown.enter.prevent="addSkill"
            class="input-field"
            :placeholder="$t('onboarding.skillsPlaceholder')"
          />
          <button @click.prevent="addSkill" class="btn btn-secondary px-4">+</button>
        </div>
      </div>

      <div>
        <label class="input-label">{{ $t('onboarding.experienceLabel') }}</label>
        <input type="number" v-model.number="store.formData.experience" class="input-field" placeholder="E.g., 5" min="0" />
      </div>

      <div class="pt-4 flex gap-3">
        <button @click="prevStep" class="btn btn-outline w-1/3">{{ $t('onboarding.back') }}</button>
        <button @click="nextStep" class="btn btn-primary w-2/3 text-lg">{{ $t('onboarding.next') }}</button>
      </div>
    </div>

    <!-- Step 4: Location & Submit -->
    <div v-show="store.step === 4" class="space-y-5 mt-10 animate-fade-in">

      <div class="bg-brand-blush p-4 rounded-xl border-2 border-brand-lavender text-center shadow-sm">
         <div class="text-4xl mb-2">🗺️</div>
         <p class="font-bold text-brand-mocha mb-4">Where are you looking for jobs?</p>

         <button type="button" @click="getLocation" class="btn btn-secondary w-full flex items-center justify-center gap-2" :disabled="locationLoading">
           <span v-if="locationLoading" class="animate-spin inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full"></span>
           <span v-else>📍</span> {{ $t('onboarding.useLocation') }}
         </button>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="input-label">{{ $t('onboarding.lat') }}</label>
          <input type="number" step="0.000001" v-model.number="store.formData.lat" class="input-field bg-white text-brand-taupe" readonly />
        </div>
        <div>
          <label class="input-label">{{ $t('onboarding.lon') }}</label>
          <input type="number" step="0.000001" v-model.number="store.formData.lon" class="input-field bg-white text-brand-taupe" readonly />
        </div>
      </div>

      <div class="pt-4 flex gap-3">
        <button @click="prevStep" class="btn btn-outline w-1/3">{{ $t('onboarding.back') }}</button>
        <button @click="submit" class="btn btn-primary w-2/3 text-lg flex justify-center items-center gap-2" :disabled="submitting">
          <span v-if="submitting" class="animate-spin inline-block w-5 h-5 border-2 border-white border-t-transparent rounded-full"></span>
          <span v-else>{{ $t('onboarding.submit') }} 🚀</span>
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useOnboardingStore } from '../stores/onboarding'
import axios from 'axios'

const router = useRouter()
const { t } = useI18n()
const store = useOnboardingStore()

const submitting = ref(false)
const locationLoading = ref(false)
const currentSkill = ref('')
const isListening = ref(false)
let recognition = null;

const progressWidth = computed(() => {
  return `${((store.step - 1) / 3) * 100}%`
})

const getStepName = (step) => {
  return t(`onboarding.step${step}`)
}

const nextStep = () => {
  if (store.step === 1 && !store.formData.name) return;
  store.nextStep()
}

const prevStep = () => {
  store.prevStep()
}

// Skills Logic
const parsedSkills = computed(() => {
  return store.formData.skills ? store.formData.skills.split(',').map(s => s.trim()).filter(Boolean) : []
})

const addSkill = () => {
  if (currentSkill.value.trim()) {
    const current = parsedSkills.value
    if (!current.includes(currentSkill.value.trim())) {
      current.push(currentSkill.value.trim())
      store.updateData({ skills: current.join(', ') })
    }
    currentSkill.value = ''
  }
}

const removeSkill = (index) => {
  const current = [...parsedSkills.value]
  current.splice(index, 1)
  store.updateData({ skills: current.join(', ') })
}

// Location Logic
const getLocation = () => {
  locationLoading.value = true
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        store.updateData({
          lat: parseFloat(position.coords.latitude.toFixed(6)),
          lon: parseFloat(position.coords.longitude.toFixed(6))
        })
        locationLoading.value = false
      },
      (error) => {
        alert("Couldn't get your location. Please ensure location services are enabled.");
        locationLoading.value = false
      }
    );
  } else {
    alert("Geolocation is not supported by this browser.");
    locationLoading.value = false
  }
}

// Voice Recognition Logic
onMounted(() => {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    // Set language based on current i18n locale could be done here, defaulting to en-US for now but can be made dynamic
    recognition.lang = 'en-US';

    recognition.onresult = (event) => {
      let interimTranscript = '';
      let finalTranscript = '';

      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript;
        } else {
          interimTranscript += event.results[i][0].transcript;
        }
      }

      // If there's already text, append with a space
      const currentBio = store.formData.bio || '';

      if (finalTranscript) {
         store.updateData({ bio: (currentBio + ' ' + finalTranscript).trim() });
      }
    };

    recognition.onerror = (event) => {
      console.error("Speech recognition error", event.error);
      isListening.value = false;
    };

    recognition.onend = () => {
      isListening.value = false;
    };
  }
})

onUnmounted(() => {
  if (recognition && isListening.value) {
    recognition.stop();
  }
})

const toggleVoice = () => {
  if (!recognition) {
    alert("Speech recognition is not supported in your browser.");
    return;
  }

  if (isListening.value) {
    recognition.stop();
  } else {
    recognition.start();
    isListening.value = true;
  }
}


// Submit Logic
const submit = async () => {
  submitting.value = true
  try {
    // Merge bio into skills if we want to extract skills later,
    // or just send standard form to the existing backend endpoint
    const payload = {
      name: store.formData.name,
      skills: store.formData.skills || store.formData.bio, // simplistic fallback if no skills explicitly added
      experience: store.formData.experience || 0,
      lat: store.formData.lat,
      lon: store.formData.lon
    }

    // We send bio as part of skills for now if skills is empty,
    // ideally backend would have a `bio` field to process NLP over.
    if (store.formData.bio && payload.skills && !payload.skills.includes(store.formData.bio)) {
        // Just appending it to let backend NLP handle it as text
        payload.skills = payload.skills + ", " + store.formData.bio
    } else if (!payload.skills) {
        payload.skills = store.formData.bio || "general"
    }

    const res = await axios.post('http://localhost:8000/workers/register', payload)

    // Emotion design delay
    setTimeout(() => {
      store.reset()
      router.push(`/worker/dashboard/${res.data.worker_id}`)
    }, 1000)
  } catch (err) {
    alert("Oops! Something went wrong.")
    console.error(err)
    submitting.value = false
  }
}
</script>

<style scoped>
.animate-fade-in-up {
  animation: fadeInUp 0.5s ease-out;
}
.animate-fade-in {
  animation: fadeIn 0.4s ease-out;
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
