<template>
    <TopBar > <template #breadcrumbs>
              <Breadcrumb  :model="items"/>

    </template></TopBar>

      <div class="content-container">
        <div class="form-header">
          <h2>{{ isEditing ? 'แก้ไขวันหยุด' : 'เพิ่มวันหยุด' }}</h2>
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
              <input type="date" id="holiday-date" v-model="form.date" required placeholder="mm/dd/yyyy" />
              <div v-if="fieldErrors.date" class="error-message">{{ fieldErrors.date }}</div>
            </div>
            <div class="form-group">
              <label for="holiday-type">ประเภทวันหยุด *</label>
              <select id="holiday-type" v-model="form.type" required>
                <option value="">กรุณาเลือกประเภท</option>
                <option v-for="type in holidayTypes" :key="type.value" :value="type.value">
                  {{ type.label }}
                </option>
              </select>
              <div v-if="fieldErrors.type" class="error-message">{{ fieldErrors.type }}</div>
            </div>
          </div>

          <div class="form-actions">
            <button v-if="isEditing" type="button" class="btn-save" @click="submitForm" :disabled="isLoading">
              <span v-if="isLoading">กำลังบันทึก...</span>
              <span v-else>บันทึก</span>
            </button>
            <button v-if="isEditing" type="button" class="btn-delete" @click="deleteHoliday" :disabled="isLoading">
              <span v-if="isLoading">กำลังลบ...</span>
              <span v-else>ลบ</span>
            </button>
            <button v-if="!isEditing" type="button" class="btn-save" @click="submitForm" :disabled="isLoading">
              <span v-if="isLoading">กำลังเพิ่ม...</span>
              <span v-else>เพิ่ม</span>
            </button>
          </div>
        </form>
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
    label : 'วันหยุด',url : '/day-off/sehedule'
  },
  {
    label : 'เพิ่มวันหยุด',url : '/day-off/add-day-off'
  }
]

const router = useRouter();
const route = useRoute();
const token = ref<string | null>(null);
const showProfileMenu = ref(false);
const errorMessage = ref<string | null>(null);
const successMessage = ref<string | null>(null);
const fieldErrors = ref<{ [key: string]: string }>({});
const isLoading = ref(false);
const isEditing = ref(false);

const holidayTypes = ref([
  { value: 'public', label: 'วันหยุดราชการ' },
  { value: 'company', label: 'วันหยุดบริษัท' },
  { value: 'religious', label: 'วันหยุดทางศาสนา' },
  { value: 'other', label: 'อื่น' },
]);

const form = reactive({
  name: '',
  date: '',
  type: '',
});

const toggleProfileMenu = () => {
  showProfileMenu.value = !showProfileMenu.value;
};

const goTo = (path: string) => {
  router.push(path);
};

const cancelForm = () => {
  if (confirm('คุณต้องการยกเลิกหรือไม่?')) {
    resetForm();
    router.push('/admin/sehedule');
  }
};

