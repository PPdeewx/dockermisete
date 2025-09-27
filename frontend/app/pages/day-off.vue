<template>
    <TopBar > <template #breadcrumbs>
              <Breadcrumb  :model="items"/>

    </template></TopBar>

  <div class="dashboard-container">


      <div class="content-container">
        <div class="header-with-button">
          <h2><i class="fas fa-calendar-alt"></i> วันหยุด/ตาราง</h2>
          <div class="button-group">
            <button class="btn-add-holiday" @click="goToAddHoliday">
              <i class="fas fa-plus"></i> เพิ่มวันหยุด
            </button>
            <button class="btn-add-room" @click="switchToTableView">
              <i class="fas fa-calendar-alt"></i> สลับเป็นรูปแบบปฏิทิน
            </button>
          </div>
        </div>
        
        <div class="holiday-table-container">
          <table class="holiday-table">
            <thead>
              <tr>
                <th>วันที่</th>
                <th>ชื่อวันหยุด</th>
                <th>ประเภทวันหยุด</th>
                <th>การจัดการ</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(holiday, index) in holidayList" :key="index">
                <td>{{ holiday.date }}</td>
                <td>{{ holiday.name }}</td>
                <td>{{ holiday.type }}</td>
                <td>
                  <button class="btn-edit" @click="goToEditHoliday(holiday.id)">
                    <i class="fas fa-edit"></i> แก้ไข
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
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
    label : 'วันหยุด',url : '/day-off'
  },
  {
    label : 'ตาราง',url : '/admin'
  }
]

const router = useRouter();
const token = ref<string | null>(null);

const viewMode = ref('table');

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

const holidayList = ref<any[]>([]);
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

    const res = await axios.get('http://localhost:8000/api/holiday/list/');
    holidayList.value = res.data.map((h: any) => ({
      id: h.id,
      date: h.date,
      name: h.name,
      type: h.holiday_type_display,
    }));
  } catch (err) {
    console.error(err);
    router.push('/login');
  }
});

function logout() {
  if (typeof window !== "undefined") {
    localStorage.removeItem("token");
  }
  delete axios.defaults.headers.common['Authorization'];
  router.push("/login");
}

const switchToTableView = () => {
  router.push('/admin27');
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

.holiday-table-container {
  overflow-x: auto;
}

.holiday-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.holiday-table th,
.holiday-table td {
  border: 1px solid #e0e0e0;
  padding: 12px 15px;
  text-align: left;
}

.holiday-table th {
  background-color: #f2f2f2;
  font-weight: bold;
}

.holiday-table tbody tr:nth-child(even) {
  background-color: #f9f9f9;
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

.btn-edit {
  background-color: #007bff;
  color: white;
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-edit:hover {
  background-color: #0056b3;
}
</style>