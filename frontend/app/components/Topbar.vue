<template>
  <div class="top-bar">
    <div class="breadcrumbs">
      <slot name='breadcrumbs'>
        <Breadcrumb  :model="items"/>
      </slot>
    </div>
    <div class="user-profile-container">
      <div class="user-profile" @click="toggleProfileMenu">
        <i class="fas fa-bell"></i>
        <i class="fas fa-user-circle"></i>
        <span class="username">{{ currentUser?.username }} ตำแหน่ง: {{ currentUser?.role }}</span>
        <i :class="['fas', showProfileMenu ? 'fa-chevron-up' : 'fa-chevron-down']"></i>

        <div class="user-profile-menu" v-if="showProfileMenu">
          <button class="menu-item" @click.stop="goToProfile">
            <i class="fas fa-user"></i><span>ดูข้อมูลส่วนตัว</span>
          </button>
          <button class="menu-item" @click.stop="goToEditProfile">
            <i class="fas fa-edit"></i><span>แก้ไขข้อมูลส่วนตัว</span>
          </button>
          <button class="menu-item" @click.stop="goToChangePassword">
            <i class="fas fa-lock"></i><span>เปลี่ยนรหัสผ่าน</span>
          </button>
          <button class="menu-item" @click.stop="logout">
            <i class="fas fa-sign-out-alt"></i><span>ออกจากระบบ</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { PrimeIcons } from '@primevue/core/api';


import { ref, onMounted, computed, onBeforeUnmount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import Breadcrumb from 'primevue/breadcrumb';

import type { MenuItem } from 'primevue/menuitem';

const items : MenuItem[] = [
  {
    label : 'Home',url : '/admin'
  }
]
const router = useRouter()
const route = useRoute()

const currentUser = ref<{ username: string; role: string } | null>(null)
const showProfileMenu = ref(false)

const toggleProfileMenu = () => {
  showProfileMenu.value = !showProfileMenu.value
}

const goTo = (path: string) => router.push(path)
const goToProfile = () => currentUser.value?.role === 'admin' ? goTo('/admin/view-personal') : goTo('/Profile')
const goToEditProfile = () => currentUser.value?.role === 'admin' ? goTo('/admin/edit-personal') : goTo('/EditProfile')
const goToChangePassword = () => currentUser.value?.role === 'admin' ? goTo('/admin/changepass') : goTo('/ChangePassword')

function logout() {
  if (typeof window !== "undefined") localStorage.removeItem("token")
  delete axios.defaults.headers.common['Authorization']
  router.push("/login")
}

function handleBodyClick(event: MouseEvent) {
  if (showProfileMenu.value && !(event.target as HTMLElement).closest('.user-profile')) {
    showProfileMenu.value = false
  }
}

onMounted(async () => {
  document.addEventListener('click', handleBodyClick)

  if (typeof window === "undefined") return
  const token = localStorage.getItem("token")
  if (!token) {
    router.push('/login')
    return
  }

  axios.defaults.headers.common['Authorization'] = `Token ${token}`

  try {
    const response = await axios.get('http://localhost:8000/api/users/me/')
    currentUser.value = response.data
  } catch (error) {
    console.error("Failed to load current user:", error)
    router.push('/login')
  }
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleBodyClick)
})

</script>


<style scoped>

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #ffffff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  margin-bottom: 20px;
}

.breadcrumbs span {
  color: #888;
}

.user-profile-container {
  display: flex;
  align-items: center;
}

.user-profile {
  position: relative;
  display: flex;
  align-items: center;
  cursor: pointer;
}

.user-profile i {
  margin-left: 15px;
  color: #555;
  cursor: pointer;
}

.user-profile .username {
  margin-left: 15px;
  font-weight: bold;
}

.user-profile-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 220px;
  z-index: 1000;
  padding: 6px;
}

.menu-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px;
  border: 0;
  background: transparent;
  text-align: left;
  cursor: pointer;
  border-radius: 6px;
}

.menu-item:hover {
  background-color: #f0f2f5;
}

.menu-item i {
  width: 20px;
  text-align: center;
}
</style>
