<template>
    <TopBar > <template #breadcrumbs>
              <Breadcrumb  :model="items"/>

    </template></TopBar>

  <div class="dashboard-container">


      <div class="content-container">
        <div class="form-header">
          <h2></h2>
          <button class="btn-cancel" @click.prevent="cancelForm">
            <i class="fas fa-times"></i> ยกเลิก
          </button>
        </div>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
        <form @submit.prevent="submitForm">
          <div class="form-row">
            <div class="form-group">
              <label for="thai-name-prefix">คำนำหน้าชื่อ *</label>
              <select id="thai-name-prefix" v-model="form.thaiNamePrefix" required>
                <option value="">กรุณาเลือก</option>
                <option v-for="prefix in thaiNamePrefixOptions" :key="prefix" :value="prefix">
                  {{ prefix }}
                </option>
              </select>
              <div v-if="fieldErrors.prefix_th" class="error-message">{{ fieldErrors.prefix_th }}</div>
            </div>
            <div class="form-group">
              <label for="english-name-prefix">คำนำหน้าชื่อภาษาอังกฤษ</label>
              <select id="english-name-prefix" v-model="form.englishNamePrefix">
                <option value="">ไม่ระบุ</option>
                <option v-for="prefix in englishNamePrefixOptions" :key="prefix" :value="prefix">
                  {{ prefix }}
                </option>
              </select>
              <div v-if="fieldErrors.prefix_en" class="error-message">{{ fieldErrors.prefix_en }}</div>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="thai-name">ชื่อภาษาไทย *</label>
              <input type="text" id="thai-name" v-model="form.thaiName" required />
              <div v-if="fieldErrors.firstname_th" class="error-message">{{ fieldErrors.firstname_th }}</div>
            </div>
            <div class="form-group">
              <label for="english-name">ชื่อภาษาอังกฤษ</label>
              <input type="text" id="english-name" v-model="form.englishName" />
              <div v-if="fieldErrors.firstname_en" class="error-message">{{ fieldErrors.firstname_en }}</div>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="thai-surname">นามสกุลภาษาไทย *</label>
              <input type="text" id="thai-surname" v-model="form.thaiSurname" required />
              <div v-if="fieldErrors.lastname_th" class="error-message">{{ fieldErrors.lastname_th }}</div>
            </div>
            <div class="form-group">
              <label for="english-surname">นามสกุลภาษาอังกฤษ</label>
              <input type="text" id="english-surname" v-model="form.englishSurname" />
              <div v-if="fieldErrors.lastname_en" class="error-message">{{ fieldErrors.lastname_en }}</div>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="email">Email *</label>
              <input type="email" id="email" v-model="form.email" required />
              <div v-if="fieldErrors.email" class="error-message">{{ fieldErrors.email }}</div>
            </div>
            <div class="form-group">
              <label for="phone">เบอร์โทรศัพท์ *</label>
              <input type="tel" id="phone" v-model="form.phone" required />
              <div v-if="fieldErrors.phone_number" class="error-message">{{ fieldErrors.phone_number }}</div>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="external-department">หน่วยงานภายนอก</label>
              <input type="text" id="external-department" v-model="form.externalDepartment" />
              <div v-if="fieldErrors.external_department" class="error-message">{{ fieldErrors.external_department }}</div>
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-submit">บันทึกข้อมูล</button>
          </div>
        </form>
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
    label : 'บุคลากร',url : '/admin'
  },
  {
    label : 'เพิ่มบุคลากรภายนอก',url : '/admin'
  }
]


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

const goToAdmin10Page = () => {
  router.push('/admin10');
};

const goToAdmin11Page = () => {
  router.push('/admin11');
};

const goToAdmin12Page = () => {
  router.push('/admin12');
};

const thaiNamePrefixOptions = ref(['นาย', 'นาง', 'นางสาว']);
const englishNamePrefixOptions = ref(['Mr.', 'Mrs.', 'Ms.']);

const form = reactive({
  thaiNamePrefix: '',
  englishNamePrefix: '',
  thaiName: '',
  thaiSurname: '',
  englishName: '',
  englishSurname: '',
  email: '',
  phone: '',
  externalDepartment: '',
});

