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
        <li class="nav-item has-submenu active">
          <a href="#" class="nav-link"><i class="fas fa-users"></i> บุคลากร</a>
          <ul class="submenu active">
            <li><a href="#" class="submenu-link">พนักงานปัจจุบัน</a></li>
            <li><a href="#" class="submenu-link">พนักงานที่ลาออก</a></li>
            <li><a href="#" class="submenu-link active">บุคลากรภายนอก</a></li>
            <li><a href="#" class="submenu-link">พนักงาน EDDP</a></li>
            <li><a href="#" class="submenu-link">เพิ่ม/แก้ไข/ลบ พนักงาน</a></li>
            <li><a href="#" class="submenu-link">เพิ่มบุคลากรภายนอก</a></li>
            <li><a href="#" class="submenu-link">เปลี่ยนสถานะพนักงาน</a></li>
            <li><a href="#" class="submenu-link">กำหนดโควต้าลา(ทั้งหมด)</a></li>
          </ul>
        </li>
        <li class="nav-item">
          <a href="#" class="nav-link"><i class="fas fa-flask"></i> ห้องวิจัย</a>
        </li>
        <li class="nav-item">
          <a href="#" class="nav-link"><i class="fas fa-calendar-alt"></i> วันหยุด</a>
        </li>
        <li class="nav-item">
          <a href="#" class="nav-link"><i class="fas fa-cog"></i> ระบบการปฏิบัติงาน</a>
        </li>
      </ul>
    </div>

    <div class="main-content">
      <div class="top-bar">
        <div class="breadcrumbs">
          <span><i class="fas fa-home"></i> หน้าหลัก > บุคลากร > บุคลากรภายนอก</span>
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
        <div class="header-with-button">
          <div class="left-section">
            <i class="fas fa-user-circle title-icon"></i>
            <h2>บุคลากรภายนอก</h2>
          </div>
          <div class="right-section">
            <button class="add-external-staff-button">
              <i class="fas fa-plus-circle"></i>
              เพิ่มบุคลากรภายนอก
            </button>
          </div>
        </div>

        <div class="search-and-table-container">
          <div class="search-bar-container">
            <label for="search">SEARCH :</label>
            <input type="text" id="search" placeholder="" class="search-input">
          </div>

          <div class="responsive-table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>ลำดับที่</th>
                  <th>รหัส</th>
                  <th>Username</th>
                  <th>Lab</th>
                  <th>ชื่อภาษาไทย</th>
                  <th>เบอร์โทรศัพท์</th>
                  <th>Email</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="i in 10" :key="i">
                  <td>{{ i }}</td>
                  <td></td>
                  <td></td>
                  <td></td>
                  <td></td>
                  <td></td>
                  <td></td>
                  <td>
                    <i class="fas fa-search action-icon view-icon"></i>
                    <i class="fas fa-edit action-icon edit-icon"></i>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const token = ref<string | null>(null);
const currentUser = ref<any>(null)

const showProfileMenu = ref(false)
const toggleProfileMenu = () => {
  showProfileMenu.value = !showProfileMenu.value
}

const goTo = (path: string) => {
  router.push(path);
};

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

.logo {
  width: 40px;
  height: 40px;
  margin-right: 10px;
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

.nav-item.has-submenu .arrow {
  transition: transform 0.3s ease-in-out;
}

.nav-item.has-submenu.active .arrow {
  transform: rotate(90deg);
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
  position: relative;
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
  transition: background-color 0.2s;
}

.dropdown-item i {
  margin-right: 12px;
  font-size: 16px;
  width: 20px;
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

.left-section {
  display: flex;
  align-items: center;
}

.title-icon {
  font-size: 24px;
  color: #888;
  margin-right: 10px;
}

h2 {
  margin: 0;
  font-size: 20px;
}

.add-button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.add-button:hover {
  background-color: #45a049;
}

.search-and-table-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.search-bar-container {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 10px;
}

.search-input {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 8px 12px;
}

.responsive-table-wrapper {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
  white-space: nowrap;
}

th {
  background-color: #f2f2f2;
  font-weight: bold;
}

tr:nth-child(even) {
  background-color: #fafafa;
}

.add-external-staff-button {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  border-radius: 5px;
  border: none;
  background-color: #4CAF50;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.add-external-staff-button:hover {
  background-color: #45a049;
}

.add-external-staff-button i {
  margin-right: 5px;
}

.action-icon {
  font-size: 20px;
  margin-right: 10px;
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
}

.action-icon:hover {
  transform: scale(1.1);
}

.view-icon {
  color: #1890ff;
}

.edit-icon {
  color: #fadb14;
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