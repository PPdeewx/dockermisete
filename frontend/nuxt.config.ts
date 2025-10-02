import Aura from '@primeuix/themes/aura';

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
        preset: Aura,
        options: {
          darkModeSelector: false,
          cssLayer: true
        }
      }
    },
    components: {
      include: ['Card','DataTable','Column','Button','AutoComplete','Dialog','InputText','Dropdown','Toast','Toolbar','Sidebar','InputNumber','Calendar','FileUpload','Password','TabView','TabPanel','TextArea','ToggleButton','MultiSelect','RadioButton','Checkbox'],
    },
  },
  css: [
    'primeicons/primeicons.css',
  ]
})