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
        </li>
        <li class="nav-item"><a href="/admin10" class="nav-link" @click.prevent="goToAdmin10Page"><i class="fas fa-flask"></i> ห้องวิจัย</a></li>
        <li class="nav-item"><a href="/admin11" class="nav-link" @click.prevent="goToAdmin11Page"><i class="fas fa-calendar-alt"></i> วันหยุด</a></li>
        <li class="nav-item active has-submenu">
          <a href="#" class="nav-link"><i class="fas fa-cog"></i> ระบบการปฏิบัติงาน</a>
          <ul class="submenu">
            <li><a href="/admin12" class="submenu-link">ตรวจสอบเวลาทำงาน</a></li>
            <li><a href="/admin13" class="submenu-link">เวลางานคนลาออก</a></li>
            <li><a href="/admin14" class="submenu-link">รายการลาตัวเอง</a></li>
            <li><a href="/admin15" class="submenu-link">รายการลา ETE</a></li>
            <li><a href="/admin16" class="submenu-link">ปฏิบัติงานนอกสถานที่</a></li>
            <li><a href="/admin17" class="submenu-link">รายการอนุมัติการลาปฏิบัติงานนอกสถานที่</a></li>
            <li><a href="/admin18" class="submenu-link">รายการอนุมัติการลา</a></li>
            <li><a href="/admin19" class="submenu-link">ขออนุมัติลา</a></li>
            <li><a href="#" class="submenu-link active">ขอลาให้คนอื่น</a></li>
            <li><a href="/admin21" class="submenu-link">ขอปฏิบัติงานนอกสถานที่</a></li>
            <li><a href="/admin22" class="submenu-link">ขอปฏิบัติงานนอกสถานที่ให้คนอื่น</a></li>
            <li><a href="/admin23" class="submenu-link">Upload เวลางาน</a></li>
          </ul>
        </li>
      </ul>
    </div>

    <div class="main-content">
      <div class="top-bar">
        <div class="breadcrumbs">
          <span><i class="fas fa-home"></i> หน้าหลัก > ขอลาให้คนอื่น</span>
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
        <div class="header-with-buttons">
          <h2><i class="fas fa-calendar-alt"></i> ระบบการยื่นใบลาแทนคนอื่น</h2>
          <button class="btn-cancel" @click="goToAdminPage">
            ยกเลิก
          </button>
        </div>

        <div class="form-section">
          <form @submit.prevent="submitForm">
            <div class="form-grid">
              <div class="form-group full-width">
                <label for="submitter-name">พนักงานผู้ยื่นลา <span class="required">*</span></label>
                <div class="read-only-text">นาย admin usermesss</div>
              </div>

              <div class="form-group full-width">
                <label for="employee-name">พนักงานผู้ลา <span class="required">*</span></label>
                <select id="employee-name" v-model="leaveForm.employee" class="form-select">
                  <option value="">เลือกพนักงานผู้ลา</option>
                  <option v-for="employee in employeeList" :key="employee.id" :value="employee.id">
                    {{ employee.name }}
                  </option>
                </select>
              </div>

              <div class="form-group full-width">
                <label>ประเภทการลา <span class="required">*</span></label>
                <div class="radio-group">
                  <label><input type="radio" v-model="leaveForm.leaveType" value="ลาป่วย"> ลาป่วย</label>
                  <label><input type="radio" v-model="leaveForm.leaveType" value="ลากิจ"> ลากิจ</label>
                  <label><input type="radio" v-model="leaveForm.leaveType" value="ลาพักร้อน"> ลาพักร้อน</label>
                </div>
              </div>

              <div class="form-group">
                <label for="startDate">ตั้งแต่วันที่ <span class="required">*</span></label>
                <input type="date" id="startDate" v-model="leaveForm.startDate" class="form-input">
              </div>

              <div class="form-group">
                <label for="endDate">ถึงวันที่ <span class="required">*</span></label>
                <input type="date" id="endDate" v-model="leaveForm.endDate" class="form-input">
              </div>
              
              <div class="form-group full-width">
                <label>ช่วงเวลา <span class="required">*</span></label>
                <div class="radio-group">
                  <label><input type="radio" v-model="leaveForm.timePeriod" value="ครึ่งวันเช้า"> ครึ่งวันเช้า</label>
                  <label><input type="radio" v-model="leaveForm.timePeriod" value="ครึ่งวันบ่าย"> ครึ่งวันบ่าย</label>
                  <label><input type="radio" v-model="leaveForm.timePeriod" value="ทั้งวัน"> ทั้งวัน</label>
                </div>
              </div>

              <div class="form-group full-width">
                <label for="reason">เหตุผลการลา <span class="required">*</span></label>
                <textarea id="reason" v-model="leaveForm.reason" class="form-textarea" rows="3"></textarea>
              </div>

              <div class="form-group full-width">
                <label for="substitute">ผู้ปฏิบัติงานแทน</label>
                <select id="substitute" v-model="leaveForm.substitute" class="form-select">
                  <option value="">เลือกผู้ปฏิบัติงานแทน</option>
                  <option v-for="substitute in substituteList" :key="substitute.id" :value="substitute.id">
                    {{ substitute.name }}
                  </option>
                </select>
              </div>
            </div>
            
            <div class="form-actions">
              <button type="button" class="btn-submit" @click="goToAdmin14Page">
                ขอยื่นลา
              </button>
            </div>
          </form>
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

const showProfileMenu = ref(false)
const toggleProfileMenu = () => {
  showProfileMenu.value = !showProfileMenu.value
}

const goTo = (path: string) => {
  router.push(path);
};

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

const goToAdmin14Page = () => {
  router.push('/admin14');
};

const leaveForm = reactive({
  submitter: 'นาย admin usermesss',
  employee: '',
  leaveType: '',
  startDate: '',
  endDate: '',
  timePeriod: 'ทั้งวัน',
  reason: '',
  approver: '',
  substitute: '',
});

const employeeList = ref([
  { id: 1, name: 'นาย ก. ไก่' },
  { id: 2, name: 'นาง ข. ไข่' },
  { id: 3, name: 'นาย ค. ควาย' },
]);

const approverList = ref([
  { id: 10, name: 'นาย A หัวหน้าห้องวิจัย' },
  { id: 20, name: 'นางสาว B ผู้จัดการ' },
]);

const substituteList = ref([
  { id: 101, name: 'นาย C พนักงาน' },
  { id: 102, name: 'นาง D พนักงาน' },
]);

const submitForm = () => {
  alert('ทำการส่งแบบฟอร์มขออนุมัติการลาแทนคนอื่น');
  console.log('Form data:', leaveForm);
};

const cancelForm = () => {
  alert('ยกเลิกการยื่นใบลา');
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

.btn-cancel {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
}

.btn-cancel:hover {
  background-color: #d32f2f;
}

.form-section {
  padding: 10px 0;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  font-weight: bold;
  margin-bottom: 5px;
  display: flex;
  align-items: center;
}

.form-group label .required {
  color: red;
  margin-left: 4px;
}

.read-only-text {
  padding: 10px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #f5f5f5;
  color: #555;
}

.radio-group {
  display: flex;
  gap: 20px;
  align-items: center;
  flex-wrap: wrap;
}

.radio-group label {
  font-weight: normal;
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
}

.form-input,
.form-select,
.form-textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1em;
}

.form-input[type="date"] {
  width: auto;
}

.form-textarea {
  resize: vertical;
}

.form-actions {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

.btn-submit {
  background-color: #52c41a;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.2s;
}

.btn-submit:hover {
  background-color: #389e08;
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
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