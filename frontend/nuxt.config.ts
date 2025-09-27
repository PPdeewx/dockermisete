import { Lara } from '@primeuix/themes'

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ['@primevue/nuxt-module'],
  primevue: {
    usePrimeVue: true,
    autoImport: true,
    options: {
      ripple: true,
      theme: {
        preset: Lara,
        options: {
          darkModeSelector: false,
          cssLayer: true
        }
      }
    },
    components: {
      include: ['Card','DataTable','Column','Button']
    },
  },
  css: [
    'primeicons/primeicons.css',
  ]
})