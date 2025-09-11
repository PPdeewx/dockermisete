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
          <a href="/admin2" class="nav-link" @click.prevent="goToAdmin2Page">
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
          <span><i class="fas fa-home"></i> หน้าหลัก > เปลี่ยนรหัสผ่าน</span>
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
          <i class="fas fa-lock"></i>
          <h2>เปลี่ยนรหัสผ่าน</h2>
        </div>
        <p class="form-description">กรุณากรอกข้อมูลให้ครบถ้วนและถูกต้อง</p>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        <div v-if="successMessage" class="success-message">{{ successMessage }}</div>

        <div class="change-password-form">
          <form @submit.prevent="submitForm">
            <div class="form-row">
              <label>รหัสผ่านเดิม <span class="required">*</span>:</label>
              <input type="password" v-model="form.currentPassword" class="form-input" placeholder="กรอกรหัสผ่านเดิม" />
            </div>
            <div class="form-row">
              <label>รหัสผ่านใหม่ <span class="required">*</span>:</label>
              <input type="password" v-model="form.newPassword" class="form-input" placeholder="กรอกรหัสผ่านใหม่" />
            </div>
            <div class="form-row">
              <label>ยืนยันรหัสผ่านใหม่ <span class="required">*</span>:</label>
              <input type="password" v-model="form.confirmPassword" class="form-input" placeholder="ยืนยันรหัสผ่านใหม่อีกครั้ง" />
            </div>
            <div class="form-actions">
              <button type="submit" class="btn-submit">บันทึกข้อมูล</button>
              <button type="button" class="btn-cancel" @click="cancelForm">ยกเลิก</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const token = ref<string | null>(null);
const currentUser = ref<any>(null);
const showProfileMenu = ref(false);
const errorMessage = ref<string>('');
const successMessage = ref<string>('');

const form = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
});

const toggleProfileMenu = () => {
  showProfileMenu.value = !showProfileMenu.value;
};

const handleBodyClick = (event: MouseEvent) => {
  if (showProfileMenu.value && !(event.target as HTMLElement).closest('.user-profile')) {
    showProfileMenu.value = false;
  }
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

const logout = () => {
  localStorage.removeItem("token");
  delete axios.defaults.headers.common['Authorization'];
  router.push("/login");
};

const submitForm = async () => {
  errorMessage.value = '';
  successMessage.value = '';

  if (!form.value.currentPassword || !form.value.newPassword || !form.value.confirmPassword) {
    errorMessage.value = 'กรุณากรอกข้อมูลให้ครบถ้วน';
    return;
  }

  if (form.value.newPassword !== form.value.confirmPassword) {
    errorMessage.value = 'รหัสผ่านใหม่และยืนยันรหัสผ่านไม่ตรงกัน';
    return;
  }

  try {
    const response = await axios.post(
      'http://localhost:8000/api/users/change-password/',
      {
        currentPassword: form.value.currentPassword,
        newPassword: form.value.newPassword,
        confirmPassword: form.value.confirmPassword,
      }
    );

    successMessage.value = response.data.message || 'เปลี่ยนรหัสผ่านสำเร็จ';
    form.value.currentPassword = '';
    form.value.newPassword = '';
    form.value.confirmPassword = '';
    setTimeout(() => {
      router.push('/admin28');
    }, 2000);
  } catch (error: any) {
    console.error('Error changing password:', error);
    if (error.response?.data) {
      const errors = error.response.data;
      const errorFields = Object.keys(errors).map(key => `${key}: ${errors[key].join(', ')}`).join('; ');
      errorMessage.value = `เกิดข้อผิดพลาด: ${errorFields}`;
    } else {
      errorMessage.value = 'เกิดข้อผิดพลาดในการเปลี่ยนรหัสผ่าน กรุณาลองใหม่';
    }
  }
};

const cancelForm = () => {
  form.value.currentPassword = '';
  form.value.newPassword = '';
  form.value.confirmPassword = '';
  router.push('/admin28');
};

onMounted(async () => {
  token.value = localStorage.getItem("token");

  if (!token.value) {
    router.push('/login');
    return;
  }

  axios.defaults.headers.common['Authorization'] = `Token ${token.value}`;

  try {
    const response = await axios.get('http://localhost:8000/api/users/me/');
    currentUser.value = response.data;

    if (currentUser.value.role !== 'admin') {
      router.push('/login');
      return;
    }

    console.log('User data:', currentUser.value);
  } catch (err) {
    console.error('Error fetching user data:', err);
    router.push('/login');
  }

  document.addEventListener('click', handleBodyClick);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleBodyClick);
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
  margin-bottom: 10px;
}

.header-with-icon h2 {
  font-size: 24px;
  font-weight: bold;
  margin: 0;
}

.header-with-icon i {
  color: #52c41a;
}

.form-description {
  color: #888;
  margin-bottom: 20px;
}

.change-password-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 600px;
  margin: 0 auto;
}

.form-row {
  display: flex;
  align-items: center;
  gap: 20px;
}

.form-row label {
  min-width: 150px;
  font-weight: bold;
  text-align: right;
  white-space: nowrap;
}

.form-input {
  flex-grow: 1;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1em;
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-top: 30px;
}

.btn-submit {
  background-color: #52c41a;
  color: white;
  border: none;
  padding: 10px 25px;
  border-radius: 5px;
  cursor: pointer;
}

.btn-cancel {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 10px 25px;
  border-radius: 5px;
  cursor: pointer;
}

@media (max-width: 768px) {
  .top-bar {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
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

.error-message {
  color: red;
  margin-bottom: 1rem;
}
.success-message {
  color: green;
  margin-bottom: 1rem;
}
.form-row {
  margin-bottom: 1rem;
}
.form-input {
  width: 100%;
  padding: 0.5rem;
}
.btn-submit, .btn-cancel {
  padding: 0.5rem 1rem;
  margin-right: 1rem;
}
</style>