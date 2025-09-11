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
          <span><i class="fas fa-home"></i> หน้าหลัก > ดูข้อมูลส่วนตัว</span>
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
        <div class="header-with-icon">
          <i class="fas fa-user"></i>
          <h2>ดูข้อมูลส่วนตัวข้อมูลส่วนตัว</h2>
        </div>

        <div class="profile-layout">
          <div class="profile-info-section">
            <div class="form-row">
              <label>ชื่อภาษาไทย :</label>
              <input type="text" v-model="profile.nameTh" class="form-input" disabled>
            </div>
            <div class="form-row">
              <label>ชื่อภาษาอังกฤษ :</label>
              <input type="text" v-model="profile.nameEn" class="form-input" disabled>
            </div>
            <div class="form-row">
              <label>ตำแหน่ง :</label>
              <input type="text" v-model="profile.position" class="form-input" disabled>
            </div>
          </div>
          <div class="profile-image-section">
            <div class="profile-placeholder">
              Profile
            </div>
          </div>
        </div>

        <div class="data-boxes-container">
          <div class="data-box">
            <div class="box-title">ประเภทการจ้างงาน :</div>
            <div class="box-content">
              <span>วันที่เริ่มทำงาน : {{ profile.startDate }}</span>
              <span>วันเกิด : {{ profile.dob }}</span>
              <span>ที่อยู่ : {{ profile.address }}</span>
              <span>Email : {{ profile.email }}</span>
              <span>เบอร์โทรศัพท์ : {{ profile.phone }}</span>
            </div>
          </div>
          <div class="data-box">
            <div class="box-title">รหัสเครื่องสแกนลายนิ้วมือ :</div>
            <div class="box-content">
              <span>วันลากิจคงเหลือ : {{ profile.leave.personal }} วัน</span>
              <span>วันลาป่วยคงเหลือ : {{ profile.leave.sick }} วัน</span>
              <span>วันลาพักร้อนคงเหลือ : {{ profile.leave.vacation }} วัน</span>
              <span>วันลาอื่นๆคงเหลือ : {{ profile.leave.other }} วัน</span>
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

const showProfileMenu = ref(false)
const toggleProfileMenu = () => {
  showProfileMenu.value = !showProfileMenu.value
}

const goTo = (path: string) => {
  router.push(path);
};

const profile = reactive({
  nameTh: 'นายแอดมิน แอดมิน',
  nameEn: 'Admin Admin',
  position: 'Admin',
  labHead: 'นายหัวหน้า หัวหน้า',
  startDate: '01/01/2568',
  dob: '01/01/2540',
  address: 'เลขที่ 123 ถนนบางนา',
  email: 'admin.admin@mis.com',
  phone: '081-123-4567',
  leave: {
    personal: 5,
    sick: 30,
    vacation: 10,
    other: 0,
  }
});


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

.header-with-icon {
  display: flex;
  align-items: center;
  gap: 10px;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 20px;
}

.header-with-icon h2 {
  font-size: 24px;
  font-weight: bold;
  margin: 0;
}

.header-with-icon i {
  color: #f44336;
}

.profile-layout {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  align-items: flex-start;
}

.profile-info-section {
  flex: 2;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.form-row label {
  font-weight: bold;
  width: 150px;
  text-align: right;
  white-space: nowrap;
}

.form-input {
  flex-grow: 1;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1em;
  background-color: #f5f5f5;
}

.profile-image-section {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.profile-placeholder {
  width: 150px;
  height: 150px;
  background-color: #e0e0e0;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #888;
  font-weight: bold;
}

.data-boxes-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.data-box {
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
}

.box-title {
  font-weight: bold;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
  margin-bottom: 10px;
}

.box-content {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

@media (max-width: 768px) {
  .top-bar {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  .profile-layout {
    flex-direction: column;
  }
  .profile-info-section {
    order: 2;
  }
  .profile-image-section {
    order: 1;
  }
  .form-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
  .form-row label {
    text-align: left;
    width: 100%;
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