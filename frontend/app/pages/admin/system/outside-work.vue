<template>
    <TopBar > <template #breadcrumbs>
              <Breadcrumb  :model="items"/>

    </template></TopBar>

  <div class="dashboard-container">

      <div class="content-container">
        <div class="header-with-buttons">
          <h2><i class=""></i> </h2>
          <div class="header-buttons">
            <button class="btn-action btn-green" @click="requestOutsideWork">
              <i class="fas fa-plus"></i> ขออนุมัติปฏิบัติงานนอกสถานที่
            </button>
          </div>
        </div>

        <div class="user-summary-section">
          <div class="profile-card">
            <div class="profile-icon"><i class="fas fa-cog"></i></div>
            <div class="profile-info">
              <div class="username-section">
                <span>{{ currentUser?.username }}</span>
                <span>รหัส: {{ currentUser?.employee_code }}</span>
              </div>
            </div>
          </div>
        </div>

        <h3 class="history-header">ประวัติการปฏิบัติงานนอกสถานที่</h3>

        <div class="history-table-container">
          <table class="history-table">
            <thead>
              <tr>
                <th>เลขที่</th>
                <th>วันที่ลา</th>
                <th>พนักงาน</th>
                <th>ช่วงเวลา</th>
                <th>เหตุผล</th>
                <th>สถานะ</th>
                <th>ดำเนินการ</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(record, index) in outsideWorkHistory" :key="index">
                <td>{{ record.id }}</td>
                <td>{{ record.date }}</td>
                <td>{{ record.employee }}</td>
                <td>{{ record.time }}</td>
                <td>{{ record.reason }}</td>
                <td><span :class="`status-badge ${record.status}`">{{ record.status_th }}</span></td>
                <td>
                  <button class="btn-action btn-edit" v-if="record.can_edit">
                    <i class="fas fa-pen"></i>
                  </button>
                  <span v-else>-</span>
                </td>
              </tr>
              <tr v-if="outsideWorkHistory.length === 0">
                  <td colspan="7" class="no-data">ไม่มีข้อมูล</td>
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
    label : 'ระบบการปฏิบัติงาน',url : '/admin'
  },
  {
    label : 'ปฏิบัติงานนอกสถานที่',url : '/admin'
  }
]
const router = useRouter();
const token = ref<string | null>(null);

const showProfileMenu = ref(false)
const toggleProfileMenu = () => {
  showProfileMenu.value = !showProfileMenu.value
}

const goTo = (path: string) => {
  router.push(path);
};

const outsideWorkHistory = ref<any[]>([]);

const requestOutsideWork = () => {
  alert('เปิดหน้าขออนุมัติปฏิบัติงานนอกสถานที่');
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

    const res = await axios.get("http://localhost:8000/api/work-from-outside/requests/")
    outsideWorkHistory.value = res.data.map((item: any) => ({
      id: item.id,
      date: `${item.start_date} - ${item.end_date}`,
      employee: item.user?.full_name || item.user,
      time: item.time_period,
      reason: item.reason,
      status: item.status,
      status_th:
        item.status === "pending"
          ? "รออนุมัติ"
          : item.status === "approved"
          ? "อนุมัติ"
          : item.status === "rejected"
          ? "ไม่อนุมัติ"
          : item.status === "cancelled"
          ? "ยกเลิก"
          : "อื่น ๆ",
      can_edit: item.status === "pending",
      can_delete: item.status === "pending",
    }));
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

.btn-action {
  background-color: #52c41a;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-action:hover {
  background-color: #389e08;
}

.user-summary-section {
  display: flex;
  align-items: center;
  background-color: #f8f8f8;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  gap: 20px;
  flex-wrap: wrap;
}

.profile-card {
  display: flex;
  align-items: center;
  gap: 15px;
}

.profile-icon {
  font-size: 50px;
  color: #bbb;
}

.profile-info {
  display: flex;
  flex-direction: column;
}

.username-section {
  display: flex;
  flex-direction: column;
}

.username-section span:first-child {
  font-size: 1.2em;
  font-weight: bold;
}

.username-section span:last-child {
  font-size: 0.9em;
  color: #666;
}

.history-header {
  border-left: 5px solid #1890ff;
  padding-left: 10px;
  font-size: 1.2em;
  font-weight: bold;
  margin-bottom: 15px;
}

.history-table-container {
  overflow-x: auto;
}

.history-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.history-table th,
.history-table td {
  border: 1px solid #e0e0e0;
  padding: 12px 15px;
  text-align: left;
  white-space: nowrap;
}

.history-table th {
  background-color: #f2f2f2;
  font-weight: bold;
}

.history-table tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.9em;
  white-space: nowrap;
}

.status-badge.pending {
  background-color: #fffbe6;
  color: #faad14;
  border: 1px solid #ffe58f;
}

.status-badge.approved {
  background-color: #f6ffed;
  color: #52c41a;
  border: 1px solid #b7eb8f;
}

.status-badge.rejected {
  background-color: #fff1f0;
  color: #f5222d;
  border: 1px solid #ffccc7;
}

.btn-action {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1em;
  margin: 0 5px;
  padding: 5px;
}

.btn-action i {
  color: #888;
}

.btn-edit i {
  color: #ffc107;
}

.btn-delete i {
  color: #f44336;
}

.no-data {
  text-align: center;
  color: #888;
  font-style: italic;
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