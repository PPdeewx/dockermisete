<template>
  <div class="full-page-container">
    

    <main class="main-content">
      <TopBar > <template #breadcrumbs>
              <Breadcrumb  :model="items"/>
      </template></TopBar>

      <div class="settings-container">
        <aside class="settings-sidebar">
          <ul class="settings-menu">
            <li class="menu-item active">
              <i class="fas fa-user"></i>
              <span>ข้อมูลส่วนตัว</span>
            </li>
          </ul>
        </aside>
        <div class="settings-content">
          <div class="profile-card">
            <div class="profile-header">
              <i class="fas fa-user icon-red"></i>
              <h3>ข้อมูลส่วนตัว</h3>
            </div>
            <div class="profile-body">
              <div class="profile-form-row">
                <div class="form-group">
                  <label>ชื่อภาษาไทย :</label>
                  <input type="text" :value="`${user?.firstname_th ?? ''} ${user?.lastname_th ?? ''}`" class="text-input" readonly />
                </div>
              </div>
              <div class="profile-form-row">
                <div class="form-group">
                  <label>ชื่อภาษาอังกฤษ :</label>
                  <input type="text" :value="`${user?.firstname_en ?? ''} ${user?.lastname_en ?? ''}`" class="text-input" readonly />
                </div>
              </div>
              <div class="profile-form-row">
                <div class="form-group">
                  <label>ตำแหน่ง :</label>
                  <input type="text" :value="user?.groupName || '-'" class="text-input" readonly />
                </div>
              </div>
              
              <div class="profile-section">
                <div class="profile-info-block">
                  <div class="info-group">
                    <label>ประเภทการจ้างงาน :</label>
                    <span>{{ user?.groupName }}</span>
                  </div>
                  <div class="info-group">
                    <label>วันที่เริ่มทำงาน :</label>
                    <span>{{ user?.start_date }}</span>
                  </div>
                  <div class="info-group">
                    <label>วันเกิด :</label>
                    <span>{{ user?.birth_date }}</span>
                  </div>
                  <div class="info-group">
                    <label>ที่อยู่ :</label>
                    <span>{{ user?.address }}</span>
                  </div>
                  <div class="info-group">
                    <label>Email :</label>
                    <span>{{ user?.email }}</span>
                  </div>
                  <div class="info-group">
                    <label>เบอร์โทรศัพท์ :</label>
                    <span>{{ user?.phone_number }}</span>
                  </div>
                </div>
                <div class="profile-info-block">
                </div>
              </div>

              <div class="leave-info-card">
                <label>รหัสเครื่องสแกนลายนิ้วมือ :</label>
                <span>{{ user?.fingerprint_id }}</span>
                <div class="leave-balance">
                  <p>วันลากิจคงเหลือ : {{ user?.quota_casual ?? 0 }} วัน</p>
                  <p>วันลาป่วยคงเหลือ : {{ user?.quota_sick ?? 0 }} วัน</p>
                  <p>วันลาพักร้อนคงเหลือ : {{ user?.quota_vacation ?? 0 }} วัน</p>
                  <p>วันลาอื่นๆคงเหลือ : {{ user?.quota_other ?? 0 }} วัน</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';

import TopBar from '~/components/Topbar.vue'

const user = ref<any>(null);
const token = ref<string | null>(null);

const router = useRouter();
const route = useRoute();

import type { MenuItem } from 'primevue/menuitem';

const items : MenuItem[] = [
  {
    label : 'หน้าหลัก',url : '/user'
  },
  {
    label : 'ดูข้อมูลส่วนตัว',url : '/Profile'
  }
]

onMounted(async () => {
  const tokenStored = localStorage.getItem("token");
  if (!tokenStored) {
    router.push("/login");
    return;
  }
  axios.defaults.headers.common['Authorization'] = `Token ${tokenStored}`;

  try {
    const response = await axios.get("http://localhost:8000/api/users/me/");
    user.value = response.data;
    if (user.value.role !== "employee") {
      router.push("/login");
    }
  } catch (err) {
    console.error(err);
    router.push("/login");
  }
});

const showProfileMenu = ref(false);
function toggleProfileMenu() {
  showProfileMenu.value = !showProfileMenu.value;
}
function handleBodyClick(event: MouseEvent) {
  if (showProfileMenu.value && !(event.target as HTMLElement).closest('.user-profile')) {
    showProfileMenu.value = false;
  }
}
onMounted(() => document.addEventListener('click', handleBodyClick));
onBeforeUnmount(() => document.removeEventListener('click', handleBodyClick));

function goTo(path: string) {
  router.push(path);
}
function logout() {
  localStorage.removeItem("token")
  delete axios.defaults.headers.common['Authorization']
  router.push("/login")
}


</script>


<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;700&display=swap');

* {
  box-sizing: border-box;
  font-family: 'Inter', 'Prompt', sans-serif;
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

.logo {
  width: 40px;
  height: 40px;
  margin-right: 10px;
  border-radius: 50%;
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

.user-profile {
  display: flex;
  align-items: center;
  position: relative;
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

.settings-container {
  display: flex;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  min-height: 80vh;
}

.settings-sidebar {
  width: 250px;
  border-right: 1px solid #eee;
  padding: 20px;
}

.settings-menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 12px 15px;
  cursor: pointer;
  border-radius: 5px;
  color: #555;
  font-weight: bold;
  transition: background-color 0.2s;
}

.menu-item i {
  margin-right: 10px;
  color: #888;
}

.menu-item.active {
  background-color: #e6f7ff;
  color: #1890ff;
}

.menu-item.active i {
  color: #1890ff;
}

.settings-content {
  flex-grow: 1;
  padding: 30px;
}

.profile-card {
  background-color: #ffffff;
}

.profile-header {
  display: flex;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 20px;
}

.icon-red {
  color: #e74c3c;
  font-size: 30px;
  margin-right: 15px;
}

.profile-header h3 {
  margin: 0;
  font-size: 22px;
}

.profile-body {
  display: flex;
  flex-direction: column;
}

.profile-form-row {
  display: flex;
  margin-bottom: 15px;
}

.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: bold;
  margin-bottom: 5px;
}

.text-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 14px;
}

.profile-section {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.profile-info-block {
  flex: 1;
  background-color: #fafafa;
  padding: 15px;
  border-radius: 8px;
}

.info-group {
  margin-bottom: 10px;
}

.info-group label {
  font-weight: bold;
  color: #555;
  margin-right: 10px;
}

.leave-info-card {
  background-color: #fafafa;
  padding: 15px;
  border-radius: 8px;
  margin-top: 20px;
}

.leave-info-card label {
  font-weight: bold;
  color: #555;
}

.leave-balance {
  margin-top: 10px;
}
.leave-balance p {
  margin: 5px 0;
}
</style>