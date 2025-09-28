<template>
    <TopBar > <template #breadcrumbs>
              <Breadcrumb  :model="items"/>

    </template></TopBar>

      <div class="content-container">
        <div class="header-with-button">
          <div class="header-with-icon">
            <i class="fas fa-calendar-alt"></i>
            <h2>วันหยุด/ปฏิทิน</h2>
          </div>
          <div class="button-group">
            <button type="button" class="btn-add-holiday" @click="goToAddHoliday">
              <i class="fas fa-plus"></i> เพิ่มวันหยุด
            </button>
            <button type="button" class="btn-add-room" @click="switchToTableView">
              <i class="fas fa-th"></i> สลับเป็นรูปแบบตาราง
            </button>
          </div>
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
            <div class="calendar-cell" 
                 v-for="(day, index) in calendarDays" 
                 :key="index" 
                 :class="{ 'holiday': day.holidayName, 'clickable': day.holidayName }" 
                 :title="day.holidayName"
                 @click="day.holidayId ? goToEditHoliday(day.holidayId) : null">
              <span v-if="!day.empty" class="day-number">{{ day.date }}</span>
              <div v-if="day.holidayName" class="holiday-name">{{ day.holidayName }}</div>
            </div>
          </div>
        </div>
      </div>
</template>

<script setup lang="ts">
import TopBar from '~/components/Topbar.vue'

import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

import Card from 'primevue/card'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'

import Breadcrumb from 'primevue/breadcrumb';

import type { MenuItem } from 'primevue/menuitem';

const items : MenuItem[] = [
  {
    label : 'วันหยุด',url : '/sehedule'
  },
  {
    label : 'ปฏิทิน',url : '/calendar'
  }
]
const router = useRouter();
const token = ref<string | null>(null);
const holidays = ref<any[]>([]);

const showProfileMenu = ref(false);
const toggleProfileMenu = () => {
  showProfileMenu.value = !showProfileMenu.value;
};

const goTo = (path: string) => {
  router.push(path);
};

const goToAdminPage = () => {
  router.push('/admin');
};

const goToAdmin2Page = () => {
  router.push('/admin2');
};

const goToAdmin10Page = () => {
  router.push('/admin10');
};

const goToAdmin11Page = () => {
  router.push('/admin11');
};

const goToAdmin12Page = () => {
  router.push('/admin12');
};

const goToAddHoliday = () => {
  router.push('/admin25');
};

const goToEditHoliday = (id: number) => {
  router.push(`/admin25?id=${id}`);
};

const switchToTableView = () => {
  router.push('/admin11');
};

const currentUser = ref<any>(null);

onMounted(async () => {
  if (typeof window !== "undefined") {
    token.value = localStorage.getItem("token");
  }

  if (!token.value) {
    router.push('/login');
    return;
  }

  axios.defaults.headers.common['Authorization'] = `Token ${token.value}`;

  try {
    const me = await axios.get('http://localhost:8000/api/users/me/');
    currentUser.value = me.data;

    if (currentUser.value.role !== 'admin') {
      router.push('/login');
      return;
    }
  } catch (err) {
    console.error(err);
    router.push('/login');
  }

  try {
    const res = await axios.get('http://localhost:8000/api/holiday/list/');
    holidays.value = res.data.map((h: any) => ({
      id: h.id,
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
    localStorage.removeItem("token");
  }
  delete axios.defaults.headers.common['Authorization'];
  router.push("/login");
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
      holidayId: holiday ? holiday.id : null,
      holidayName: holiday ? holiday.name : '',
      holidayType: holiday ? holiday.type : ''
    });
  }

  calendarDays.value = daysArray;
  currentMonthYear.value = `${firstDay.toLocaleString('th-TH', { month: 'long' })} ${firstDay.getFullYear() + 543}`;
}

onMounted(() => generateCalendar());
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
  background-color: #5b74e6;
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
  background-color: #454ba0;
}

.calendar-grid {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}

.calendar-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
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
  grid-template-columns: repeat(7, 1fr);
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

.button-group {
  display: flex;
  gap: 10px;
}

.btn-add-holiday {
  background-color: #28a745;
  color: white;
  padding: 8px 16px;
  font-size: 1em;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.btn-add-holiday:hover {
  background-color: #218838;
}

.calendar-cell.clickable {
  cursor: pointer;
}

.calendar-cell.clickable:hover {
  background-color: #e9ecef;
}
</style>