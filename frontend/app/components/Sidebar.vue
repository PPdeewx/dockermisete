<template>
  <div class="sidebar">
    <div class="sidebar-header">
      <span>MIS ETE</span>
    </div>
    <ul class="nav-menu">
      <li v-for="item in menuItems" :key="item.label" class="nav-item" :class="{ 'has-submenu': item.submenu }">
        <a @click.prevent="goTo(item.path)" class="nav-link">
          <i :class="item.icon"></i> {{ item.label }}
        </a>
        <!-- ถ้ามี submenu -->
        <ul v-if="item.submenu" class="submenu">
          <li v-for="sub in item.submenu" :key="sub.label">
            <a @click.prevent="goTo(sub.path)" class="nav-link">{{ sub.label }}</a>
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const currentUser = ref<{ username: string; role: string } | null>(null)
const menuItems = ref<any[]>([])

const goTo = (path: string) => {
  router.push(path)
}

onMounted(async () => {
  const token = localStorage.getItem("token")
  if (!token) {
    router.push("/login")
    return
  }

  axios.defaults.headers.common['Authorization'] = `Token ${token}`

  try {
    const response = await axios.get('http://localhost:8000/api/users/me/')
    currentUser.value = response.data

    // สร้างเมนูตาม role
    if (currentUser.value.role === 'admin') {
      menuItems.value = [
        { label: 'หน้าหลัก', path: '/admin', icon: 'fas fa-home' },
        { label: 'บุคลากร', path: '/admin2', icon: 'fas fa-users' },
        { label: 'ห้องวิจัย', path: '/admin10', icon: 'fas fa-flask' },
        { label: 'วันหยุด', path: '/admin11', icon: 'fas fa-calendar-alt' },
        { label: 'ระบบการปฏิบัติงาน', path: '/admin12', icon: 'fas fa-cog' },
      ]
    } else if (currentUser.value.role === 'employee') {
      menuItems.value = [
        { label: 'หน้าหลัก', path: '/user', icon: 'fas fa-home' },
        { label: 'ยื่นใบลา', path: '/user2', icon: 'fas fa-file-alt' },
        { label: 'ยื่นใบลาแทน', path: '/user3', icon: 'fas fa-file' },
        { label: 'ประวัติการลา', path: '/user4', icon: 'fas fa-history' },
        { label: 'ขออนุญาตปฏิบัติงานนอกสถานที่', path: '/user5', icon: 'fas fa-briefcase' },
        { label: 'วันหยุด', path: '/user8', icon: 'fas fa-calendar' },
      ]
    }
  } catch (err) {
    console.error(err)
    router.push("/login")
  }
})
</script>

<style scoped>

.sidebar {
  width: 250px;
  background-color: #ffffff;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  padding: 10px;
}

.sidebar-header {
  display: flex;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #eee;
  margin-bottom: 10px;
}

.sidebar-header span {
  font-size: 18px;
  font-weight: bold;
}

.nav-menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  margin-bottom: 5px;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  text-decoration: none;
  color: #555;
  border-radius: 5px;
  transition: background-color 0.2s, color 0.2s;
  cursor: pointer;
}

.nav-link i {
  margin-right: 10px;
  width: 20px;
  text-align: center;
}

.nav-link:hover,
.nav-item.active .nav-link {
  background-color: #e6f7ff;
  color: #1890ff;
}
</style>
