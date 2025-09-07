<template>
  <div class="full-page-container">
    <div class="sidebar">
      <div class="sidebar-header">
        <span>MIS ETE</span>
      </div>
      <ul class="nav-menu">
        <li class="nav-item">
          <a href="#" class="nav-link"><i class="fas fa-home"></i> หน้าหลัก</a>
        </li>
        <li class="nav-item has-submenu active">
          <a href="#" class="nav-link"><i class="fas fa-users"></i> บุคลากร</a>
          <ul class="submenu active">
            <li><a href="#" class="submenu-link">พนักงานปัจจุบัน</a></li>
            <li><a href="#" class="submenu-link">พนักงานที่ลาออก</a></li>
            <li><a href="#" class="submenu-link">บุคลากรภายนอก</a></li>
            <li><a href="#" class="submenu-link">พนักงาน EDDP</a></li>
            <li><a href="#" class="submenu-link">เพิ่ม/แก้ไข/ลบ พนักงาน</a></li>
            <li><a href="#" class="submenu-link">เพิ่มบุคลากรภายนอก</a></li>
            <li><a href="#" class="submenu-link">เปลี่ยนสถานะพนักงาน</a></li>
            <li><a href="#" class="submenu-link active">กำหนดโควต้าลา(ทั้งหมด)</a></li>
          </ul>
        </li>
        <li class="nav-item"><a href="#" class="nav-link"><i class="fas fa-flask"></i> ห้องวิจัย</a></li>
        <li class="nav-item"><a href="#" class="nav-link"><i class="fas fa-calendar-alt"></i> วันหยุด</a></li>
        <li class="nav-item"><a href="#" class="nav-link"><i class="fas fa-cog"></i> ระบบการปฏิบัติงาน</a></li>
      </ul>
    </div>

    <div class="main-content">
      <div class="top-bar">
        <div class="breadcrumbs">
          <span><i class="fas fa-home"></i> หน้าหลัก > บุคลากร > กำหนดโควต้าลา(ทั้งหมด)</span>
        </div>
        <div class="user-profile-container">
          <div class="user-profile" @click="toggleProfileMenu">
            <i class="fas fa-bell"></i>
            <i class="fas fa-user-circle"></i>
            <span class="username">{{ currentUser?.username }} ตำแหน่ง: {{ currentUser?.role }}</span>
            <i :class="['fas', showProfileMenu ? 'fa-chevron-up' : 'fa-chevron-down']"></i>

            <div class="user-profile-menu" v-if="showProfileMenu">
              <button class="menu-item" @click.stop="goTo('/admin')">
                <i class="fas fa-user"></i>
                <span>ดูข้อมูลส่วนตัว</span>
              </button>
              <button class="menu-item" @click.stop="goTo('/admin')">
                <i class="fas fa-edit"></i>
                <span>แก้ไขข้อมูลส่วนตัว</span>
              </button>
              <button class="menu-item" @click.stop="goTo('/admin')">
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
        <div class="quota-controls">
          <div class="filter-group">
            <div class="filter-item">
              <label for="status-filter">สถานะพนักงาน</label>
              <select id="status-filter" v-model="filter.status">
                <option value="ทั้งหมด">ทั้งหมด</option>
                <option value="พนักงานปัจจุบัน">พนักงานปัจจุบัน</option>
                <option value="พนักงานที่ลาออก">พนักงานที่ลาออก</option>
              </select>
            </div>
            <div class="filter-item">
              <label for="room-filter">ห้องวิจัย</label>
              <select id="room-filter" v-model="filter.room">
                <option value="ทั้งหมด">ทั้งหมด</option>
                <option v-for="room in roomOptions" :key="room" :value="room">
                  {{ room }}
                </option>
              </select>
            </div>
            <div class="filter-item">
              <label for="search-name">ค้นหา</label>
              <input type="text" id="search-name" v-model="filter.search" placeholder="ค้นหาชื่อ" />
            </div>
          </div>
          <div class="quota-default">
            <span>Quota Default</span>
            <input type="number" v-model="quota.sick" placeholder="10.0" />
            <input type="number" v-model="quota.personal" placeholder="12.0" />
            <input type="number" v-model="quota.vacation" placeholder="30.0" />
            <button class="btn-default" @click="applyDefaultQuota">บันทึก Default</button>
          </div>
        </div>
        
        <div class="table-responsive">
          <table>
            <thead>
              <tr>
                <th>ลำดับที่</th>
                <th>ชื่อ-นามสกุล</th>
                <th>สถานะพนักงาน</th>
                <th>ห้องวิจัย</th>
                <th>ลาป่วย</th>
                <th>ลากิจ</th>
                <th>ลาพักร้อน</th>
                <th>อื่นๆ</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(employee, index) in filteredEmployees" :key="index">
                <td>{{ index + 1 }}</td>
                <td>{{ employee.name }}</td>
                <td>{{ employee.status }}</td>
                <td>{{ employee.room }}</td>
                <td><input type="number" v-model="employee.sickLeave" /></td>
                <td><input type="number" v-model="employee.personalLeave" /></td>
                <td><input type="number" v-model="employee.vacationLeave" /></td>
                <td><input type="number" v-model="employee.otherLeave" /></td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div class="form-actions">
          <button type="submit" class="btn-submit" @click="saveQuotaChanges">บันทึกข้อมูล</button>
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

