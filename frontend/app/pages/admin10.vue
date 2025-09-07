<template>
  <div class="full-page-container">
    <div class="sidebar">
      <div class="sidebar-header">
        <span>MIS ETE</span>
      </div>
      <ul class="nav-menu">
        <li class="nav-item">
          <a href="#" class="nav-link"><i class="fas fa-home"></i> หน้าหลัก</a>
        </li>
        <li class="nav-item has-submenu">
          <a href="#" class="nav-link"><i class="fas fa-users"></i> บุคลากร</a>
          <ul class="submenu">
            <li><a href="#" class="submenu-link">พนักงานปัจจุบัน</a></li>
            <li><a href="#" class="submenu-link">พนักงานที่ลาออก</a></li>
            <li><a href="#" class="submenu-link">บุคลากรภายนอก</a></li>
            <li><a href="#" class="submenu-link">พนักงาน EDDP</a></li>
            <li><a href="#" class="submenu-link">เพิ่ม/แก้ไข/ลบ พนักงาน</a></li>
            <li><a href="#" class="submenu-link">เพิ่มบุคลากรภายนอก</a></li>
            <li><a href="#" class="submenu-link">เปลี่ยนสถานะพนักงาน</a></li>
            <li><a href="#" class="submenu-link">กำหนดโควต้าลา(ทั้งหมด)</a></li>
          </ul>
        </li>
        <li class="nav-item active">
          <a href="#" class="nav-link"><i class="fas fa-flask"></i> ห้องวิจัย</a>
        </li>
        <li class="nav-item"><a href="#" class="nav-link"><i class="fas fa-calendar-alt"></i> วันหยุด</a></li>
        <li class="nav-item"><a href="#" class="nav-link"><i class="fas fa-cog"></i> ระบบการปฏิบัติงาน</a></li>
      </ul>
    </div>

    <div class="main-content">
      <div class="top-bar">
        <div class="breadcrumbs">
          <span><i class="fas fa-home"></i> หน้าหลัก > ห้องวิจัย</span>
        </div>
        <div class="user-profile-container">
          <div class="user-profile" @click="toggleDropdown">
            <i class="fas fa-bell"></i>
            <i class="fas fa-user-circle"></i>
            <span class="username">Username ตำแหน่ง: Admin</span>
            <i class="fas fa-chevron-down" :class="{ 'rotate': isDropdownOpen }"></i>
          </div>
          <div class="dropdown-menu" v-if="isDropdownOpen">
            <a href="#" class="dropdown-item"><i class="fas fa-user"></i> ดูข้อมูลส่วนตัว</a>
            <a href="#" class="dropdown-item"><i class="fas fa-user-edit"></i> แก้ไขข้อมูลส่วนตัว</a>
            <a href="#" class="dropdown-item"><i class="fas fa-fingerprint"></i> เปลี่ยนรหัสผ่าน</a>
            <a href="#" class="dropdown-item"><i class="fas fa-sign-out-alt"></i> ออกจากระบบ</a>
          </div>
        </div>
      </div>

      <div class="content-container">
        <div class="header-with-button">
          <h2><i class="fas fa-flask"></i> ห้องวิจัย</h2>
          <button class="btn-add-room" @click="addRoom">
            <i class="fas fa-plus"></i> เพิ่มห้องวิจัย
          </button>
        </div>
        
        <div class="room-list">
          <div v-for="dept in departments" :key="dept.id" class="room-card">
            <div class="room-card-header">
              <h3>
                {{ dept.name_th }}<br>
                <small>{{ dept.name_en }}</small>
              </h3>
              <div class="room-actions">
                <button class="btn-action edit" @click="editDepartment(dept)"><i class="fas fa-edit"></i></button>
                <button class="btn-action delete" @click="deleteDepartment(dept)"><i class="fas fa-times"></i></button>
              </div>
            </div>
            <div class="room-card-body">
              <p>
                <strong>หัวหน้าห้องวิจัย : </strong>{{ dept.head || '-' }}
              </p>
              <div class="personnel-list">
                <strong>บุคลากร :</strong>
                <ol v-if="dept.personnel && dept.personnel.length">
                  <li v-for="(person, pIndex) in dept.personnel" :key="pIndex">{{ person }}</li>
                </ol>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const isDropdownOpen = ref(false)
