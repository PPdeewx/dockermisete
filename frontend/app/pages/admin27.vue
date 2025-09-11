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
        <li class="nav-item"><a href="/admin10" class="nav-link" @click.prevent="goToAdmin10Page"><i class="fas fa-flask"></i> ห้องวิจัย</a></li>
        <li class="nav-item"><a href="/admin11" class="nav-link" @click.prevent="goToAdmin11Page"><i class="fas fa-calendar-alt"></i> วันหยุด</a></li>
        <li class="nav-item"><a href="/admin12" class="nav-link" @click.prevent="goToAdmin12Page"><i class="fas fa-cog"></i> ระบบการปฏิบัติงาน</a></li>
      </ul>
    </div>

    <div class="main-content">
      <div class="top-bar">
        <div class="breadcrumbs">
          <span><i class="fas fa-home"></i> หน้าหลัก > วันหยุด/ปฏิทิน</span>
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
          <div class="header-with-icon">
            <i class="fas fa-calendar-alt"></i>
            <h2>วันหยุด/ปฏิทิน</h2>
          </div>
          <button type="button" class="btn-add-room" @click="switchToTableView">
            <i class="fas fa-th"></i> สลับเป็นรูปแบบตาราง
          </button>
        </div>

        <div class="calendar-grid">
          <div class="calendar-nav">
            <button @click="prevMonth">&lt;</button>
            <span class="calendar-month">{{ currentMonthYear }}</span>
            <button @click="nextMonth">&gt;</button>
          </div>
          <div class="calendar-header">
            <div class="day-name" v-for="day in ['อาทิตย์','จันทร์','อังคาร','พุธ','พฤหัสบดี','ศุกร์','เสาร์']" :key="day">{{ day }}</div>
          </div>
          <div class="calendar-body">
            <div class="calendar-cell empty" v-for="(day, index) in calendarDays" :key="index" :class="{ 'holiday': day.holidayName }" :title="day.holidayName">
              <span v-if="!day.empty" class="day-number">{{ day.date }}</span>
              <div v-if="day.holidayName" class="holiday-name">{{ day.holidayName }}</div>
            </div>
          </div>
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
const holidays = ref<any[]>([]);

const showProfileMenu = ref(false)
const toggleProfileMenu = () => {
  showProfileMenu.value = !showProfileMenu.value
}

const goTo = (path: string) => {
  router.push(path);
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

  try {
    const res = await axios.get('http://localhost:8000/api/holiday/list/');
    holidays.value = res.data.map((h: any) => ({
      date: new Date(h.date),
      name: h.name,
      type: h.holiday_type_display,
    }));
  } catch (err) {
    console.error(err);
  }
});

function logout() {
  if (typeof window !== "undefined") {
    localStorage.removeItem("token")
  }
  delete axios.defaults.headers.common['Authorization']
  router.push("/login")
}

const calendarDays = ref<any[]>([]);
const currentMonthOffset = ref(0);
const currentMonthYear = ref('');

const prevMonth = () => {
  currentMonthOffset.value--;
  generateCalendar(currentMonthOffset.value);
};

const nextMonth = () => {
  currentMonthOffset.value++;
  generateCalendar(currentMonthOffset.value);
};

function generateCalendar(offset = 0) {
  const today = new Date();
  const year = today.getFullYear();
  const month = today.getMonth() + offset;
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);

  const daysArray: any[] = [];

  const emptyCells = firstDay.getDay();
  for (let i = 0; i < emptyCells; i++) {
    daysArray.push({ empty: true });
  }

  for (let day = 1; day <= lastDay.getDate(); day++) {
    const fullDate = new Date(year, month, day);
    const holiday = holidays.value.find(h => h.date.toDateString() === fullDate.toDateString());
    daysArray.push({
      date: day,
      fullDate,
      holidayName: holiday ? holiday.name : '',
      holidayType: holiday ? holiday.type : ''
    });
  }

  calendarDays.value = daysArray;
  currentMonthYear.value = `${firstDay.toLocaleString('th-TH', { month: 'long' })} ${firstDay.getFullYear() + 543}`;
}

onMounted(() => generateCalendar());

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

const goToAdmin12Page = () => {
  window.location.href = '/admin12';
};

const switchToTableView = () => {
  window.location.href = '/admin11';
};

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

.header-with-button {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 20px;
}

.header-with-icon {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-with-icon h2 {
  font-size: 24px;
  font-weight: bold;
  margin: 0;
}

.header-with-icon i {
  color: #52c41a;
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

.calendar-grid {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}

.calendar-header {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  background-color: #f5f5f5;
  border-bottom: 1px solid #ddd;
}

.day-name {
  padding: 15px;
  text-align: center;
  font-weight: bold;
}

.calendar-body {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
}

.calendar-cell {
  min-height: 100px;
  border: 1px solid #eee;
  position: relative;
  padding: 10px;
}

.day-number {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 1.2em;
  font-weight: bold;
  color: #888;
}

@media (max-width: 768px) {
  .top-bar, .header-with-button {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }

  .calendar-header, .calendar-body {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
  }
}

.calendar-cell.holiday {
  background-color: #fff1f0;
  color: #cf1322;
}
.holiday-name {
  bottom: 5px;
  left: 5px;
  font-size: 1.5em;
  font-weight: bold;
}

.calendar-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.calendar-nav button {
  padding: 5px 10px;
  font-size: 1em;
  cursor: pointer;
}

.calendar-nav .calendar-month {
  font-weight: bold;
  font-size: 1.1em;
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