const submitForm = async () => {

  errorMessage.value = null;
  fieldErrors.value = {};

  if (!form.email.includes('@')) {
    errorMessage.value = 'กรุณากรอก email ให้ถูกต้อง';
    return;
  }
  if (!/^\d{10}$/.test(form.phone)) {
    errorMessage.value = 'กรุณากรอกเบอร์โทรศัพท์ 10 หลัก';
    return;
  }
  if (!form.thaiName || !form.thaiSurname || !form.thaiNamePrefix) {
    errorMessage.value = 'กรุณากรอกชื่อ, นามสกุล, และคำนำหน้าภาษาไทย';
    return;
  }

  try {
    const response = await axios.post('http://localhost:8000/api/users/create/external/', {
      username: form.email,
      prefix_th: form.thaiNamePrefix,
      firstname_th: form.thaiName,
      lastname_th: form.thaiSurname,
      prefix_en: form.englishNamePrefix || null,
      firstname_en: form.englishName || null,
      lastname_en: form.englishSurname || null,
      email: form.email,
      phone_number: form.phone,
      external_department: form.externalDepartment || null,
      groups: ['external'],
      role: 'employee',
      status: 'active',
    });
    successMessage.value = 'บันทึกบุคลากรภายนอกเรียบร้อยแล้ว';
    errorMessage.value = null;
    fieldErrors.value = {};
    resetForm();
    setTimeout(() => {
      router.push('/admin4');
    }, 2000);
  } catch (error: any) {
    console.error('Full error response:', JSON.stringify(error.response?.data, null, 2));
   
    if (error.response?.data) {
      const errors = error.response.data;
    
      for (const [field, messages] of Object.entries(errors)) {
        if (Array.isArray(messages)) {
          fieldErrors.value[field] = errorTranslations[messages[0]] || messages[0];
        } else {
          fieldErrors.value[field] = errorTranslations[messages] || messages;
        }
      }
      
      errorMessage.value =
        errorTranslations[errors?.email?.[0]] ||
        errorTranslations[errors?.username?.[0]] ||
        errorTranslations[errors?.groups?.[0]] ||
        errors?.non_field_errors?.[0] ||
        errors?.prefix_th?.[0] ||
        errors?.firstname_th?.[0] ||
        errors?.lastname_th?.[0] ||
        'เกิดข้อผิดพลาดในการบันทึก กรุณาลองใหม่';
    } else {
      errorMessage.value = 'เกิดข้อผิดพลาดในการเชื่อมต่อเซิร์ฟเวอร์';
    }
    successMessage.value = null;
    console.error('Error creating user:', error);
  }
};

const errorTranslations: { [key: string]: string } = {
  'A user with that email already exists.': 'อีเมลนี้มีอยู่ในระบบแล้ว',
  'A user with that username already exists.': 'ชื่อผู้ใช้นี้มีอยู่ในระบบแล้ว',
  'Invalid group name: external': 'ไม่พบกลุ่ม external ในระบบ',
  'This field is required.': 'กรุณากรอกข้อมูลในช่องนี้',
  'This field cannot be null.': 'ช่องนี้ต้องไม่ว่าง',
  'Object with name=external does not exist.': 'ไม่พบกลุ่ม external ในระบบ',
};

const cancelForm = () => {
  if (confirm('คุณต้องการยกเลิกการกรอกข้อมูลหรือไม่?')) {
    resetForm();
    router.push('/admin4');
  }
};

const resetForm = () => {
  Object.assign(form, {
    thaiNamePrefix: '',
    englishNamePrefix: '',
    thaiName: '',
    thaiSurname: '',
    englishName: '',
    englishSurname: '',
    email: '',
    phone: '',
    externalDepartment: '',
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

.error-message {
  color: red;
  margin-bottom: 10px;
}
.success-message {
  color: green;
  margin-bottom: 10px;
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

.form-group-container,
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

.radio-group {
  display: flex;
  gap: 15px;
  align-items: center;
  flex-wrap: wrap;
}

.radio-group label {
  font-weight: normal;
  display: flex;
  align-items: center;
  gap: 5px;
}

.small-text {
  font-size: 0.9em;
  color: #888;
  margin-bottom: 10px;
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