<template>
  <div class="full-page-container">
    <aside class="sidebar">
      <div class="sidebar-header">
        <span>MIS ETE</span>
      </div>
      <ul class="nav-menu">
        <li class="nav-item" :class="{ 'active': $route.path === '/user' }">
          <router-link to="/user" class="nav-link">
            <i class="fas fa-home"></i> หน้าหลัก
          </router-link>
        </li>
        <li class="nav-item" :class="{ 'active': $route.path === '/user2' }">
          <router-link to="/user2" class="nav-link">
            <i class="fas fa-file-alt"></i> ยื่นใบลา
          </router-link>
        </li>
        <li class="nav-item" :class="{ 'active': $route.path === '/user3' }">
          <router-link to="/user3" class="nav-link">
            <i class="fas fa-file-alt"></i> ยื่นใบลาเเทน
          </router-link>
        </li>
        <li class="nav-item" :class="{ 'active': $route.path === '/user4' }">
          <router-link to="/user4" class="nav-link">
            <i class="fas fa-history"></i> ประวัติการลา
          </router-link>
        </li>
        <li class="nav-item" :class="{ 'active': $route.path === '/user5' }">
          <router-link to="/user5" class="nav-link">
            <i class="fas fa-user-edit"></i> ขออนุญาตปฏิบัติงานนอกสถานที่
          </router-link>
        </li>
        <li class="nav-item" :class="{ 'active': $route.path === '/user6' }">
          <router-link to="/user6" class="nav-link">
            <i class="fas fa-user-edit"></i> ขออนุญาตปฏิบัติงานนอกสถานที่ให้คนอื่น
          </router-link>
        </li>
        <li class="nav-item" :class="{ 'active': $route.path === '/user7' }">
          <router-link to="/user7" class="nav-link">
            <i class="fas fa-calendar-times"></i> ดูรายการปฏิบัติงานนอกสถานที่
          </router-link>
        </li>
        <li class="nav-item" :class="{ 'active': $route.path === '/user8' }">
          <router-link to="/user8" class="nav-link">
            <i class="fas fa-calendar-plus"></i> วันหยุด
          </router-link>
        </li>
      </ul>
    </aside>

    <main class="main-content">
      <div class="top-bar">
        <div class="breadcrumbs">
          <span><i class="fas fa-home"></i> {{ breadcrumbs }}</span>
        </div>
        
        <div class="user-profile" @click.stop="toggleProfileMenu">
          <i class="fas fa-bell"></i>
          <i class="fas fa-user-circle"></i>
          <span class="username">{{ user?.username }}</span>
          <span v-if="user">ตำแหน่ง: {{ user.role }}</span>
          <i class="fas fa-chevron-down"></i>

          <div class="user-profile-menu" v-if="showProfileMenu">
            <button class="menu-item" @click.stop="goTo('/user10')">
              <i class="fas fa-user"></i>
              <span>ดูข้อมูลส่วนตัว</span>
            </button>
            <button class="menu-item" @click.stop="goTo('/user11')">
              <i class="fas fa-edit"></i>
              <span>แก้ไขข้อมูลส่วนตัว</span>
            </button>
            <button class="menu-item" @click.stop="goTo('/user12')">
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

      <div class="work-history-container">
        <div class="work-history-header">
          <div class="header-left">
            <i class="fas fa-calendar-alt icon-red"></i>
            <div>
              <h3>ประวัติรายการปฏิบัติงานนอกสถานที่</h3>
            </div>
          </div>
          <router-link to="/user5" class="btn-create-request">
            <i class="fas fa-plus-circle"></i> ขออนุมัติปฏิบัติงานนอกสถานที่
          </router-link>
        </div>
        
        <div class="user-info-box">
          <div class="user-info-card">
            <div class="user-avatar-placeholder">
              <i class="fas fa-user-circle"></i>
            </div>
            <div class="user-details">
              <span>รหัส {{ user?.employee_code || 'N/A' }}</span>
              <p>{{ user?.firstname_th || 'Username' }} {{ user?.lastname_th || 'Username' }}</p>
            </div>
          </div>
        </div>

        <h4 class="table-title">ประวัติรายการปฏิบัติงานนอกสถานที่</h4>
        <div class="work-history-table-wrapper">
          <table class="work-history-table">
            <thead>
              <tr>
                <th>เลขที่ใบลา</th>
                <th>วันที่ลา</th>
                <th>พนักงาน</th>
                <th>ช่วงเวลา</th>
                <th>เหตุผล</th>
                <th>สถานะ</th>
                <th>ดำเนินการ</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in workHistory" :key="index">
                <td>{{ item.id }}</td>
                <td>{{ item.date }}</td>
                <td>{{ item.employee }}</td>
                <td>{{ item.period }}</td>
                <td>{{ item.reason }}</td>
                <td>{{ item.status }}</td>
                <td class="actions-cell">
                  <i class="fas fa-edit action-icon" @click="openEditModal(item)"></i>
                  <i class="fas fa-search-plus action-icon" @click="goTo('/user15')"></i>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
 
    <div v-if="showEditModal" class="modal-backdrop">
      <div class="modal-content">
        <div class="modal-header">
          <h3>แก้ไขข้อมูลการปฏิบัติงานนอกสถานที่ {{ selectedItem?.employee }}</h3>
          <button class="modal-close-button red" @click="closeEditModal">ยกเลิก</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <label>พนักงาน :</label>
            <span class="form-text">{{ selectedItem?.employee }}</span>
          </div>

          <div class="form-row">
            <label>ผู้ร่วมปฏิบัติงาน :</label>
            <select class="select-input" v-model="selectedItem.collaborators" multiple>
              <option v-for="user in allUsers" :key="user.id" :value="user.id">
                {{ user.full_name }}
              </option>
            </select>
            <div class="selected-names">
              <span v-for="id in selectedItem.collaborators" :key="id">
                {{ allUsers.find(u => u.id === id)?.full_name || '' }}
                <span v-if="id !== selectedItem.collaborators[selectedItem.collaborators.length-1]">, </span>
              </span>
            </div>
          </div>

          <div class="form-row date-row">
            <label>ลาตั้งแต่วันที่ :</label>
            <input type="date" v-model="selectedItem.start_date" class="date-input" />
            <label>ถึงวันที่ * :</label>
            <input type="date" v-model="selectedItem.end_date" class="date-input" />
          </div>

          <div class="form-row">
            <label>ช่วงเวลา :</label>
            <div class="radio-group">
              <label><input type="radio" value="morning" v-model="selectedItem.period"> ครึ่งวันเช้า</label>
              <label><input type="radio" value="afternoon" v-model="selectedItem.period"> ครึ่งวันบ่าย</label>
              <label><input type="radio" value="full" v-model="selectedItem.period"> ทั้งวัน</label>
            </div>
          </div>

          <div class="form-row">
            <label>เหตุผลการลา :</label>
            <input type="text" v-model="selectedItem.reason" class="text-input" />
          </div>

          <div class="form-row">
            <label>หัวหน้างาน :</label>
            <select class="select-input" v-model="selectedItem.approver">
              <option value="">เลือกหัวหน้างาน</option>
              <option v-for="user in allUsers" :key="user.id" :value="user.id">
                {{ user.full_name }}
              </option>
            </select>
            <div class="selected-names">
              <span v-if="selectedItem.approver">
                {{ allUsers.find(u => u.id === selectedItem.approver)?.full_name || '' }}
              </span>
            </div>
          </div>

          <button class="edit-button yellow" @click="saveEdit">
            <i class="fas fa-edit"></i> แก้ไขข้อมูล
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';

