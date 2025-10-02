<template>
    <TopBar > <template #breadcrumbs>
              <Breadcrumb  :model="items"/>

    </template></TopBar>

      <div class="content-container">
        <div class="header-with-icon">
          <i class="fas fa-user-edit"></i>
          <h2>แก้ไขข้อมูลส่วนตัว</h2>
        </div>
        <p class="form-description">กรุณากรอกข้อมูลในช่องว่างที่มีเครื่องหมาย *</p>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        <div v-if="successMessage" class="success-message">{{ successMessage }}</div>

        <div class="edit-profile-form">
          <div class="form-column">
            <div class="form-row">
              <label>คำนำหน้าชื่อ <span class="required">*</span>:</label>
              <div class="form-input-container">
                <select v-model="form.prefix_th" class="form-select">
                  <option value="">กรุณาเลือก</option>
                  <option value="นาย">นาย</option>
                  <option value="นาง">นาง</option>
                  <option value="นางสาว">นางสาว</option>
                </select>
                <small class="inline-desc">เลือกคำนำหน้าชื่อ</small>
              </div>
            </div>
            <div class="form-row">
              <label>ชื่อภาษาไทย <span class="required">*</span>:</label>
              <div class="form-input-container">
                <input type="text" v-model="form.firstname_th" class="form-input" />
                <small class="inline-desc">กรอกชื่อภาษาไทย</small>
              </div>
            </div>
            <div class="form-row">
              <label>นามสกุลภาษาไทย <span class="required">*</span>:</label>
              <div class="form-input-container">
                <input type="text" v-model="form.lastname_th" class="form-input" />
                <small class="inline-desc">กรอกนามสกุลภาษาไทย</small>
              </div>
            </div>
            <div class="form-row">
              <label>ชื่อภาษาอังกฤษ:</label>
              <div class="form-input-container">
                <input type="text" v-model="form.firstname_en" class="form-input" />
                <small class="inline-desc">กรอกชื่อภาษาอังกฤษ (ถ้ามี)</small>
              </div>
            </div>
            <div class="form-row">
              <label>นามสกุลภาษาอังกฤษ:</label>
              <div class="form-input-container">
                <input type="text" v-model="form.lastname_en" class="form-input" />
                <small class="inline-desc">กรอกนามสกุลภาษาอังกฤษ (ถ้ามี)</small>
              </div>
            </div>
            <div class="form-row">
              <label>Email <span class="required">*</span>:</label>
              <input type="email" v-model="form.email" class="form-input" />
            </div>
            <div class="form-row">
              <label>เบอร์โทรศัพท์ <span class="required">*</span>:</label>
              <input type="tel" v-model="form.phone_number" class="form-input" />
            </div>
            <div class="form-row textarea-row">
              <label>ที่อยู่ติดต่อสะดวก:</label>
              <textarea v-model="form.address" class="form-textarea"></textarea>
            </div>
          </div>
          <div class="profile-image-section">
            <img :src="profileImageUrl" v-if="profileImageUrl" class="profile-image" />
            <div v-else class="profile-placeholder">
              Profile
            </div>
            <input type="file" id="chooseFile" class="file-input" @change="handleFileUpload" />
            <label for="chooseFile" class="btn-choose-file">Choose File</label>
          </div>
        </div>

        <div class="form-actions">
          <button class="btn-submit" @click="submitForm">บันทึกข้อมูล</button>
          <button class="btn-cancel" @click="goToAdmin28Page">ยกเลิก</button>
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
  {
    label : 'แก้ไขข้อมูลส่วนตัว',url : '/day-off'
  }
]

const router = useRouter();
const token = ref<string | null>(null);
const showProfileMenu = ref(false);
const currentUser = ref<any>(null);
const errorMessage = ref<string>('');
const successMessage = ref<string>('');
const profileImageUrl = ref<string | null>(null);

const form = reactive({
  prefix_th: '',
  firstname_th: '',
  lastname_th: '',
  firstname_en: '',
  lastname_en: '',
  email: '',
  phone_number: '',
  address: '',
  profile_image: null as File | null,
});

const toggleProfileMenu = () => {
  showProfileMenu.value = !showProfileMenu.value;
};

