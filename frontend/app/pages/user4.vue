<template>
  <div class="full-page-container">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <span class="logo-text">MIS ETE</span>
      </div>
      <ul class="nav-menu">
        <li class="nav-item" :class="{ 'active': $route.path === '/user' }">
          <router-link to="/user" class="nav-link">
            <i class="fas fa-home"></i> หน้าหลัก
          </router-link>
        </li>
        <li class="nav-item" :class="{ 'active': $route.path === '/user2' }">
          <router-link to="/user2" class="nav-link">
            <i class="fas fa-file-alt"></i> ยื่นใบลา
          </router-link>
        </li>
        <li class="nav-item" :class="{ 'active': $route.path === '/user3' }">
          <router-link to="/user3" class="nav-link">
            <i class="fas fa-user-friends"></i> ยื่นใบลาแทน
          </router-link>
        </li>
        <li class="nav-item" :class="{ 'active': $route.path === '/user4' }">
          <router-link to="/user4" class="nav-link">
            <i class="fas fa-history"></i> ประวัติการลา
          </router-link>
        </li>
        <li class="nav-item" :class="{ 'active': $route.path === '/user5' }">
          <router-link to="/user5" class="nav-link">
            <i class="fas fa-user-edit"></i> ขออนุญาตปฏิบัติงานนอกสถานที่
          </router-link>
        </li>
        <li class="nav-item" :class="{ 'active': $route.path === '/user6' }">
          <router-link to="/user6" class="nav-link">
            <i class="fas fa-user-edit"></i> ขออนุญาตปฏิบัติงานนอกสถานที่ให้คนอื่น
          </router-link>
        </li>
        <li class="nav-item" :class="{ 'active': $route.path === '/user7' }">
          <router-link to="/user7" class="nav-link">
            <i class="fas fa-list-alt"></i> ดูรายการปฏิบัติงานนอกสถานที่
          </router-link>
        </li>
        <li class="nav-item" :class="{ 'active': $route.path === '/user8' }">
          <router-link to="/user8" class="nav-link">
            <i class="fas fa-calendar-alt"></i> วันหยุด
          </router-link>
        </li>
      </ul>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <!-- Top Bar -->
      <div class="top-bar">
        <div class="breadcrumbs">
          <span><i class="fas fa-home"></i> {{ breadcrumbs }}</span>
        </div>
        <div class="user-profile" @click.stop="toggleProfileMenu">
          <i class="fas fa-bell"></i>
          <i class="fas fa-user-circle"></i>
          <span class="username">{{ user?.username }}</span>
          <span v-if="user">ตำแหน่ง: {{ user.role }}</span>
          <i class="fas fa-chevron-down"></i>

          <div class="user-profile-menu" v-if="showProfileMenu">
            <button class="menu-item" @click.stop="goTo('/user10')">
              <i class="fas fa-user"></i>
              <span>ดูข้อมูลส่วนตัว</span>
            </button>
            <button class="menu-item" @click.stop="goTo('/user11')">
              <i class="fas fa-edit"></i>
              <span>แก้ไขข้อมูลส่วนตัว</span>
            </button>
            <button class="menu-item" @click.stop="goTo('/user12')">
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

      <!-- Content Container -->
      <div class="content-container">
        <!-- Header -->
        <div class="content-header">
          <div class="header-left">
            <i class="fas fa-calendar-alt title-icon"></i>
            <h2>ประวัติการลางาน</h2>
          </div>
          <div class="header-right">
            <button class="action-button green" @click="goTo('/user3')"><i class="fas fa-plus"></i> ลาให้คนอื่น</button>
            <button class="action-button green" @click="goTo('/user2')"><i class="fas fa-plus"></i> ขออนุมัติลา</button>
          </div>
        </div>

        <!-- Profile & Summary -->
        <div class="profile-and-summary">
          <div class="profile-card">
            <div class="profile-icon">
              <i class="fas fa-cog gear-icon"></i>
            </div>
            <div class="profile-details">
              <span class="profile-username">{{ user?.username }}</span>
              <span class="profile-id">รหัส {{ user?.employee_code }}</span>
            </div>
          </div>

          <div class="leave-summary">
            <div class="leave-item" v-for="lq in leaveQuotas" :key="lq.id">
              <span>{{ lq.leave_type.name }} คงเหลือ</span>
              <strong>{{ (lq.quota_total - lq.quota_used).toFixed(1) }} วัน</strong>
            </div>
          </div>
        </div>

        <!-- Leave Table -->
        <div class="responsive-table-wrapper">
          <table>
            <thead>
              <tr>
                <th>เลขที่ใบลา</th>
                <th>วันที่ลา</th>
                <th>ประเภทการลา</th>
                <th>ช่วงเวลา</th>
                <th>เหตุผล</th>
                <th>สถานะ</th>
                <th>ดำเนินการ</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="leave in leaves" :key="leave.id">
                <td>{{ leave.leave_number }}</td>
                <td>{{ formatDate(leave.start_date) }} ถึง {{ formatDate(leave.end_date) }}</td>
                <td>{{ leave.leave_type.name }}</td>
                <td>{{ leave.period === 'full' ? 'ทั้งวัน' : (leave.period === 'morning' ? 'ครึ่งเช้า' : 'ครึ่งบ่าย') }}</td>
                <td>{{ leave.reason || '-' }}</td>
                <td>{{ leave.status_display }}</td>
                <td>
                  <i class="fas fa-edit action-icon" @click="goTo(`/user13/${leave.id}`)"></i>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';

