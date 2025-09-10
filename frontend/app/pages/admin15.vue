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
        <li class="nav-item has-submenu">
          <a href="#" class="nav-link"><i class="fas fa-users"></i> บุคลากร</a>
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
        <li class="nav-item">
          <a href="#" class="nav-link"><i class="fas fa-flask"></i> ห้องวิจัย</a>
        </li>
        <li class="nav-item"><a href="#" class="nav-link"><i class="fas fa-calendar-alt"></i> วันหยุด</a></li>
        <li class="nav-item active has-submenu">
          <a href="#" class="nav-link"><i class="fas fa-cog"></i> ระบบการปฏิบัติงาน</a>
          <ul class="submenu">
            <li><a href="#" class="submenu-link">ตรวจสอบเวลาทำงาน</a></li>
            <li><a href="#" class="submenu-link">เวลางานคนลาออก</a></li>
            <li><a href="#" class="submenu-link">รายการลาตัวเอง</a></li>
            <li><a href="#" class="submenu-link active">รายการลา ETE</a></li>
            <li><a href="#" class="submenu-link">ปฏิบัติงานนอกสถานที่</a></li>
            <li><a href="#" class="submenu-link">รายการอนุมัติการลาปฏิบัติงานนอกสถานที่</a></li>
            <li><a href="#" class="submenu-link">รายการอนุมัติการลา</a></li>
            <li><a href="#" class="submenu-link">ขออนุมัติลา</a></li>
            <li><a href="#" class="submenu-link">ขอลาให้คนอื่น</a></li>
            <li><a href="#" class="submenu-link">ขอปฏิบัติงานนอกสถานที่</a></li>
            <li><a href="#" class="submenu-link">ขอปฏิบัติงานนอกสถานที่ให้คนอื่น</a></li>
            <li><a href="#" class="submenu-link">Upload เวลางาน</a></li>
          </ul>
        </li>
      </ul>
    </div>

    <div class="main-content">
      <div class="top-bar">
        <div class="breadcrumbs">
          <span><i class="fas fa-home"></i> หน้าหลัก > รายการลา ETE</span>
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
          <h2><i class="fas fa-list-alt"></i> รายการลา ETE</h2>
          <button class="btn-export" @click="exportData">
            <i class="fas fa-file-export"></i> Export
          </button>
        </div>
        
        <div class="search-export-container">
          <div class="search-inputs">
            <div class="input-group">
              <label for="date-range">ช่วงวันที่</label>
              <input type="text" id="date-range" placeholder="ช่วงวันที่" class="form-input" v-model="dateRange">
            </div>
            <div class="input-group">
              <label for="room-select">ห้องวิจัย</label>
              <select id="room-select" class="form-select" v-model="selectedRoom">
                <option value="">ทั้งหมด</option>
                <option v-for="room in roomList" :key="room.id" :value="room.id">
                  {{ room.name }}
                </option>
              </select>
            </div>
            <div class="input-group">
              <label for="name-search">ค้นหาชื่อพนักงาน</label>
              <input type="text" id="name-search" placeholder="ค้นหาชื่อพนักงาน" class="form-input" v-model="searchName">
            </div>
            <button class="btn-search" @click="search">ค้นหา</button>
          </div>
        </div>
        
        <div class="leave-table-container">
          <table class="leave-table">
            <thead>
              <tr>
                <th>ชื่อ - นามสกุล</th>
                <th>ห้องวิจัย</th>
                <th>ประเภทการลา</th>
                <th>ชั่วโมง/วัน</th>
                <th>สถานะ</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(leave, index) in filteredLeaveList" :key="index">
                <td>{{ leave.name }}</td>
                <td>{{ roomNameById(leave.room) }}</td>
                <td>{{ leave.type }}</td>
                <td>{{ leave.duration }}</td>
                <td><span :class="`status-badge ${leave.status}`">{{ leave.status_th }}</span></td>
              </tr>
            </tbody>
          </table>
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
const dateRange = ref('');
const selectedRoom = ref('');
const searchName = ref('');

const showProfileMenu = ref(false)
const toggleProfileMenu = () => {
  showProfileMenu.value = !showProfileMenu.value
}

const roomList = reactive([
  { id: 'eedp', name: 'โครงการพัฒนาการศึกษาด้านพลังงาน' },
  { id: 'reec', name: 'ห้องวิจัยพลังงานทดแทนและอนุรักษ์พลังงาน' },
  { id: 'cceme', name: 'ห้องวิจัยด้านวิศวกรรมและการบริหารจัดการการเปลี่ยนแปลงสภาพภูมิอากาศด้านพลังงาน' },
]);

const leaveList = ref([
  {
    name: 'นาย ก. ไก่',
    room: 'reec',
    type: 'ลาป่วย',
    duration: '1 วัน',
    status: 'pending',
    status_th: 'รอดำเนินการ'
  },
  {
    name: 'นาง ข. ไข่',
    room: 'eedp',
    type: 'ลาพักร้อน',
    duration: '2 วัน',
    status: 'approved',
    status_th: 'อนุมัติแล้ว'
  },
  {
    name: 'นาย ค. ควาย',
    room: 'cceme',
    type: 'ลากิจ',
    duration: '0.5 วัน',
    status: 'rejected',
    status_th: 'ไม่อนุมัติ'
  },
]);

const filteredLeaveList = computed(() => {
  return leaveList.value.filter(leave => {
    const roomMatch = !selectedRoom.value || leave.room === selectedRoom.value;
    const nameMatch = leave.name.toLowerCase().includes(searchName.value.toLowerCase());
    return roomMatch && nameMatch;
  });
});

const roomNameById = (id: string) => {
  const room = roomList.find(r => r.id === id);
  return room ? room.name : 'ไม่ระบุ';
};

const search = () => {
  alert('ทำการค้นหาข้อมูล');
};

const exportData = () => {
  alert('ส่งออกข้อมูล');
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

.header-with-button h2 i {
  margin-right: 10px;
  color: #ff9800;
}

.btn-export {
  background-color: #1890ff;
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

.btn-export:hover {
  background-color: #096dd9;
}

.search-export-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f8f8f8;
  border-radius: 8px;
  border: 1px solid #eee;
  flex-wrap: wrap;
  gap: 15px;
}

.search-inputs {
  display: flex;
  align-items: flex-end;
  gap: 15px;
  flex-wrap: wrap;
}

.input-group {
  display: flex;
  flex-direction: column;
}

.input-group label {
  font-size: 0.9em;
  color: #666;
  margin-bottom: 5px;
}

.form-input,
.form-select {
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1em;
  min-width: 150px;
}

.btn-search {
  background-color: #1890ff;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
}

.btn-search:hover {
  background-color: #096dd9;
}

.leave-table-container {
  overflow-x: auto;
}

.leave-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.leave-table th,
.leave-table td {
  border: 1px solid #e0e0e0;
  padding: 12px 15px;
  text-align: left;
  white-space: nowrap;
}

.leave-table th {
  background-color: #f2f2f2;
  font-weight: bold;
}

.leave-table tbody tr:nth-child(even) {
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