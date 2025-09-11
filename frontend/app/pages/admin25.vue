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
          <a href="#" class="nav-link" @click.prevent="goToAdmin2Page">
             <i class="fas fa-users"></i> บุคลากร</a>
        </li>
        <li class="nav-item">
          <a href="/admin10" class="nav-link" @click.prevent="goToAdmin10Page"><i class="fas fa-flask"></i> ห้องวิจัย</a>
        </li>
        <li class="nav-item active">
          <a href="#" class="nav-link"><i class="fas fa-calendar-alt"></i> วันหยุด</a>
          <ul class="submenu active">
            <li><a href="/admin11" class="submenu-link">วันหยุดประจำปี</a></li>
            <li><a href="/admin25" class="submenu-link active">เพิ่มวันหยุด</a></li>
          </ul>
        </li>
        <li class="nav-item">
          <a href="/admin12" class="nav-link" @click.prevent="goToAdmin12Page"><i class="fas fa-cog"></i> ระบบการปฏิบัติงาน</a>
        </li>
      </ul>
    </div>

    <div class="main-content">
      <div class="top-bar">
        <div class="breadcrumbs">
          <span><i class="fas fa-home"></i> หน้าหลัก > วันหยุด > เพิ่มวันหยุด</span>
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
        <div class="form-header">
          <h2>เพิ่มวันหยุด</h2>
          <button class="btn-cancel" @click.prevent="cancelForm">
            <i class="fas fa-times"></i> ยกเลิก
          </button>
        </div>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
        
        <form @submit.prevent="submitForm">
          <div class="form-row">
            <div class="form-group">
              <label for="holiday-name">ชื่อวันหยุด *</label>
              <input type="text" id="holiday-name" v-model="form.name" required />
              <div v-if="fieldErrors.name" class="error-message">{{ fieldErrors.name }}</div>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="holiday-date">วันที่ *</label>
              <input type="date" id="holiday-date" v-model="form.date" required />
              <div v-if="fieldErrors.date" class="error-message">{{ fieldErrors.date }}</div>
            </div>
            <div class="form-group">
              <label for="holiday-type">ประเภทวันหยุด *</label>
              <select id="holiday-type" v-model="form.type" required>
                <option value="">กรุณาเลือกประเภท</option>
                <option v-for="type in holidayTypes" :key="type" :value="type">
                  {{ type }}
                </option>
              </select>
              <div v-if="fieldErrors.type" class="error-message">{{ fieldErrors.type }}</div>
            </div>
          </div>

          <div class="form-actions">
            <button type="button" class="btn-save" @click="submitForm('save')">บันทึก</button>
            <button type="button" class="btn-save-add" @click="submitForm('save_add')">บันทึกและเพิ่ม</button>
            <button type="button" class="btn-save-edit" @click="submitForm('save_edit')">บันทึกและแก้ไข</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const token = ref<string | null>(null);
const showProfileMenu = ref(false);
const errorMessage = ref<string | null>(null);
const successMessage = ref<string | null>(null);
const fieldErrors = ref<{ [key: string]: string }>({});

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

const holidayTypes = ref(['วันหยุดราชการ','วันหยุดบริษัท','วันหยุดทางศาสนา','อื่น']);

const form = reactive({
  name: '',
  date: '',
  type: '',
});

const cancelForm = () => {
  if (confirm('คุณต้องการยกเลิกการเพิ่มวันหยุดหรือไม่?')) {
    resetForm();
    router.push('/admin11');
  }
};

const submitForm = async (action: 'save' | 'save_add' | 'save_edit') => {
  errorMessage.value = null;
  successMessage.value = null;
  fieldErrors.value = {};

  try {
    const response = await axios.post('http://localhost:8000/api/holidays/', {
      name: form.name,
      date: form.date,
      holiday_type: form.type,
    });

    successMessage.value = 'บันทึกวันหยุดเรียบร้อยแล้ว';
    
    if (action === 'save') {
      setTimeout(() => {
        router.push('/admin11');
      }, 1000);
    } else if (action === 'save_add') {
      resetForm();
    } else if (action === 'save_edit') {
      // Stay on the same page, no action needed other than showing success message
    }

  } catch (error: any) {
    console.error('Full error response:', JSON.stringify(error.response?.data, null, 2));
    if (error.response?.data) {
      const errors = error.response.data;
      if (typeof errors === 'object' && errors !== null) {
        for (const [field, messages] of Object.entries(errors)) {
          fieldErrors.value[field] = Array.isArray(messages) ? messages[0] : messages;
        }
      } else {
        errorMessage.value = 'เกิดข้อผิดพลาดในการบันทึก กรุณาลองใหม่';
      }
    } else {
      errorMessage.value = 'เกิดข้อผิดพลาดในการเชื่อมต่อเซิร์ฟเวอร์';
    }
    successMessage.value = null;
    console.error('Error creating holiday:', error);
  }
};

const resetForm = () => {
  Object.assign(form, {
    name: '',
    date: '',
    type: '',
  });
  errorMessage.value = null;
  fieldErrors.value = {};
};

const currentUser = ref<any>(null);

onMounted(async () => {
  if (typeof window !== 'undefined') {
    token.value = localStorage.getItem('token');
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
  } catch (err) {
    console.error(err);
    router.push('/login');
  }
});

function logout() {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('token');
  }
  delete axios.defaults.headers.common['Authorization'];
  router.push('/login');
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

.content-container {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 20px;
}

.form-header h2 {
  font-weight: bold;
  font-size: 24px;
}

.btn-cancel {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  border-radius: 5px;
  border: none;
  background-color: #ff6b6b;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-cancel:hover {
  background-color: #e55a5a;
}

.btn-cancel i {
  margin-right: 5px;
}

.form-row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  flex: 1 1 300px;
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: bold;
  margin-bottom: 5px;
}

.form-group input,
.form-group select {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 100%;
}

.error-message {
  color: red;
  margin-top: 5px;
  font-size: 12px;
}

.success-message {
  color: green;
  margin-bottom: 10px;
}

.form-actions {
  margin-top: 30px;
  display: flex;
  justify-content: center;
  gap: 15px;
}

.btn-save,
.btn-save-add,
.btn-save-edit {
  border: none;
  padding: 12px 30px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.2s;
  color: white;
}

.btn-save {
  background-color: #4caf50;
}

.btn-save:hover {
  background-color: #45a049;
}

.btn-save-add {
  background-color: #2196f3;
}

.btn-save-add:hover {
  background-color: #1a7bb9;
}

.btn-save-edit {
  background-color: #ffc107;
}

.btn-save-edit:hover {
  background-color: #e0ac00;
}
</style>