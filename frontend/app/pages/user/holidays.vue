<template>
  <div class="full-page-container">
    

    <main class="main-content">
      <TopBar></TopBar>

      <div class="holidays-container">
        <div class="holidays-header">
          <div class="header-left">
            <i class="fas fa-calendar-alt icon-red"></i>
            <div>
              <h3>วันหยุด/ตาราง</h3>
            </div>
          </div>
          <button type="button" class="btn-calendar" @click="goTo('/user/holidays-calendar')">
            <i class="fas fa-calendar-alt"></i> สลับเป็นรูปแบบปฏิทิน
          </button>
        </div>

        <div class="holiday-table-wrapper">
          <table class="holiday-table">
            <thead>
              <tr>
                <th>วันที่</th>
                <th>ชื่อวันหยุด</th>
                <th>ประเภทวันหยุด</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(holiday, index) in holidays" :key="index">
                <td>{{ holiday.date }}</td>
                <td>{{ holiday.name }}</td>
                <td>{{ holiday.holiday_type_display }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';

import TopBar from '~/components/Topbar.vue'

const user = ref<any>(null);
const token = ref<string | null>(null);
const holidays = ref<any[]>([]);

const router = useRouter();
const route = useRoute();

onMounted(async () => {
  const tokenStored = localStorage.getItem("token");
  if (!tokenStored) {
    router.push("/login");
    return;
  }
  axios.defaults.headers.common['Authorization'] = `Token ${tokenStored}`;

  try {
    
    const responseUser = await axios.get("http://localhost:8000/api/users/me/");
    user.value = responseUser.data;
    if (user.value.role !== "employee") {
      router.push("/login");
    }

    const responseHoliday = await axios.get("http://localhost:8000/api/holiday/list/");
    holidays.value = responseHoliday.data;
  } catch (err) {
    console.error(err);
    router.push("/login");
  }
});

const showProfileMenu = ref(false);
function toggleProfileMenu() {
  showProfileMenu.value = !showProfileMenu.value;
}
function handleBodyClick(event: MouseEvent) {
  if (showProfileMenu.value && !(event.target as HTMLElement).closest('.user-profile')) {
    showProfileMenu.value = false;
  }
}
onMounted(() => {
  document.addEventListener('click', handleBodyClick);
});
onBeforeUnmount(() => {
  document.removeEventListener('click', handleBodyClick);
});

function goTo(path: string) {
  router.push(path);
}
function logout() {
  localStorage.removeItem("token")
  delete axios.defaults.headers.common['Authorization']
  router.push("/login")
}


</script>


<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;700&display=swap');

* {
  box-sizing: border-box;
  font-family: 'Inter', 'Prompt', sans-serif;
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
  border-radius: 50%;
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

.holidays-container {
  background-color: #ffffff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.holidays-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 20px;
}

.header-left {
  display: flex;
  align-items: center;
}

.icon-red {
  color: #e74c3c;
  font-size: 30px;
  margin-right: 15px;
}

.holidays-header h3 {
  margin: 0;
  font-size: 22px;
}

.btn-calendar {
  background: #f1f1f1;
  color: #4caf50;
  padding: 8px 14px;
  border: 1px solid #4caf50;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  font-weight: bold;
  white-space: nowrap;
}

.btn-calendar i {
  margin-right: 5px;
}

.holiday-table-wrapper {
  overflow-x: auto;
}

.holiday-table {
  width: 100%;
  border-collapse: collapse;
}

.holiday-table th,
.holiday-table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

.holiday-table th {
  background-color: #f2f2f2;
  font-weight: bold;
}

.holiday-table tbody tr:nth-child(even) {
  background-color: #fafafa;
}

.holiday-table tbody tr:hover {
  background-color: #e6f7ff;
}
</style>