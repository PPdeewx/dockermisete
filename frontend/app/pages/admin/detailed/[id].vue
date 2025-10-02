<template>
  <div class="full-page-container">
    

    <div class="main-content">
      <TopBar > <template #breadcrumbs>
              <Breadcrumb  :model="items"/>

      </template></TopBar>

      <div class="content-container">
        <div class="header-with-buttons">
          <h2><i class="fas fa-user-circle"></i> ข้อมูลพนักงานอย่างละเอียด</h2>
        </div>

        <div v-if="loading" class="loading">กำลังโหลด...</div>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        <div v-if="employee" class="form-section">
          <div class="form-grid">
            <div class="form-group">
              <label>ชื่อภาษาไทย :</label>
              <span>{{ employee.prefix_th }} {{ employee.firstname_th }} {{ employee.lastname_th }}</span>
            </div>
            <div class="form-group">
              <label>ชื่อภาษาอังกฤษ :</label>
              <span>{{ employee.firstname_en || '-' }} {{ employee.lastname_en || '-' }}</span>
            </div>
            <div class="form-group">
              <label>ตำแหน่ง :</label>
              <span>{{ employee.groupName || employee.groups?.[0]?.name || '-' }}</span>
            </div>
            <div class="form-group">
              <label>ห้องวิจัย :</label>
              <span>{{ employee.department?.name_th || '-' }}</span>
            </div>
          </div>

          <div class="form-grid-columns-2">
            <div class="form-box">
              <label class="box-title">ประเภทการจ้างงาน :</label>
              <div class="form-group">
                <label>ประเภทการจ้างงาน :</label>
                <span>{{ employee.employment_type || '-' }}</span>
              </div>
              <div class="form-group">
                <label>วันที่รับเข้าทำงาน :</label>
                <span>{{ employee.start_date || '-' }}</span>
              </div>
              <div class="form-group">
                <label>วันเกิด :</label>
                <span>{{ employee.dob || '-' }}</span>
              </div>
              <div class="form-group">
                <label>ที่อยู่ :</label>
                <span>{{ employee.address || '-' }}</span>
              </div>
              <div class="form-group">
                <label>Email :</label>
                <span>{{ employee.email || '-' }}</span>
              </div>
              <div class="form-group">
                <label>เบอร์โทรศัพท์ :</label>
                <span>{{ employee.phone_number || '-' }}</span>
              </div>
            </div>

            <div class="form-box">
              <label class="box-title">รหัสของระบบอื่นๆ :</label>
              <div class="form-group">
                <label>รหัสบัญชี :</label>
                <span>{{ employee.employee_code || '-' }}</span>
              </div>
              <div class="form-group">
                <label>ลาป่วยคงเหลือ :</label>
                <span>{{ employee.quota_sick || '0' }}</span>
              </div>
              <div class="form-group">
                <label>ลาพักร้อนคงเหลือ :</label>
                <span>{{ employee.quota_vacation || '0' }}</span>
              </div>
              <div class="form-group">
                <label>ลากิจคงเหลือ :</label>
                <span>{{ employee.quota_casual || '0' }}</span>
              </div>
              <div class="form-group">
                <label>ลาอื่นๆคงเหลือ :</label>
                <span>{{ employee.quota_other || '0' }}</span>
              </div>
            </div>
          </div>

          <div class="form-actions">
            <button class="btn-back" @click="goToAdmin2Page">ย้อนกลับ</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import axios from 'axios';
import { useRouter, useRoute } from 'vue-router';

import TopBar from '~/components/Topbar.vue'

const router = useRouter();
const route = useRoute();
const token = ref<string | null>(null);
const currentUser = ref<any>(null);
const employee = ref<any>(null);
const loading = ref(false);
const errorMessage = ref('');
const showProfileMenu = ref(false);

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

const loadEmployee = async (id: number) => {
  loading.value = true;
  errorMessage.value = '';
  try {
    const response = await axios.get(`http://localhost:8000/api/users/${id}/`);
    employee.value = response.data;
    console.log('Employee data:', employee.value);
  } catch (err: any) {
    console.error('Error fetching employee data:', err);
    if (err.response?.status === 404) {
      errorMessage.value = 'ไม่พบข้อมูลพนักงาน';
    } else {
      errorMessage.value = 'ไม่สามารถโหลดข้อมูลพนักงานได้';
    }
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  token.value = localStorage.getItem("token");

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

    const employeeId = route.params.id;
    if (employeeId) {
      await loadEmployee(Number(employeeId));
    } else {
      errorMessage.value = 'ไม่พบรหัสพนักงาน';
      router.push('/admin2');
    }
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
  color: #f44336;
}

.form-section {
  margin-top: 1rem;
}

.form-grid, .form-grid-columns-2 {
  display: grid;
  gap: 1rem;
}

.form-grid {
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}

.form-grid-columns-2 {
  grid-template-columns: 1fr 1fr;
}

.form-box {
  border: 1px solid #ddd;
  padding: 1rem;
  border-radius: 4px;
}

.box-title {
  font-weight: bold;
  font-size: 1.2rem;
  margin-bottom: 1rem;
  display: block;
}

.form-box .box-title {
  display: block;
  font-size: 1.1em;
  font-weight: bold;
  margin-bottom: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.form-group span {
  padding: 0.5rem;
  background: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-group .form-input {
  flex-grow: 1;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

@media (max-width: 768px) {
  .form-grid, .form-grid-columns-2 {
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

.loading {
  text-align: center;
  font-size: 1.2rem;
  margin: 2rem 0;
}

.error-message {
  color: red;
  margin-bottom: 1rem;
  text-align: center;
}

.form-actions {
  margin-top: 1rem;
  text-align: center;
}

.btn-back {
  padding: 0.5rem 1rem;
  background: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.btn-back:hover {
  background: #5a6268;
}
</style>