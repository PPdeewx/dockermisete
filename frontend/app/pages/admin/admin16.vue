<template>
    <TopBar > <template #breadcrumbs>
              <Breadcrumb  :model="items"/>

    </template></TopBar>
      
      <div class="dashboard-container">
        <div class="card-left">
          <div class="card">
            <div class="card-header">
              <i class="fas fa-list-alt icon-blue"></i>
              <h4>ประกาศล่าสุด</h4>
            </div>
            <div class="card-body-list">
              <div class="timeline-item" v-for="(announcement, index) in announcements" :key="index">
                <div class="timeline-left">
                  <span class="timeline-time">{{ announcement.time }}</span>
                </div>
                <div class="timeline-right">
                  <p class="timeline-title">{{ announcement.title }}</p>
                  <p class="timeline-subtitle">{{ announcement.subtitle }}</p>
                  <span class="timeline-date">{{ announcement.date }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="card-right">
          <div class="card">
            <div class="card-header">
              <i class="fas fa-user-clock icon-blue"></i>
              <h4>พนักงานปฏิบัติงานวันนี้</h4>
            </div>
            <div class="card-body-center">
              <div class="donut-chart-container">
                <div class="donut-chart" style="--p: 40; --c: #a54687; --b: 10px;">
                    <span class="donut-label">40</span>
                </div>
              </div>
              <p class="donut-sublabel">พธ. 13 ธ.ค. 2568</p>
            </div>
          </div>

          <div class="card">
            <div class="card-header">
              <i class="fas fa-exclamation-triangle icon-yellow"></i>
              <h4>สถิติการมาสายของท่านในปีนี้</h4>
            </div>
            <div class="card-body-center">
              <div class="alert-box">
                <i class="fas fa-exclamation-triangle"></i>
                <p>0 นาที / 0 บาท</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="table-card">
        <div class="card-header">
          <i class="fas fa-calendar-times icon-red"></i>
          <h4>คำนวณการลาและทำงานนอกสถานที่ของพนักงาน 15 วันต่อจากนี้</h4>
        </div>
        <div class="card-body">
          <div class="responsive-table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>วันที่</th>
                  <th>พนักงาน</th>
                  <th>ประเภท</th>
                  <th>ช่วงเวลา</th>
                  <th>สถานะ</th>
                  <th>เหตุผล</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in upcomingActivities" :key="index">
                  <td>{{ item.date }}</td>
                  <td>{{ item.employee }}</td>
                  <td>{{ item.type }}</td>
                  <td>{{ item.period }}</td>
                  <td>{{ item.status }}</td>
                  <td>{{ item.reason }}</td>
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
    label : 'หน้าหลัก',url : '/admin'
  },
]

const router = useRouter()
const token = ref<string | null>(null)
const currentUser = ref<any>(null)

const showProfileMenu = ref(false)
const toggleProfileMenu = () => {
  showProfileMenu.value = !showProfileMenu.value
}

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
    currentUser.value = me.data

    if (currentUser.value.role !== 'admin') {
      router.push('/login')
      return
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

const announcements = ref([
  {
    title: 'การใช้งานระบบเบื้องต้น',
    subtitle: 'การลา/ยื่นปฏิบัติงานนอกสถานที่ และตรวจสอบเวลาเข้าออกในแต่ละวัน',
    date: '26 Mar 2025',
    time: '08:30 AM'
  },
  {
    title: 'การใช้งานตัวอื่นๆ',
    subtitle: 'สามารถเข้าใช้งานได้ดังนี้: แจ้งย้ายที่อยู่, แจ้งการออกจากระบบ',
    date: '26 Mar 2025',
    time: '16:30 PM'
  },
  {
    title: 'รายงานปัญหาการใช้งานระบบ',
    subtitle: 'หากพบปัญหาการใช้งาน กรุณา Capture หน้าจอ พร้อมทั้ง URL แจ้งให้ทีมงานทราบ',
    date: '26 Mar 2025',
    time: '17:00 PM'
  },
])

const upcomingActivities = ref([
  {
    date: '2025-12-13',
    employee: 'Username',
    type: 'ลาป่วย',
    period: 'ทั้งวัน',
    status: 'รออนุมัติ',
    reason: 'ไม่สบาย'
  },
  {
    date: '2025-12-14',
    employee: 'Username',
    type: 'ลากิจ',
    period: 'ครึ่งวันเช้า',
    status: 'อนุมัติ',
    reason: 'ธุระส่วนตัว'
  },
  {
    date: '2025-12-15',
    employee: 'Username',
    type: 'ทำงานนอกสถานที่',
    period: 'ทั้งวัน',
    status: 'อนุมัติ',
    reason: 'ประชุมลูกค้า'
  }
])
</script>


<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;700&display=swap');

* {
  box-sizing: border-box;
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

.submenu {
  list-style: none;
  padding: 0;
  margin-left: 15px;
  display: none;
}

.nav-item.has-submenu.active .submenu {
  display: block;
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

/* Style for the dropdown menu */
.dropdown-menu {
  position: absolute;
  top: 100%; /* Position below the user-profile div */
  right: 0;
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  min-width: 200px;
  margin-top: 10px; /* Add some space between the user info and the dropdown */
  z-index: 1000; /* Ensure it's on top of other content */
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

.dashboard-container {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
}

.card-left {
    flex: 2;
}

.card-right {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.card {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
  margin-bottom: 15px;
  width: 100%;
}

.card-header h4 {
  margin: 0;
  font-size: 16px;
}

.icon-blue {
    color: #1890ff;
    font-size: 20px;
    margin-right: 10px;
}

.icon-yellow {
    color: #ffc107;
    font-size: 20px;
    margin-right: 10px;
}

.icon-red {
    color: #e74c3c;
    font-size: 20px;
    margin-right: 10px;
}

.card-body-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.timeline-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 20px;
}

.timeline-left {
  position: relative;
  width: 80px;
  padding-right: 10px;
  text-align: right;
  font-size: 12px;
  color: #888;
}

.timeline-right {
  flex-grow: 1;
  border-left: 2px solid #ccc;
  padding-left: 15px;
}

.timeline-item:not(:last-child) .timeline-right {
    padding-bottom: 15px;
}

.timeline-title {
  margin: 0;
  font-weight: bold;
}

.timeline-subtitle {
  margin: 5px 0;
  font-size: 14px;
  color: #555;
}

.timeline-date {
  font-size: 12px;
  color: #aaa;
}

.card-body-center {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    flex-grow: 1;
    width: 100%;
}

.donut-chart-container {
    position: relative;
    width: 120px;
    height: 120px;
    margin-bottom: 10px;
}

.donut-chart {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: radial-gradient(closest-side, white 79%, transparent 80% 100%),
                conic-gradient(var(--c) calc(var(--p) * 1%), #eee 0);
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}

.donut-label {
    position: absolute;
    font-size: 36px;
    font-weight: bold;
    color: #a54687;
}

.donut-sublabel {
    font-size: 12px;
    color: #888;
    margin-top: 5px;
}

.alert-box {
    background-color: #fff3cd;
    color: #856404;
    border: 1px solid #ffeeba;
    padding: 15px;
    border-radius: 5px;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.alert-box i {
    margin-right: 10px;
}

.alert-box p {
    margin: 0;
    font-weight: bold;
}

.table-card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
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