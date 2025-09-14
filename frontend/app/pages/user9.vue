<template>
  <div class="full-page-container">
    <aside class="sidebar">
      <div class="sidebar-header">
        <span>MIS ETE</span>
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
            <i class="fas fa-file-alt"></i> ยื่นใบลาเเทน
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
            <i class="fas fa-calendar-times"></i> ดูรายการปฏิบัติงานนอกสถานที่
          </router-link>
        </li>
        <li class="nav-item" :class="{ 'active': $route.path === '/user8' || $route.path === '/user9' }">
          <router-link to="/user8" class="nav-link">
            <i class="fas fa-calendar-plus"></i> วันหยุด
          </router-link>
        </li>
      </ul>
    </aside>

    <div class="main-content">
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

      <div class="holidays-container">
        <div class="holidays-header">
          <div class="header-left">
            <i class="fas fa-calendar-alt icon-red"></i>
            <div>
              <h3>วันหยุด/ปฏิทิน</h3>
            </div>
          </div>
          <button type="button" class="btn-table" @click="goTo('/user8')">
            <i class="fas fa-table"></i> สลับเป็นรูปแบบตาราง
          </button>
        </div>

        <div class="calendar-header">
          <button @click="prevMonth" class="month-btn"><i class="fas fa-chevron-left"></i></button>
          <span class="month-label">{{ getMonthName(currentMonth) }} {{ currentYear }}</span>
          <button @click="nextMonth" class="month-btn"><i class="fas fa-chevron-right"></i></button>
        </div>

        <div class="calendar-view">
          <table class="calendar-table">
            <thead>
              <tr>
                <th>จันทร์</th>
                <th>อังคาร</th>
                <th>พุธ</th>
                <th>พฤหัสบดี</th>
                <th>ศุกร์</th>
                <th>เสาร์</th>
                <th>อาทิตย์</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="week in calendarWeeks" :key="week[0].date">
                <td v-for="day in week" :key="day.date"
                    :class="{'holiday': isHoliday(day.date), 'today': isToday(day.date)}">
                  <div v-if="day.date">
                    <div class="date-text">{{ formatDate(day.date) }}</div>
                    <div v-if="isHoliday(day.date)" class="holiday-name">
                      {{ getHolidayName(day.date) }}
                    </div>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';

const user = ref<any>(null);
const holidays = ref<any[]>([]);
const showProfileMenu = ref(false);

const currentMonth = ref(new Date().getMonth());
const currentYear = ref(new Date().getFullYear());

const router = useRouter();
const route = useRoute();

function toggleProfileMenu() {
  showProfileMenu.value = !showProfileMenu.value;
}

function handleBodyClick(event: MouseEvent) {
  if (showProfileMenu.value && !(event.target as HTMLElement).closest('.user-profile')) {
    showProfileMenu.value = false;
  }
}

function goTo(path: string) {
  router.push(path);
}

function logout() {
  localStorage.removeItem("token");
  delete axios.defaults.headers.common['Authorization'];
  router.push("/login");
}

onMounted(() => {
  document.addEventListener('click', handleBodyClick);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleBodyClick);
});

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

function isHoliday(dateStr: string) {
  return holidays.value.some(h => h.date === dateStr);
}
function getHolidayName(dateStr: string) {
  const h = holidays.value.find(h => h.date === dateStr);
  return h ? h.name : '';
}

const calendarWeeks = computed(() => {
  const weeks: any[] = [];
  const month = currentMonth.value;
  const year = currentYear.value;

  const firstDayOfMonth = new Date(year, month, 1);
  const lastDayOfMonth = new Date(year, month + 1, 0);

  let week: any[] = [];

  // เริ่มวันจันทร์
  let startDay = firstDayOfMonth.getDay();
  startDay = startDay === 0 ? 6 : startDay - 1;

  for (let i = 0; i < startDay; i++) {
    week.push({ day: '', date: '' });
  }

  for (let day = 1; day <= lastDayOfMonth.getDate(); day++) {
    const dateStr = `${year}-${String(month + 1).padStart(2,'0')}-${String(day).padStart(2,'0')}`;
    week.push({ day, date: dateStr });

    if (week.length === 7) {
      weeks.push(week);
      week = [];
    }
  }

  if (week.length) {
    while (week.length < 7) week.push({ day: '', date: '' });
    weeks.push(week);
  }

  return weeks;
});