const toggleDropdown = () => { isDropdownOpen.value = !isDropdownOpen.value }

const departments = ref<any[]>([])

onMounted(async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/users/departments/', {
      headers: { Authorization: `Token ${localStorage.getItem('token')}` }
    })
    departments.value = res.data
  } catch (err) {
    console.error(err)
  }
})

const addDepartment = () => {
  alert('ฟังก์ชันสำหรับเพิ่ม Department')
}

const editDepartment = (dept: any) => {
  alert(`แก้ไขข้อมูลห้องวิจัย: ${dept.name_th}`)
}

const deleteDepartment = async (dept: any) => {
  if (confirm(`คุณต้องการลบห้องวิจัย ${dept.name_th} หรือไม่?`)) {
    try {
      await axios.delete(`http://localhost:8000/api/users/departments/${dept.id}/`, {
        headers: { Authorization: `Token ${localStorage.getItem('token')}` }
      })
      departments.value = departments.value.filter(d => d.id !== dept.id)
    } catch (err: any) {
      alert(err.response?.data?.detail || 'ลบไม่สำเร็จ')
    }
  }
}
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;700&display=swap');

* {
  box-sizing: border-box;
  font-family: 'Noto Sans Thai', sans-serif;
}

.full-page-container {
  display: flex;
  min-height: 100vh;
  background-color: #f0f2f5;
  color: #333;
}

.sidebar {
  width: 350px;
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
  padding: 0;
  margin-left: 15px;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease-in-out;
}

.nav-item.has-submenu.active .submenu {
  max-height: 500px;
}

.submenu-link {
  display: block;
  padding: 8px 15px 8px 45px;
  text-decoration: none;
  color: #555;
  border-left: 3px solid transparent;
  transition: all 0.2s;
}

.submenu-link:hover,
.submenu-link.active {
  background-color: #f5f5f5;
  border-left: 3px solid #1890ff;
  color: #1890ff;
}

.main-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

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
  position: relative;
}

.user-profile {
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

.user-profile .fa-chevron-down {
  transition: transform 0.3s ease-in-out;
}

.user-profile .fa-chevron-down.rotate {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  margin-top: 10px;
  z-index: 100;
  min-width: 220px;
  padding: 10px 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 10px 20px;
  text-decoration: none;
  color: #333;
}

.dropdown-item i {
  margin-right: 12px;
  font-size: 16px;
}

.dropdown-item:hover {
  background-color: #f5f5f5;
}

.content-container {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header-with-button {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 20px;
}

.header-with-button h2 {
  font-size: 24px;
  font-weight: bold;
}

.btn-add-room {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  display: flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
}

.btn-add-room:hover {
  background-color: #45a049;
}

.room-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.room-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  background-color: #fff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.room-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.room-card-header h3 {
  margin: 0;
  font-size: 1.2em;
  font-weight: bold;
  line-height: 1.4;
}

.room-card-header small {
  color: #666;
  font-size: 0.9em;
  font-weight: normal;
}

.room-actions {
  display: flex;
  gap: 10px;
}

.btn-action {
  background: none;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 8px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 1em;
}

.btn-action.edit {
  color: #1890ff;
  border-color: #1890ff;
}

.btn-action.edit:hover {
  background-color: #e6f7ff;
}

.btn-action.delete {
  color: #f5222d;
  border-color: #f5222d;
}

.btn-action.delete:hover {
  background-color: #fff1f0;
}

.room-card-body p {
  margin: 0 0 10px 0;
}

.personnel-list {
  font-size: 0.9em;
  line-height: 1.6;
}

.personnel-list ol {
  padding-left: 25px;
  margin-top: 5px;
}

.personnel-list li {
  margin-bottom: 2px;
}
</style>