const goTo = (path: string) => {
  router.push(path);
};

const logout = () => {
  localStorage.removeItem("token");
  delete axios.defaults.headers.common['Authorization'];
  router.push("/login");
};

const handleFileUpload = (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (input.files && input.files.length > 0) {
    const file = input.files[0];
    form.profile_image = file;

    profileImageUrl.value = URL.createObjectURL(file);
  }
};

const submitForm = async () => {
  errorMessage.value = '';
  successMessage.value = '';

  if (!form.prefix_th || !form.firstname_th || !form.lastname_th || !form.email || !form.phone_number) {
    errorMessage.value = 'กรุณากรอกข้อมูลในช่องที่มีเครื่องหมาย * ให้ครบถ้วน';
    return;
  }

  const formData = new FormData();
  formData.append('prefix_th', form.prefix_th);
  formData.append('firstname_th', form.firstname_th);
  formData.append('lastname_th', form.lastname_th);
  formData.append('firstname_en', form.firstname_en || '');
  formData.append('lastname_en', form.lastname_en || '');
  formData.append('email', form.email);
  formData.append('phone_number', form.phone_number);
  formData.append('address', form.address || '');
  if (form.profile_image) {
    formData.append('profile_image', form.profile_image);
  }

  try {
    const response = await axios.patch('http://localhost:8000/api/users/profile/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    if (response.data.profile_image) {
      profileImageUrl.value = response.data.profile_image;
    }

    successMessage.value = 'บันทึกข้อมูลสำเร็จ';
    
    setTimeout(() => {
      router.push('/admin28');
    }, 2000);
  } catch (err: any) {
    console.error('Error updating profile:', err);
    if (err.response?.data) {
      const errors = err.response.data;
      const errorFields = Object.keys(errors).map(key => `${key}: ${errors[key].join(', ')}`).join('; ');
      errorMessage.value = `เกิดข้อผิดพลาด: ${errorFields}`;
    } else {
      errorMessage.value = 'เกิดข้อผิดพลาดในการบันทึกข้อมูล กรุณาลองใหม่';
    }
  }
};

const fetchUserProfile = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/users/me/');
    currentUser.value = response.data;
    if (response.data.profile_image) {
      profileImageUrl.value = response.data.profile_image;
    }
    if (currentUser.value.role !== 'admin') {
      router.push('/login');
      return;
    }

    form.prefix_th = response.data.prefix_th || '';
    form.firstname_th = response.data.firstname_th || '';
    form.lastname_th = response.data.lastname_th || '';
    form.firstname_en = response.data.firstname_en || '';
    form.lastname_en = response.data.lastname_en || '';
    form.email = response.data.email || '';
    form.phone_number = response.data.phone_number || '';
    form.address = response.data.address || '';

  } catch (err) {
    console.error('Error fetching user data:', err);
    router.push('/login');
  }
};

onMounted(async () => {
  token.value = localStorage.getItem("token");
  if (!token.value) {
    router.push('/login');
    return;
  }
  axios.defaults.headers.common['Authorization'] = `Token ${token.value}`;
  await fetchUserProfile();
});
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

.edit-profile-form {
  display: flex;
  gap: 40px;
  align-items: flex-start;
}

.form-column {
  flex: 2;
  display: flex;
  flex-direction: column;
  gap: 15px;
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

.required {
  color: #f44336;
}

.form-input-container {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-input, .form-select, .form-textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1em;
  min-width: 250px;
}

.form-textarea {
  min-height: 100px;
}

.inline-desc {
  font-size: 0.8em;
  color: #888;
}

.profile-image-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.profile-image {
  width: 150px;
  height: 150px;
  border-radius: 8px;
  object-fit: cover;
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

.file-input {
  display: none;
}

.btn-choose-file {
  background-color: #fff;
  color: #555;
  border: 1px solid #ccc;
  padding: 8px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: all 0.2s;
}

.btn-choose-file:hover {
  background-color: #f5f5f5;
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
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
  .top-bar, .header-with-button {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  .edit-profile-form {
    flex-direction: column;
  }
  .form-row, .textarea-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
  .form-row label {
    text-align: left;
    width: 100%;
  }
  .form-actions {
    justify-content: center;
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
</style>