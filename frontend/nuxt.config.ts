// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ['@primevue/nuxt-module'],
  primevue: {
    ripple: true,
    components: ['Card','DataTable','Column','Button'],
  },
  css: [
    'primeicons/primeicons.css',
  ]
})