const user = ref<any>(null);
const token = ref<string | null>(null);

const allUsers = ref<any[]>([]);

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

    const usersRes = await axios.get("http://localhost:8000/api/users/");
    allUsers.value = usersRes.data;

    await loadWorkHistory();

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
onMounted(() => {
  document.addEventListener('click', handleBodyClick);
});
onBeforeUnmount(() => {
  document.removeEventListener('click', handleBodyClick);
});

const router = useRouter();
const route = useRoute();

function goTo(path: string) {
  router.push(path);
}
function logout() {
  localStorage.removeItem("token")
  delete axios.defaults.headers.common['Authorization']
  router.push("/login")
}

const workHistory = ref<any[]>([]);
const showEditModal = ref(false);
const selectedItem = ref<any>(null);

function openEditModal(item: any) {
  selectedItem.value = { ...item }; 
  showEditModal.value = true;
}

function closeEditModal() {
  showEditModal.value = false;
  selectedItem.value = null;
}

async function saveEdit() {
  if (!selectedItem.value) return;
  try {

    await axios.patch(`http://localhost:8000/api/work-from-outside/requests/${selectedItem.value.id}/`, selectedItem.value);
    
    const index = workHistory.value.findIndex((w) => w.id === selectedItem.value.id);
    if (index !== -1) workHistory.value[index] = { ...selectedItem.value };
    
    closeEditModal();
  } catch (err) {
    console.error("ไม่สามารถแก้ไขได้:", err);
  }
}

const loadWorkHistory = async () => {
  if (!user.value) return;
  try {
    const res = await axios.get(`http://localhost:8000/api/work-from-outside/requests/?user=${user.value.id}`);
    workHistory.value = res.data.map((item: any) => ({
      id: item.request_number,
      date: `${item.start_date} - ${item.end_date}`,
      start_date: item.start_date,    
      end_date: item.end_date,        
      employee: item.user.full_name || "ไม่ระบุ",
      collaborators: item.collaborators ? item.collaborators.map((u: any) => u.id) : [],
      approver: item.approver?.id || null,
      period: item.time_period,
      reason: item.reason,
      status:
        item.status === "pending"
          ? "รอการอนุมัติ"
          : item.status === "approved"
          ? "อนุมัติแล้ว"
          : item.status === "rejected"
          ? "ไม่อนุมัติ"
          : item.status === "cancelled"
          ? "ยกเลิก"
          : "อื่น ๆ",
    }));
  } catch (err) {
    console.error("ไม่สามารถโหลดประวัติได้:", err);
  }
};