const user = ref(null);
const leaves = ref([]);
const leaveQuotas = ref([]);
const showProfileMenu = ref(false);

const router = useRouter();
const route = useRoute();

function toggleProfileMenu() {
  showProfileMenu.value = !showProfileMenu.value;
}

function handleBodyClick(event) {
  if (showProfileMenu.value && !event.target.closest('.user-profile')) {
    showProfileMenu.value = false;
  }
}

onMounted(() => {
  document.addEventListener('click', handleBodyClick);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleBodyClick);
});

// Fetch user info and leaves
async function fetchData() {
  const tokenStored = localStorage.getItem("token");
  if (!tokenStored) {
    router.push("/login");
    return;
  }
  axios.defaults.headers.common['Authorization'] = `Token ${tokenStored}`;

  try {
    const resUser = await axios.get("http://localhost:8000/api/users/me/");
    user.value = resUser.data;
    if (user.value.role !== "employee") router.push("/login");

    const resLeaves = await axios.get("http://localhost:8000/api/leave/leave-requests/");
    const dataLeaves = resLeaves.data.results || resLeaves.data || [];
    leaves.value = dataLeaves.map(l => ({
      ...l,
      status_display: mapStatus(l.status)
    }));

    //const resQuotas = await axios.get("http://localhost:8000/api/leave/leave-quotas/");
    //leaveQuotas.value = resQuotas.data;

  } catch (err) {
    console.error(err);
    router.push("/login");
  }
}

function mapStatus(status) {
  switch(status) {
    case 'pending': return 'รอการอนุมัติ';
    case 'approved': return 'อนุมัติ';
    case 'rejected': return 'ไม่อนุมัติ';
    case 'cancelled': return 'ยกเลิก';
    default: return status;
  }
}

function formatDate(dateStr) {
  const d = new Date(dateStr);
  return `${d.getDate()}/${d.getMonth()+1}/${d.getFullYear()+543}`;
}

const goTo = (path) => router.push(path);

function logout() {
  localStorage.removeItem("token");
  delete axios.defaults.headers.common['Authorization'];
  router.push("/login");
}

onMounted(() => {
  fetchData();
});

const breadcrumbs = computed(() => {
  switch (route.path) {
    case '/user': return 'หน้าหลัก';
    case '/user2': return 'หน้าหลัก > ยื่นใบลา';
    case '/user3': return 'หน้าหลัก > ยื่นใบลาแทน';
    case '/user4': return 'หน้าหลัก > ประวัติการลา';
    case '/user5': return 'หน้าหลัก > ขออนุญาตปฏิบัติงานนอกสถานที่';
    case '/user6': return 'หน้าหลัก > ขออนุญาตปฏิบัติงานนอกสถานที่ให้คนอื่น';
    case '/user7': return 'หน้าหลัก > ดูรายการปฏิบัติงานนอกสถานที่';
    case '/user8': return 'หน้าหลัก > วันหยุด';
    case '/user10': return 'หน้าหลัก > ข้อมูลส่วนตัว';
    case '/user11': return 'หน้าหลัก > ข้อมูลส่วนตัว > แก้ไข';
    case '/user12': return 'หน้าหลัก > เปลี่ยนรหัสผ่าน';
    case '/user13': return 'หน้าหลัก > ประวัติการลา > แก้ไข';
    default: return 'หน้าหลัก';
  }
});
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

.logo-text {
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
  justify-content: flex-start;
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
  display: flex;
  align-items: center;
  position: relative; 
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

.content-container {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.content-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #eee;
    padding-bottom: 15px;
    margin-bottom: 20px;
}

.header-left {
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

.header-right .action-button {
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s;
  white-space: nowrap;
  color: white;
  margin-left: 10px;
}

.header-right .action-button.green {
  background-color: #28a745;
}
.header-right .action-button.green:hover {
  background-color: #218838;
}

.profile-and-summary {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.profile-card {
  display: flex;
  align-items: center;
  background-color: #f7f7f7;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  width: 300px;
}

.profile-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: #e9ecef;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 15px;
}

.gear-icon {
  font-size: 30px;
  color: #888;
}

.profile-details {
  display: flex;
  flex-direction: column;
}

.profile-username {
  font-weight: bold;
  font-size: 16px;
}

.profile-id {
  font-size: 12px;
  color: #666;
}

.leave-summary {
    display: flex;
    flex-wrap: wrap;
}

.leave-item {
    display: flex;
    flex-direction: column;
    text-align: center;
    background-color: #e6f7ff;
    border: 1px solid #c9e9ff;
    border-radius: 8px;
    padding: 15px;
    margin-left: 10px;
    width: 150px;
}
.leave-item span {
    font-size: 14px;
    color: #555;
    margin-bottom: 5px;
}
.leave-item strong {
    font-size: 20px;
    color: #1890ff;
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

td .action-icon {
  margin-right: 8px;
  color: #3f68a8;
  cursor: pointer;
  transition: color 0.2s;
}

td .action-icon:hover {
  color: #305488;
}

tr:nth-child(even) {
  background-color: #fafafa;
}

@media (max-width: 992px) {
  .profile-and-summary {
    flex-direction: column;
    align-items: flex-start;
  }
  .leave-summary {
    margin-top: 15px;
    margin-left: -10px; 
  }
  .profile-card {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .sidebar {
    width: 200px;
  }
  .top-bar {
    padding: 10px;
  }
  .user-profile .username {
    display: none;
  }
  .content-header {
    flex-direction: column;
    align-items: flex-start;
  }
  .header-right {
    margin-top: 10px;
  }
}
</style>