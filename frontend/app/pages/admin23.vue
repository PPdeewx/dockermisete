<template>
  <div class="full-page-container">
    <div class="sidebar">
      <div class="sidebar-header">
        <span>MIS ETE</span>
      </div>
        <ul class="nav-menu">
         <li class="nav-item">
       <a href="/admin" class="nav-link" @click.prevent="goToAdminPage">
     <i class="fas fa-home"></i> หน้าหลัก
   </a>
</li>
        <li class="nav-item has-submenu">
          <a href="/admin2" class="nav-link"@click.prevent="goToAdmin2Page">
            <i class="fas fa-users"></i> บุคลากร
          </a>
        </li>
        <li class="nav-item"><a href="/admin10" class="nav-link" @click.prevent="goToAdmin10Page"><i class="fas fa-flask"></i> ห้องวิจัย</a></li>
        <li class="nav-item"><a href="/admin11" class="nav-link" @click.prevent="goToAdmin11Page"><i class="fas fa-calendar-alt"></i> วันหยุด</a></li>
        <li class="nav-item active has-submenu">
          <a href="#" class="nav-link"><i class="fas fa-cog"></i> ระบบการปฏิบัติงาน</a>
          <ul class="submenu">
            <li><a href="/admin12" class="submenu-link">ตรวจสอบเวลาทำงาน</a></li>
            <li><a href="/admin13" class="submenu-link">เวลางานคนลาออก</a></li>
            <li><a href="/admin14" class="submenu-link">รายการลาตัวเอง</a></li>
            <li><a href="/admin15" class="submenu-link">รายการลา ETE</a></li>
            <li><a href="/admin16" class="submenu-link">ปฏิบัติงานนอกสถานที่</a></li>
            <li><a href="/admin17" class="submenu-link">รายการอนุมัติการลาปฏิบัติงานนอกสถานที่</a></li>
            <li><a href="/admin18" class="submenu-link">รายการอนุมัติการลา</a></li>
            <li><a href="/admin19" class="submenu-link">ขออนุมัติลา</a></li>
            <li><a href="/admin20" class="submenu-link">ขอลาให้คนอื่น</a></li>
            <li><a href="/admin21" class="submenu-link">ขอปฏิบัติงานนอกสถานที่</a></li>
            <li><a href="/admin22" class="submenu-link">ขอปฏิบัติงานนอกสถานที่ให้คนอื่น</a></li>
            <li><a href="#" class="submenu-link active">Upload เวลางาน</a></li>
          </ul>
        </li>
      </ul>
    </div>

    <div class="main-content">
      <div class="top-bar">
        <div class="breadcrumbs">
          <span><i class="fas fa-home"></i> หน้าหลัก > Upload เวลางาน</span>
        </div>
        <div class="user-profile-container">
          <div class="user-profile" @click="toggleProfileMenu">
            <i class="fas fa-bell"></i>
            <i class="fas fa-user-circle"></i>
            <span class="username">{{ currentUser?.username }} ตำแหน่ง: {{ currentUser?.role }}</span>
            <i :class="['fas', showProfileMenu ? 'fa-chevron-up' : 'fa-chevron-down']"></i>

            <div class="user-profile-menu" v-if="showProfileMenu">
              <button class="menu-item" @click.stop="goTo('/admin28')">
                <i class="fas fa-user"></i>
                <span>ดูข้อมูลส่วนตัว</span>
              </button>
              <button class="menu-item" @click.stop="goTo('/admin29')">
                <i class="fas fa-edit"></i>
                <span>แก้ไขข้อมูลส่วนตัว</span>
              </button>
              <button class="menu-item" @click.stop="goTo('/admin30')">
                <i class="fas fa-lock"></i>
                <span>เปลี่ยนรหัสผ่าน</span>
              </button>
              <button class="menu-item" @click.stop="logout">
                <i class="fas fa-sign-out-alt"></i>
                <span>ออกจากระบบ</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="content-container">
        <div class="header-with-buttons">
          <h2><i class="fas fa-calendar-alt"></i> UPLOAD เวลางาน</h2>
        </div>
        
        <div class="table-controls">
          <button class="btn-upload">UPLOAD ไฟล์ Excel</button>
          <div class="search-container">
            <input type="text" placeholder="ค้นหา" class="search-input">
            <button class="btn-search"><i class="fas fa-search"></i> ค้นหา</button>
          </div>
          <button class="btn-export">Export</button>
        </div>
        
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>วันที่</th>
                <th>รหัสพนักงาน</th>
                <th>ชื่อ - นามสกุล</th>
                <th>เวลาเข้างาน</th>
                <th>เวลาออกงาน</th>
                <th>มาสาย (นาที)</th>
                <th>ออกก่อน</th>
                <th>สถานะ</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>13/ส.ค./2568</td>
                <td>001</td>
                <td>นายแอดมิน แอดมิน</td>
                <td>09:00</td>
                <td>17:00</td>
                <td>10</td>
                <td>0</td>
                <td>เข้างานปกติ</td>
              </tr>
              <tr>
                <td>14/ส.ค./2568</td>
                <td>002</td>
                <td>นายสมชาย มีสุข</td>
                <td>09:30</td>
                <td>17:00</td>
                <td>30</td>
                <td>0</td>
                <td>มาสาย</td>
              </tr>
              <tr>
                <td>15/ส.ค./2568</td>
                <td>003</td>
                <td>นางสาวสมศรี ใจดี</td>
                <td>09:00</td>
                <td>16:30</td>
                <td>0</td>
                <td>30</td>
                <td>ออกก่อน</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const token = ref<string | null>(null);