const submitForm = async () => {
  if (isLoading.value) return;
  isLoading.value = true;
  errorMessage.value = null;
  successMessage.value = null;
  fieldErrors.value = {};

  if (!form.name.trim()) {
    fieldErrors.value.name = 'กรุณากรอกชื่อวันหยุด';
    isLoading.value = false;
    return;
  }
  if (!form.date) {
    fieldErrors.value.date = 'กรุณาเลือกวันที่';
    isLoading.value = false;
    return;
  }
  if (!form.type) {
    fieldErrors.value.type = 'กรุณาเลือกประเภทวันหยุด';
    isLoading.value = false;
    return;
  }
  const today = new Date().toISOString().split('T')[0];
  if (form.date < today) {
    fieldErrors.value.date = 'วันที่ต้องไม่เป็นวันในอดีต';
    isLoading.value = false;
    return;
  }

  try {
    const holidayId = route.query.id;
    const method = holidayId && isEditing.value ? axios.put : axios.post;
    const url = holidayId && isEditing.value
      ? `http://localhost:8000/api/holiday/${holidayId}/`
      : 'http://localhost:8000/api/holiday/';

    const response = await method(url, {
      name: form.name,
      date: form.date,
      holiday_type: form.type,
    });

    successMessage.value = isEditing.value ? 'แก้ไขวันหยุดเรียบร้อยแล้ว' : 'เพิ่มวันหยุดเรียบร้อยแล้ว';
    setTimeout(() => {
      router.push('admin/sehedule');
    }, 1000);
  } catch (error: any) {
    console.error('Full error response:', JSON.stringify(error.response?.data, null, 2));
    if (error.response?.status === 400) {
      const errors = error.response.data;
      if (errors.date && errors.date.includes('วันหยุดนี้มีอยู่แล้ว')) {
        fieldErrors.value.date = 'วันหยุดในวันที่เลือกมีอยู่แล้ว กรุณาเลือกวันที่อื่น';
      } else if (errors.holiday_type) {
        fieldErrors.value.type = 'ประเภทวันหยุดไม่ถูกต้อง กรุณาเลือกใหม่';
      } else {
        for (const [field, messages] of Object.entries(errors)) {
          fieldErrors.value[field] = Array.isArray(messages) ? messages[0] : messages;
        }
      }
    } else if (error.response?.status === 404) {
      errorMessage.value = 'ไม่พบวันหยุดที่ระบุ';
    } else {
      errorMessage.value = 'เกิดข้อผิดพลาดในการบันทึก กรุณาลองใหม่';
    }
    successMessage.value = null;
    console.error('Error processing holiday:', error);
  } finally {
    isLoading.value = false;
  }
};

const deleteHoliday = async () => {
  if (isLoading.value) return;
  if (!confirm('คุณแน่ใจหรือไม่ว่าต้องการลบวันหยุดนี้?')) return;

  isLoading.value = true;
  errorMessage.value = null;
  successMessage.value = null;

  try {
    const holidayId = route.query.id;
    if (!holidayId) {
      errorMessage.value = 'ไม่พบ ID วันหยุด';
      isLoading.value = false;
      return;
    }

    await axios.delete(`http://localhost:8000/api/holiday/${holidayId}/`, {
      headers: { Authorization: `Token ${token.value}` },
    });

    successMessage.value = 'ลบวันหยุดเรียบร้อยแล้ว';
    setTimeout(() => {
      router.push('admin/sehedule');
    }, 1000);
  } catch (error: any) {
    console.error('Error deleting holiday:', JSON.stringify(error.response?.data, null, 2));
    if (error.response?.status === 404) {
      errorMessage.value = 'ไม่พบวันหยุดที่ระบุ';
    } else {
      errorMessage.value = 'เกิดข้อผิดพลาดในการลบวันหยุด';
    }
  } finally {
    isLoading.value = false;
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
  isEditing.value = false;
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

    const holidayId = route.query.id;
    console.log('Holiday ID from query:', holidayId);
    if (holidayId) {
      isEditing.value = true;
      try {
        const response = await axios.get(`http://localhost:8000/api/holiday/${holidayId}/`);
        console.log('Holiday data:', response.data);
        Object.assign(form, {
          name: response.data.name,
          date: response.data.date,
          type: response.data.holiday_type,
        });
      } catch (error: any) {
        console.error('Error fetching holiday:', error);
        if (error.response?.status === 404) {
          errorMessage.value = 'ไม่พบวันหยุดที่ระบุ กรุณาตรวจสอบ ID';
        } else {
          errorMessage.value = 'ไม่สามารถดึงข้อมูลวันหยุดได้';
        }
      }
    }
  } catch (err) {
    console.error('Error fetching user:', err);
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

.btn-save {
  border: none;
  padding: 12px 30px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.2s;
  color: white;
  background-color: #4caf50;
}

.btn-save:hover {
  background-color: #45a049;
}

.btn-delete {
  border: none;
  padding: 12px 30px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.2s;
  color: white;
  background-color: #ff6b6b;
}

.btn-delete:hover {
  background-color: #e55a5a;
}
</style>