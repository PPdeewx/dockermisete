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
            <i class="fas fa-calendar-check"></i> ขออนุญาตปฏิบัติงานนอกสถานที่
          </router-link>
        </li>
        <li class="nav-item" :class="{ 'active': $route.path === '/user6' }">
          <router-link to="/user6" class="nav-link">
            <i class="fas fa-calendar-check"></i> ขออนุญาตปฏิบัติงานนอกสถานที่ให้คนอื่น
          </router-link>
        </li>
        <li class="nav-item" :class="{ 'active': $route.path === '/user7' }">
          <router-link to="/user7" class="nav-link">
            <i class="fas fa-calendar-times"></i> ดูรายการปฏิบัติงานนอกสถานที่
          </router-link>
        </li>
        <li class="nav-item" :class="{ 'active': $route.path === '/user8' }">
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
          <span class="username">Username ตำแหน่ง:</span>
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

      <div class="leave-form-container">
        <div class="form-header">
          <div class="header-left">
            <i class="fas fa-calendar-check icon-red"></i>
            <div>
              <h3>ระบบการขออนุญาตปฏิบัติงานนอกสถานที่ให้คนอื่น</h3>
            </div>
          </div>
          <button type="button" class="btn-cancel" @click="cancelForm"><i class="fas fa-times-circle"></i> ยกเลิก</button>
        </div>

        <div class="user-info-section">
          <span class="user-label">พนักงาน *:</span>
          <span class="user-name">นาย Username  usernamesss</span>
        </div>

        <form @submit.prevent="submitForm" class="leave-form">
          <div class="form-row">
            <div class="form-group full-width">
              <label>ผู้ร่วมปฏิบัติงาน (Optional):</label>
              <input type="text" v-model="form.coworkers" class="text-input" />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group-dates">
              <label>วันที่ *:</label>
              <input type="date" v-model="form.startDate" class="date-input" />
            </div>
            <div class="form-group-dates">
              <label>ถึงวันที่ *:</label>
              <input type="date" v-model="form.endDate" class="date-input" />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>ช่วงเวลา :</label>
              <div class="radio-group">
                <label><input type="radio" value="ครึ่งวันเช้า" v-model="form.period" /> ครึ่งวันเช้า</label>
                <label><input type="radio" value="ครึ่งวันบ่าย" v-model="form.period" /> ครึ่งวันบ่าย</label>
                <label><input type="radio" value="ทั้งวัน" v-model="form.period" /> ทั้งวัน</label>
              </div>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group full-width">
              <label>เหตุผล*:</label>
              <input type="text" v-model="form.reason" class="text-input" />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group full-width">
              <label>หัวหน้างาน *:</label>
              <select v-model="form.approver" class="select-input">
                <option disabled value="">เลือกหัวหน้างาน</option>
                <option v-for="person in approvers" :key="person.id" :value="person.name">
                  {{ person.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="form-buttons-bottom">
            <button type="submit" class="btn-submit">ขออนุมัติลา</button>
          </div>
        </form>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';

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

const router = useRouter();
const route = useRoute();

function goTo(path: string) {
  router.push(path);
}
function logout() {
  router.push('/login');
}

const form = ref({
  coworkers: '',
  startDate: '',
  endDate: '',
  period: 'ครึ่งวันเช้า',
  reason: '',
  approver: ''
});

const approvers = ref([
  { id: 1, name: 'หัวหน้า A' },
  { id: 2, name: 'หัวหน้า B' }
]);

const submitForm = () => {
  console.log('ส่งฟอร์ม:', form.value);
  alert('ส่งคำขอสำเร็จ!');
  router.push('/user7');
};

const cancelForm = () => {
  console.log('ยกเลิกฟอร์ม');
  router.push('/user');
};

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

.leave-form-container {
  background-color: #ffffff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-header {
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

.form-header h3 {
  margin: 0;
  font-size: 22px;
}

.note {
  font-size: 14px;
  color: #888;
  margin: 5px 0 0;
}

.btn-cancel {
  background: #f1f1f1;
  color: #e74c3c;
  padding: 8px 14px;
  border: 1px solid #e74c3c;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  font-weight: bold;
}

.btn-cancel i {
  margin-right: 5px;
}

.user-info-section {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.user-label {
  font-weight: bold;
  margin-right: 10px;
}

.user-name {
  color: #555;
}

.leave-form {
  padding: 0;
}

.form-row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 15px;
}

.form-group {
  flex: 1 1 45%;
  display: flex;
  flex-direction: column;
}

.form-group-dates {
  flex: 1 1 45%;
  display: flex;
  align-items: center;
  gap: 10px;
}

.form-group label {
  font-weight: bold;
  margin-bottom: 5px;
}

.radio-group {
  display: flex;
  gap: 20px;
}

.text-input,
.select-input,
.date-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 14px;
}

.date-input {
  flex: 1;
}

.form-group-dates label {
  flex-shrink: 0;
  font-weight: bold;
}

.form-group.full-width {
  flex: 1 1 100%;
}

.form-buttons-bottom {
  display: flex;
  justify-content: flex-end;
  margin-top: 30px;
}

.btn-submit {
  background: #4caf50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}
</style>