const breadcrumbs = computed(() => {
  switch (route.path) {
    case '/user':
      return 'หน้าหลัก';
    case '/user2':
      return 'หน้าหลัก > ยื่นใบลา';
    case '/user3':
      return 'หน้าหลัก > ยื่นใบลาแทน';
    case '/user4':
      return 'หน้าหลัก > ประวัติการลา';
    case '/user5':
      return 'หน้าหลัก > ขออนุญาตปฏิบัติงานนอกสถานที่';
    case '/user6':
      return 'หน้าหลัก > ขออนุญาตปฏิบัติงานนอกสถานที่ให้คนอื่น';
    case '/user7':
      return 'หน้าหลัก > ดูรายการปฏิบัติงานนอกสถานที่';
    case '/user8':
      return 'หน้าหลัก > วันหยุด';
    case '/user10':
      return 'หน้าหลัก > ข้อมูลส่วนตัว';
    case '/user11':
      return 'หน้าหลัก > ข้อมูลส่วนตัว > แก้ไข';
    case '/user12':
      return 'หน้าหลัก > เปลี่ยนรหัสผ่าน';
    default:
      return 'หน้าหลัก';
  }
});
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

.work-history-container {
  background-color: #ffffff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.work-history-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 20px;
}

.header-left {
  display: flex;
  align-items: center;
}

.icon-red {
  color: #e74c3c;
  font-size: 30px;
  margin-right: 15px;
}

.work-history-header h3 {
  margin: 0;
  font-size: 22px;
}

.btn-create-request {
  background: #f1f1f1;
  color: #4caf50;
  padding: 8px 14px;
  border: 1px solid #4caf50;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  font-weight: bold;
  white-space: nowrap;
}

.btn-create-request i {
  margin-right: 5px;
}

.user-info-box {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.user-info-card {
  display: flex;
  align-items: center;
}

.user-avatar-placeholder {
  width: 60px;
  height: 60px;
  background-color: #ddd;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 15px;
}
.user-avatar-placeholder i {
    font-size: 24px;
    color: #888;
}

.user-details span {
  font-weight: bold;
  color: #555;
  font-size: 14px;
}
.user-details p {
    margin: 0;
    font-size: 16px;
    font-weight: bold;
}

.table-title {
    font-size: 18px;
    margin-bottom: 15px;
    padding-left: 10px;
    border-left: 4px solid #1890ff;
}

.work-history-table-wrapper {
  overflow-x: auto;
}

.work-history-table {
  width: 100%;
  border-collapse: collapse;
}

.work-history-table th,
.work-history-table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

.work-history-table th {
  background-color: #f2f2f2;
  font-weight: bold;
}

.work-history-table tbody tr:nth-child(even) {
  background-color: #fafafa;
}

.work-history-table tbody tr:hover {
  background-color: #e6f7ff;
}

.actions-cell i {
  margin-right: 10px;
  cursor: pointer;
  font-size: 16px;
}
.fa-search-plus {
  color: #1890ff;
}
.fa-trash-alt {
  color: #e74c3c;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  width: 600px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 15px;
  margin-bottom: 20px;
}

.modal-header h3 {
  font-size: 18px;
  font-weight: bold;
  margin: 0;
}

.modal-close-button {
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  color: white;
}

.modal-close-button.red {
  background-color: #dc3545;
}
.modal-close-button.red:hover {
  background-color: #c82333;
}

.modal-body .form-row {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.modal-body .form-row label {
  width: 150px;
  font-weight: bold;
  font-size: 14px;
}

.modal-body .form-row .form-text {
  font-size: 14px;
}

.radio-group label {
  font-weight: normal;
  margin-right: 15px;
  display: inline-flex;
  align-items: center;
}

.radio-group input {
  margin-right: 5px;
}

.modal-body .date-row {
  align-items: center;
}

.modal-body .date-input,
.modal-body .text-input,
.modal-body .select-input {
  flex-grow: 1;
  padding: 8px 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

.modal-body .date-input {
    width: 150px;
}

.modal-body .text-input {
    width: 300px;
}
.modal-body .select-input {
    width: 300px;
}

.modal-body .edit-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 20px;
  float: right;
  color: white;
}

.modal-body .edit-button.yellow {
  background-color: #ffc107;
}
.modal-body .edit-button.yellow:hover {
  background-color: #e0a800;
}
</style>