const showProfileMenu = ref(false)
const toggleProfileMenu = () => {
  showProfileMenu.value = !showProfileMenu.value
}

const goTo = (path: string) => {
  router.push(path);
};

const goToAdminPage = () => {
  router.push('/admin');
};

const goToAdmin2Page = () => {
  window.location.href = '/admin2';
};

const goToAdmin10Page = () => {
  window.location.href = '/admin10';
};

const goToAdmin11Page = () => {
  window.location.href = '/admin11';
};

const uploadFile = () => {
  alert('อัปโหลดไฟล์...');
};

const searchData = () => {
  alert('ค้นหาข้อมูล...');
};

const exportData = () => {
  alert('Export ข้อมูล...');
};

const saveData = () => {
  alert('บันทึกข้อมูล...');
};

const currentUser = ref<any>(null)

onMounted(async () => {
  if (typeof window !== "undefined") {
    token.value = localStorage.getItem("token")
  }

  if (!token.value) {
    router.push('/login')
    return
  }

  axios.defaults.headers.common['Authorization'] = `Token ${token.value}`

  try {
    const me = await axios.get('http://localhost:8000/api/users/me/')
    currentUser.value = me.data;

    if (currentUser.value.role !== 'admin') {
      router.push('/login');
      return;
    }
  } catch (err) {
    console.error(err)
    router.push('/login')
  }
})

function logout() {
  if (typeof window !== "undefined") {
    localStorage.removeItem("token")
  }
  delete axios.defaults.headers.common['Authorization']
  router.push("/login")
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

.header-with-buttons {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 20px;
}

.header-with-buttons h2 {
  font-size: 24px;
  font-weight: bold;
}

.header-with-buttons h2 i {
  margin-right: 10px;
  color: #ff9800;
}

.table-controls {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-bottom: 20px;
  gap: 10px;
}

.btn-upload {
  background-color: #1890ff;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  font-weight: bold;
}

.btn-upload:hover {
  background-color: #096dd9;
}

.search-container {
  display: flex;
  border: 1px solid #ccc;
  border-radius: 5px;
  overflow: hidden;
}

.search-input {
  border: none;
  padding: 8px 12px;
  width: 200px;
  font-size: 1em;
}

.search-input:focus {
  outline: none;
}

.btn-search {
  background-color: #1890ff;
  color: white;
  border: none;
  padding: 8px 15px;
  cursor: pointer;
}

.btn-search:hover {
  background-color: #096dd9;
}

.btn-export {
  background-color: #fff;
  color: #1890ff;
  border: 1px solid #1890ff;
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
}

.btn-export:hover {
  background-color: #f0f2f5;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

thead th {
  background-color: #007bff;
  color: white;
}

.save-actions {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}

.btn-save {
  background-color: #52c41a;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.2s;
}

.btn-save:hover {
  background-color: #389e08;
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