const roomOptions = ref([
  'โครงการพัฒนาการศึกษาด้านพลังงาน[Energy Education Development Project: EEDP]',
  'ห้องวิจัยพลังงานทดแทนและอนุรักษ์พลังงาน[Renewable Energy and Energy Conservation Laboratory - REEC]',
  'ห้องวิจัยด้านวิศวกรรมและการบริหารจัดการการเปลี่ยนแปลงสภาพภูมิอากาศด้านพลังงาน[Climate Change Engineering and Management in Energy Sector Laboratory - CCEME]',
]);

const filter = reactive({
  status: 'ทั้งหมด',
  room: 'ทั้งหมด',
  search: '',
});

const quota = reactive({
  sick: 10.0,
  personal: 12.0,
  vacation: 30.0,
});

const employees = reactive([
  {
    name: 'สมชาย เจริญสุข',
    status: 'พนักงานปัจจุบัน',
    room: 'ห้องวิจัยด้านวิศวกรรมและการบริหารจัดการการเปลี่ยนแปลงสภาพภูมิอากาศด้านพลังงาน[Climate Change Engineering and Management in Energy Sector Laboratory - CCEME]',
    sickLeave: 10.0,
    personalLeave: 12.0,
    vacationLeave: 30.0,
    otherLeave: 0.0,
  },
  {
    name: 'สมหญิง รักดี',
    status: 'พนักงานปัจจุบัน',
    room: 'โครงการพัฒนาการศึกษาด้านพลังงาน[Energy Education Development Project: EEDP]',
    sickLeave: 10.0,
    personalLeave: 12.0,
    vacationLeave: 30.0,
    otherLeave: 0.0,
  },
  {
    name: 'เอกชัย มีชัย',
    status: 'พนักงานที่ลาออก',
    room: 'ห้องวิจัยพลังงานทดแทนและอนุรักษ์พลังงาน[Renewable Energy and Energy Conservation Laboratory - REEC]',
    sickLeave: 0.0,
    personalLeave: 0.0,
    vacationLeave: 0.0,
    otherLeave: 0.0,
  },
  {
    name: 'อรุณี สว่างจิต',
    status: 'พนักงานปัจจุบัน',
    room: 'โครงการพัฒนาการศึกษาด้านพลังงาน[Energy Education Development Project: EEDP]',
    sickLeave: 10.0,
    personalLeave: 12.0,
    vacationLeave: 30.0,
    otherLeave: 0.0,
  },
]);

const filteredEmployees = computed(() => {
  return employees.filter(employee => {
    const statusMatch = filter.status === 'ทั้งหมด' || employee.status === filter.status;
    const roomMatch = filter.room === 'ทั้งหมด' || employee.room === filter.room;
    const searchMatch = employee.name.toLowerCase().includes(filter.search.toLowerCase());
    return statusMatch && roomMatch && searchMatch;
  });
});

const applyDefaultQuota = () => {
  employees.forEach(employee => {
    employee.sickLeave = quota.sick;
    employee.personalLeave = quota.personal;
    employee.vacationLeave = quota.vacation;
  });
  alert('Default Quota ถูกบันทึกแล้ว!');
};

const saveQuotaChanges = () => {
  console.log('บันทึกข้อมูลโควต้าที่เปลี่ยนแปลง:', employees);
  alert('บันทึกข้อมูลเรียบร้อยแล้ว!');
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
  width: 300px;
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

.quota-controls {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 20px;
}

.filter-group {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.filter-item {
  display: flex;
  flex-direction: column;
}

.filter-item label {
  font-weight: bold;
  margin-bottom: 5px;
}

.filter-item select,
.filter-item input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.quota-default {
  display: flex;
  align-items: flex-end;
  gap: 10px;
}

.quota-default span {
  font-weight: bold;
  margin-right: 5px;
}

.quota-default input {
  width: 80px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center;
}

.btn-default {
  padding: 8px 15px;
  border-radius: 5px;
  background-color: #1890ff;
  color: white;
  border: none;
  cursor: pointer;
  white-space: nowrap;
}

.table-responsive {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

thead th {
  background-color: #f5f5f5;
  padding: 12px;
  text-align: left;
  border-bottom: 2px solid #ddd;
}

tbody td {
  padding: 12px;
  border-bottom: 1px solid #eee;
}

tbody tr:hover {
  background-color: #fafafa;
}

tbody input[type="number"] {
  width: 80px;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center;
}

.form-actions {
  margin-top: 30px;
  text-align: center;
}

.btn-submit {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.2s;
}

.btn-submit:hover {
  background-color: #45a049;
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