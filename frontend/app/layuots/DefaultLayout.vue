<template>
  <div class="full-page-container">
    <Sidebar />
    <div class="main-content">
      <TopBar :currentUser="currentUser" @logout="logout" />
      <div class="page-content">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

import Sidebar from './Sidebar.vue'
import TopBar from './Topbar.vue'

const router = useRouter()
const currentUser = ref<any>(null)

function logout() {
  localStorage.removeItem('token')
  delete axios.defaults.headers.common['Authorization']
  router.push('/login')
}

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) return router.push('/login')

  axios.defaults.headers.common['Authorization'] = `Token ${token}`
  try {
    const me = await axios.get('http://localhost:8000/api/users/me/')
    currentUser.value = me.data
    if (currentUser.value.role !== 'admin') router.push('/login')
  } catch (err) {
    console.error(err)
    router.push('/login')
  }
})
</script>

<style scoped>
.full-page-container {
  display: flex;
  min-height: 100vh;
  background-color: #f0f2f5;
}

.main-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.page-content {
  flex-grow: 1;
}
</style>
