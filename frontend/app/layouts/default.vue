<template>
  <div>
    <div class="full-page-container">
    <Sidebar />
    <div class="main-content">
      

      <slot /> 
    
    </div>
  </div>
  </div>
</template>

<script setup lang="ts">
import Sidebar from '~/components/Sidebar.vue'
</script>

<style scoped>
.full-page-container {
  display: flex;
  height: 100vh;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  padding: 1rem;
}

.dashboard-container {
  padding: 1rem 0;
}

.mb-3 {
  margin-bottom: 1rem;
}
</style>
