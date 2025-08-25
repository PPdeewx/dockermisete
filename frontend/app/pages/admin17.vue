<template>
  <div class="full-page-container">
    <div class="sidebar">
      <div class="sidebar-header">
        <span>MIS ETE</span>
      </div>
      <ul class="nav-menu">
        <li class="nav-item">
          <router-link to="/admin16" class="nav-link">
            <i class="fas fa-home"></i> หน้าหลัก
          </router-link>
        </li>
        <li class="nav-item has-submenu active">
          <a href="#" class="nav-link" @click.prevent="toggleSubmenu">
            <i class="fas fa-users"></i> บุคลากร
          </a>
          <ul class="submenu" v-if="showSubmenu">
            <router-link to="/admin18" class="submenu-link" :class="{ 'active': $route.path === '/admin18' }">
              พนักงานปัจจุบัน
            </router-link>
             <router-link to="/admin19" class="submenu-link" :class="{ 'active': $route.path === '/admin19' }">
              พนักงานที่ลาออก
            </router-link>
            <li><a href="#" class="submenu-link">บุคลากรภายนอก</a></li>
            <li><a href="#" class="submenu-link">พนักงาน EDDP</a></li>
            <li><a href="#" class="submenu-link">เพิ่ม/แก้ไข/ลบ พนักงาน</a></li>
            <li><a href="#" class="submenu-link">เพิ่มบุคลากรภายนอก</a></li>
            <li><a href="#" class="submenu-link">เปลี่ยนสถานะพนักงาน</a></li>
            <li><a href="#" class="submenu-link">กำหนดโควต้าลา(ทั้งหมด)</a></li>
            <li><a href="#" class="submenu-link">Reset Quota ประจำปี</a></li>
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
          <span><i class="fas fa-home"></i> หน้าหลัก > บุคลากร > พนักงานปัจจุบัน</span>
        </div>
        <div class="user-profile" @click="toggleUserDropdown">
          <i class="fas fa-bell"></i>
          <i class="fas fa-user-circle"></i>
          <span class="username">Username ตำแหน่ง: Admin</span>
          <i :class="['fas', showUserDropdown ? 'fa-chevron-up' : 'fa-chevron-down']"></i>

          <div class="dropdown-menu" v-if="showUserDropdown">
            <a href="#" class="dropdown-item">ดูข้อมูลส่วนตัว</a>
            <a href="#" class="dropdown-item">แก้ไขข้อมูลส่วนตัว</a>
            <a href="#" class="dropdown-item">เปลี่ยนรหัสผ่าน</a>
            <a href="#" class="dropdown-item">ออกจากระบบ</a>
          </div>
        </div>
      </div>

      <div class="content-container">
        <div class="header-with-button">
          <div class="left-section">
            <i class="fas fa-user-circle title-icon"></i>
            <h2>พนักงานปัจจุบัน</h2>
          </div>
          <button class="add-button"><i class="fas fa-plus"></i> เพิ่มพนักงาน</button>
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
                <tr v-for="(employee, index) in employees" :key="employee.id">
                  <td>{{ index + 1 }}</td>
                  <td>{{ employee.code }}</td>
                  <td>{{ employee.username }}</td>
                  <td>{{ employee.lab }}</td>
                  <td>{{ employee.name }}</td>
                  <td>{{ employee.phone }}</td>
                  <td>{{ employee.email }}</td>
                  <td>
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
import { ref } from 'vue';
import { useRoute } from 'vue-router';

// ใช้ useRoute เพื่อเข้าถึงข้อมูล route ปัจจุบัน
const route = useRoute();

const showSubmenu = ref(true);
const showUserDropdown = ref(false);

const toggleSubmenu = () => {
  showSubmenu.value = !showSubmenu.value;
};

const toggleUserDropdown = () => {
  showUserDropdown.value = !showUserDropdown.value;
};

// ข้อมูลพนักงาน (จำลอง)
const employees = ref([
  { id: 1, code: 'E001', username: 'john.doe', lab: 'Lab A', name: 'นายจอห์น โด', phone: '081-123-4567', email: 'john.d@example.com' },
  { id: 2, code: 'E002', username: 'jane.smith', lab: 'Lab B', name: 'นางสาวเจน สมิท', phone: '082-234-5678', email: 'jane.s@example.com' },
  { id: 3, code: 'E003', username: 'peter.pan', lab: 'Lab C', name: 'นายปีเตอร์ แพน', phone: '083-345-6789', email: 'peter.p@example.com' },
  { id: 4, code: 'E004', username: 'mary.jane', lab: 'Lab A', name: 'นางสาวแมรี่ เจน', phone: '084-456-7890', email: 'mary.j@example.com' },
  { id: 5, code: 'E005', username: 'bruce.wayne', lab: 'Lab B', name: 'นายบรูซ เวย์น', phone: '085-567-8901', email: 'bruce.w@example.com' },
]);
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

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  min-width: 200px;
  margin-top: 10px;
  z-index: 1000;
  padding: 5px 0;
}

.dropdown-item {
  display: block;
  padding: 10px 15px;
  text-decoration: none;
  color: #333;
  transition: background-color 0.2s;
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
</style>