function isToday(dateStr: string) {
  const today = new Date();
  const d = new Date(dateStr);
  return d.toDateString() === today.toDateString();
}

function formatDate(dateStr: string) {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  const day = String(d.getDate()).padStart(2, '0');
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const year = d.getFullYear();
  return `${day}/${month}/${year}`;
}

function prevMonth() {
  if (currentMonth.value === 0) {
    currentMonth.value = 11;
    currentYear.value -= 1;
  } else {
    currentMonth.value -= 1;
  }
}

function nextMonth() {
  if (currentMonth.value === 11) {
    currentMonth.value = 0;
    currentYear.value += 1;
  } else {
    currentMonth.value += 1;
  }
}

function getMonthName(monthIndex: number) {
  const monthNames = ['มกราคม','กุมภาพันธ์','มีนาคม','เมษายน','พฤษภาคม','มิถุนายน','กรกฎาคม','สิงหาคม','กันยายน','ตุลาคม','พฤศจิกายน','ธันวาคม'];
  return monthNames[monthIndex];
}

const breadcrumbs = computed(() => {
  switch (route.path) {
    case '/user':
      return 'หน้าหลัก';
    case '/user2':
      return 'หน้าหลัก > ยื่นใบลา';
    case '/user3':
      return 'หน้าหลัก > ยื่นใบลาแทน';
    case '/user4':
      return 'หน้าหลัก > ประวัติการลา';
    case '/user5':
      return 'หน้าหลัก > ขออนุญาตปฏิบัติงานนอกสถานที่';
    case '/user6':
      return 'หน้าหลัก > ขออนุญาตปฏิบัติงานนอกสถานที่ให้คนอื่น';
    case '/user7':
      return 'หน้าหลัก > ดูรายการปฏิบัติงานนอกสถานที่';
    case '/user8':
      return 'หน้าหลัก > วันหยุด';
    case '/user9':
      return 'หน้าหลัก > วันหยุด > ปฏิทิน';
    case '/user10':
      return 'หน้าหลัก > ข้อมูลส่วนตัว';
    case '/user11':
      return 'หน้าหลัก > ข้อมูลส่วนตัว > แก้ไข';
    case '/user12':
      return 'หน้าหลัก > เปลี่ยนรหัสผ่าน';
    default:
      return 'หน้าหลัก';
  }
});
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

.btn-table {
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

.btn-table i {
  margin-right: 5px;
}

.calendar-header {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 15px;
  font-weight: bold;
  font-size: 1.2rem;
}

.month-btn {
  background: #f1f1f1;
  border: 1px solid #ccc;
  padding: 5px 10px;
  margin: 0 10px;
  cursor: pointer;
  border-radius: 5px;
}

.month-label {
  min-width: 150px;
  text-align: center;
}

.calendar-view {
  width: 100%;
}

.calendar-table {
  width: 100%;
  border-collapse: collapse;
}

.calendar-table th,
.calendar-table td {
  border: 1px solid #ddd;
  padding: 12px;
  height: 120px; 
  vertical-align: top;
  text-align: left;
}

.calendar-table th {
  background-color: #f2f2f2;
  font-weight: bold;
  text-align: center;
}

.calendar-table td {
  padding: 30px;
  vertical-align: top;
  border: 1px solid #ccc;
  min-width: 80px;
  height: 60px;
}

.calendar-table td.holiday {
  background-color: #ffe6e6;
}

.calendar-table td.today {
  border: 2px solid #007bff;
}

.date-text {
  font-weight: bold;
}

.holiday-name {
  color: red;
  font-size: 0.85rem;
  margin-top: 4px;
}
</style>
