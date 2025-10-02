<template>
  <div class="sidebar">
    <div class="sidebar-header">
      <span>MIS ETE</span>
    </div>
    <ul class="nav-menu">
      <li
        v-for="item in menuItems"
        :key="item.label"
        class="nav-item"
        :class="{ 'has-submenu': item.submenu, open: openMenu === item.label }"
      >
       
        <a
          @click.prevent="item.submenu ? toggleSubmenu(item.label) : goTo(item.path)"
          class="nav-link"
        >
          <i :class="item.icon"></i> {{ item.label }}
          <span v-if="item.submenu" class="arrow" :class="{ rotated: openMenu === item.label }">▶</span>
        </a>

        <ul v-if="item.submenu" class="submenu" v-show="openMenu === item.label">
          <li v-for="sub in item.submenu" :key="sub.label">
            <a @click.prevent="goTo(sub.path)" class="submenu-link">{{ sub.label }}</a>
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
const openMenu = ref<string | null>(null)

const goTo = (path: string) => {
  router.push(path)
}

const toggleSubmenu = (label: string) => {
  openMenu.value = openMenu.value === label ? null : label
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

    if (currentUser.value.role === 'admin') {
      menuItems.value = [
        { label: 'หน้าหลัก', path: '/admin', icon: 'fas fa-home' },
        {
          label: 'บุคลากร',
          icon: 'fas fa-users',
          submenu: [
            { label: 'พนักงานปัจจุบัน', path: '/admin/person/current' },
            { label: 'พนักงานที่ลาออก', path: '/admin/person/resign' },
            { label: 'บุคลากรภายนอก', path: '/admin/person/external' },
            { label: 'พนักงาน EDDP', path: '/admin/person/eddp' },
            { label: 'เพิ่ม/แก้ไข/ลบ พนักงาน', path: '/admin/person/edit-employees' },
            { label: 'เพิ่มบุคลากรภายนอก', path: '/admin/person/add-external' },
            { label: 'เปลี่ยนสถานะพนักงาน', path: '/admin/person/change-status' },
            { label: 'กำหนดโควต้าลา(ทั้งหมด)', path: '/admin/person/quota' }
          ]
        },
        { label: 'ห้องวิจัย', path: '/admin/research', icon: 'fas fa-flask' },
        { label: 'วันหยุด', path: '/admin/sehedule', icon: 'fas fa-calendar-alt' },
        { 
          label: 'ระบบการปฏิบัติงาน',
          icon: 'fas fa-cog',
          submenu: [
            { label: 'ตรวจสอบเวลาทำงาน', path: '/admin/system/work-hours' },
            { label: 'เวลางานคนลาออก', path: '/admin/system/resign-period' },
            { label: 'รายการลาตัวเอง', path: '/admin/system/leave-list' },
            { label: 'รายการลา ETE', path: '/admin/system/leave-list-ete' },
            { label: 'ปฏิบัติงานนอกสถานที่', path: '/admin/system/outside-work.' },
            { label: 'รายการอนุมัติการลาปฏิบัติงานนอกสถานที่', path: '/admin/system/osl-approval' },
            { label: 'รายการอนุมัติการลา', path: '/admin/system/approve-leave' },
            { label: 'ขออนุมัติลา', path: '/admin/system/leave-approval' },
            { label: 'ขอลาให้คนอื่น', path: '/admin/system/substitute-leave' },
            { label: 'ขอปฏิบัติงานนอกสถานที่', path: '/admin/system/off-site-request' },
            { label: 'ขอปฏิบัติงานนอกสถานที่ให้คนอื่น', path: '/admin/system/outside-work-request' },
            { label: 'Upload เวลางาน', path: '/admin/system/upload' },
          ]
        }
      ]
      
    } else if (currentUser.value.role === 'employee') {
      menuItems.value = [
        { label: 'หน้าหลัก', path: '/user', icon: 'fas fa-home' },
        {
          label: 'ลา',
          icon: 'fas fa-file-alt',
          submenu: [
            { label: 'ยื่นใบลา', path: '/user/leave-request', icon: 'fas fa-file-alt' },
            { label: 'ยื่นใบลาแทน', path: '/user/leave-request-for-others', icon: 'fas fa-file' },
            { label: 'ประวัติการลา', path: '/user/leave-history', icon: 'fas fa-history' },
          ]
        },
        {
          label: 'ปฏิบัติงานนอกสถานที่',
          icon: 'fas fa-briefcase',
          submenu: [
            { label: 'ขออนุญาตปฏิบัติงานนอกสถานที่', path: '/user/work-outside-request', icon: 'fas fa-briefcase' },
            { label: 'ขออนุญาตปฏิบัติงานนอกสถานที่ให้คนอื่น', path: '/user/work-outside-request-for-others', icon: 'fas fa-briefcase' },
            { label: 'ประวัติปฏิบัติงานนอกสถานที่', path: '/user/work-outside-history', icon: 'fas fa-briefcase' },
          ]
        },
        { label: 'วันหยุด', path: '/user/holidays', icon: 'fas fa-calendar' },
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
  justify-content: space-between;
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

.submenu {
  list-style: none;
  margin: 5px 0 5px 15px;
  padding: 0;
}

.submenu-link {
  display: block;
  padding: 8px 15px;
  font-size: 14px;
  color: #555;
  border-radius: 4px;
  text-decoration: none;
  transition: background-color 0.2s;
  cursor: pointer;
}

.submenu-link:hover {
  background-color: #f0f8ff;
  color: #1890ff;
}

.arrow {
  font-size: 12px;
  transition: transform 0.3s;
  margin-left: auto;
}

.arrow.rotated {
  transform: rotate(90deg);
}
</style>
