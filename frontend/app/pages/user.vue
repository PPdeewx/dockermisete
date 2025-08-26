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
            <i class="fas fa-user-edit"></i> ขออนุญาติปฏิบัติงานนอกสถานที่
          </router-link>
        </li>
        <li class="nav-item" :class="{ 'active': $route.path === '/user6' }">
          <router-link to="/user6" class="nav-link">
            <i class="fas fa-user-edit"></i> ขออนุญาติปฏิบัติงานนอกสถานที่ให้คนอื่น
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

    <main class="main-content">
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

      <div class="dashboard-container">
        <div class="card-left">
          <div class="card">
            <div class="card-header">
              <i class="fas fa-scroll icon-blue"></i>
              <h4>ประกาศล่าสุด</h4>
            </div>
            <div class="card-body">
              <div class="timeline">
                <div
                  class="timeline-item"
                  v-for="(announcement, index) in announcements"
                  :key="index"
                >
                  <div class="timeline-content">
                    <h5 class="timeline-title">{{ announcement.title }}</h5>
                    <p class="timeline-text">{{ announcement.text }}</p>
                    <span class="timeline-date">{{ announcement.date }}</span>
                  </div>
                  <div class="timeline-indicator">
                    <span class="timeline-time">{{ announcement.time }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="card-right">
          <div class="card">
            <div class="card-header">
              <i class="fas fa-users icon-blue"></i>
              <h4>พนักงานปฏิบัติงานวันนี้</h4>
            </div>
            <div class="card-body-center">
              <div class="donut-chart-container">
                <div
                  class="donut-chart"
                  :style="`--p: ${donutValue}; --c: #a54687; --b: 10px;`"
                >
                  <span class="donut-label">{{ donutValue }}</span>
                </div>
              </div>
              <p class="donut-sublabel">{{ todayLabel }}</p>
            </div>
          </div>

          <div class="card">
            <div class="card-header">
              <i class="fas fa-exclamation-triangle icon-yellow"></i>
              <h4>สถิติการลาสายของท่านในปีนี้</h4>
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
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios';

const router = useRouter()
const route = useRoute()

const user = ref<any>(null)
const token = ref<string | null>(null)

onMounted(async () => {
  const tokenStored = localStorage.getItem("token");
  if (!tokenStored) {
    router.push("/login");
    return;
  }
  axios.defaults.headers.common['Authorization'] = `Token ${tokenStored}`;

  try {
    const response = await axios.get("http://localhost:8000/api/users/me/");
    user.value = response.data;
    if (user.value.role !== "employee") {
      router.push("/login");
    }
  } catch (err) {
    console.error(err);
    router.push("/login");
  }
});

function logout() {
  localStorage.removeItem("token")
  delete axios.defaults.headers.common['Authorization']
  router.push("/login")
}

const announcements = ref([
  {
    title: 'การใช้งานระบบเบื้องต้น',
    text: 'กรุณาตรวจสอบคู่มือการใช้งานแบบฟอร์มการลาต่างๆ',
    date: '24 Mar 2025',
    time: '08:30 AM'
  },
  {
    title: 'การใช้งานตัวอื่นๆ',
    text: 'กรุณาตรวจสอบคู่มือและแบบฟอร์มการลา',
    date: '26 Mar 2025',
    time: '16:30 PM'
  },
  {
    title: 'รายงานปัญหาการใช้งานระบบ',
    text: 'หากมีปัญหาการใช้งานระบบ กรุณา Capture หน้าจอ พร้อมทั้ง URL แจ้งทางทีมงาน',
    date: '26 Mar 2025',
    time: '17:00 PM'
  }
])

const donutValue = ref(40)
const todayLabel = ref('พธ. 13 ธ.ค. 2568')

const showProfileMenu = ref(false)
function toggleProfileMenu() {
  showProfileMenu.value = !showProfileMenu.value
}

function handleBodyClick(event: MouseEvent) {
  if (showProfileMenu.value && !(event.target as HTMLElement).closest('.user-profile')) {
    showProfileMenu.value = false
  }
}
onMounted(() => document.addEventListener('click', handleBodyClick))
onBeforeUnmount(() => document.removeEventListener('click', handleBodyClick))

function goTo(path: string) {
  router.push(path)
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

.dashboard-container {
  display: flex;
  gap: 20px;
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

.timeline {
  position: relative;
  margin: 0;
  max-height: 260px;
  overflow-y: auto;
  padding-right: 6px;
}

.timeline-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 20px;
  position: relative;
}

.timeline-content {
  border-left: 2px solid #ccc;
  padding-left: 15px;
  margin-left: 45px;
}

.timeline-indicator {
  position: absolute;
  top: 0;
  left: 0;
  width: 60px;
  text-align: right;
  font-size: 12px;
  color: #888;
}

.timeline-title {
  margin: 0;
  font-weight: bold;
}

.timeline-text {
  margin: 5px 0;
  font-size: 14px;
  color: #555;
}

.timeline-date {
  font-size: 12px;
  color: #aaa;
}

.timeline-time {
  font-size: 12px;
  color: #888;
}

.card-body-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex-grow: 1;
  text-align: center;
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

@media (max-width: 992px) {
  .dashboard-container {
    flex-direction: column;
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
}
</style>