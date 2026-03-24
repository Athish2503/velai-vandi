import { defineStore } from 'pinia'

export const useOnboardingStore = defineStore('onboarding', {
  state: () => ({
    step: 1,
    formData: {
      name: '',
      phone: '',
      bio: '',
      skills: '',
      experience: null,
      lat: 11.0168,
      lon: 76.9558
    }
  }),
  actions: {
    setStep(newStep) {
      if (newStep >= 1 && newStep <= 4) {
        this.step = newStep
      }
    },
    nextStep() {
      if (this.step < 4) this.step++
    },
    prevStep() {
      if (this.step > 1) this.step--
    },
    updateData(payload) {
      this.formData = { ...this.formData, ...payload }
    },
    reset() {
      this.step = 1
      this.formData = {
        name: '',
        phone: '',
        bio: '',
        skills: '',
        experience: null,
        lat: 11.0168,
        lon: 76.9558
      }
    }
  }
})
