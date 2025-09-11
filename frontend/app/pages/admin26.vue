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
        </li>
        <li class="nav-item"><a href="/admin10" class="nav-link" @click.prevent="goToAdmin10Page"><i class="fas fa-flask"></i> ห้องวิจัย</a></li>
        <li class="nav-item"><a href="/admin11" class="nav-link" @click.prevent="goToAdmin11Page"><i class="fas fa-calendar-alt"></i> วันหยุด</a></li>
        <li class="nav-item"><a href="/admin12" class="nav-link" @click.prevent="goToAdmin12Page"><i class="fas fa-cog"></i> ระบบการปฏิบัติงาน</a></li>
      </ul>
    </div>

    <div class="main-content">
      <div class="top-bar">
        <div class="breadcrumbs">
          <span><i class="fas fa-home"></i> หน้าหลัก > เพิ่ม / แก้ไข ห้องวิจัย</span>
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
          <div class="header-with-icon">
            <i class="fas fa-flask"></i>
            <h2>เพิ่ม / แก้ไข ห้องวิจัย</h2>
          </div>
          <button class="btn-cancel" @click="goToAdmin10Page"><i class="fas fa-times"></i> ยกเลิก</button>
        </div>

        <div class="form-section">
          <div class="form-row">
            <label for="labNameTh">ชื่อห้องปฏิบัติการภาษาไทย * :</label>
            <div class="input-container">
              <input type="text" id="labNameTh" v-model="form.labNameTh" class="form-input">
              <span class="input-description">Labels can have inline descriptions</span>
            </div>
          </div>
          <div class="form-row">
            <label for="labNameEn">ชื่อห้องปฏิบัติการอังกฤษ * :</label>
            <div class="input-container">
              <input type="text" id="labNameEn" v-model="form.labNameEn" class="form-input">
              <span class="input-description">Labels can have inline descriptions</span>
            </div>
          </div>
          <div class="form-row">
            <label for="labNameAbbr">ชื่อย่อห้องวิจัย :</label>
            <div class="input-container">
              <input type="text" id="labNameAbbr" v-model="form.labNameAbbr" class="form-input">
              <span class="input-description">มี หรือ ไม่มีก็ได้</span>
            </div>
          </div>
          <div class="form-row">
            <label for="labHead">หัวหน้าห้องวิจัย :</label>
            <div class="input-container">
              <select id="labHead" v-model="form.labHead" class="form-input">
                <option value="">กรุณาเลือกหัวหน้าห้องวิจัย</option>
                <option v-for="employee in employees" :key="employee.id" :value="employee.name">{{ employee.name }}</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <label for="labDesc">คำอธิบายห้องวิจัย * :</label>
            <div class="input-container">
              <textarea id="labDesc" v-model="form.labDesc" class="form-input textarea-input"></textarea>
            </div>
          </div>
        </div>

        <div class="member-selection-section">
          <div class="section-header">
            <h3>พนักงานในห้องวิจัย:</h3>
            <span>รายชื่อในช่องด้านขวามือ คือ พนักงานในห้องวิจัย</span>
          </div>
          <div class="member-selection-container">
            <div class="member-list">
              <div class="list-title">พนักงานที่ไม่ได้สังกัด</div>
              <ul class="employee-list">
                <li v-for="employee in unassignedEmployees" :key="employee.id" @click="selectEmployee(employee)">
                  {{ employee.name }}
                </li>
              </ul>
            </div>
            <div class="action-buttons">
              <button class="btn-action-move" @click="assignSelected"><i class="fas fa-angle-right"></i></button>
              <button class="btn-action-move" @click="unassignSelected"><i class="fas fa-angle-left"></i></button>
            </div>
            <div class="member-list">
              <div class="list-title">พนักงานในห้องวิจัย</div>
              <ul class="employee-list">
                <li v-for="employee in assignedEmployees" :key="employee.id" @click="unselectEmployee(employee)">
                  {{ employee.name }}
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div class="button-footer">
          <button class="btn-save-data" @click="goToAdmin10Page"><i class="fas fa-save"></i> บันทึกข้อมูล</button>
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

const form = reactive({
  labNameTh: '',
  labNameEn: '',
  labNameAbbr: '',
  labHead: '',
  labDesc: ''
});

const allEmployees = ref([
  { id: 1, name: 'นาย A พนักงาน' },
  { id: 2, name: 'นาย B พนักงาน' },
  { id: 3, name: 'นาง C พนักงาน' },
  { id: 4, name: 'นาย D พนักงาน' },
  { id: 5, name: 'นาย E พนักงาน' },
]);

const unassignedEmployees = ref([...allEmployees.value]);
const assignedEmployees = ref<typeof allEmployees.value>([]);

const selectedUnassigned = ref<any>(null);
const selectedAssigned = ref<any>(null);


const selectEmployee = (employee: any) => {
  selectedUnassigned.value = employee;
};

const unselectEmployee = (employee: any) => {
  selectedAssigned.value = employee;

};

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

const assignSelected = () => {
  if (selectedUnassigned.value) {
    assignedEmployees.value.push(selectedUnassigned.value);
    unassignedEmployees.value = unassignedEmployees.value.filter(emp => emp.id !== selectedUnassigned.value.id);
    selectedUnassigned.value = null;
  }
};

const unassignSelected = () => {
  if (selectedAssigned.value) {
    unassignedEmployees.value.push(selectedAssigned.value);
    assignedEmployees.value = assignedEmployees.value.filter(emp => emp.id !== selectedAssigned.value.id);
    selectedAssigned.value = null;
  }
};

const saveData = () => {
  console.log('บันทึกข้อมูล:', {
    form: form,
    assignedEmployees: assignedEmployees.value
  });

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

.header-with-button {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 20px;
}

.header-with-icon {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-with-icon h2 {
  font-size: 24px;
  font-weight: bold;
  margin: 0;
}

.header-with-icon i {
  color: #f44336;
}

.btn-cancel {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  display: flex;
  align-items: center;
  gap: 5px;
}

.btn-cancel:hover {
  background-color: #da3329;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
  border-bottom: 1px solid #eee;
  padding-bottom: 20px;
  margin-bottom: 20px;
}

.form-row {
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

.form-row label {
  font-weight: bold;
  width: 250px;
  text-align: right;
  padding-top: 8px;
}

.input-container {
  flex-grow: 1;
}

.form-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1em;
}

.textarea-input {
  min-height: 120px;
  resize: vertical;
}

.input-description {
  display: block;
  font-size: 0.85em;
  color: #888;
  margin-top: 5px;
}

.member-selection-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.section-header h3 {
  margin: 0;
}

.section-header span {
  color: #888;
  font-size: 0.9em;
}

.member-selection-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.member-list {
  width: 40%;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.list-title {
  padding: 10px;
  font-weight: bold;
  background-color: #eee;
  border-bottom: 1px solid #ddd;
}

.employee-list {
  list-style: none;
  padding: 0;
  margin: 0;
  min-height: 200px;
  overflow-y: auto;
}

.employee-list li {
  padding: 10px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
}

.employee-list li:hover {
  background-color: #e6f7ff;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.btn-action-move {
  background-color: #1890ff;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
}

.btn-action-move:hover {
  background-color: #096dd9;
}

.button-footer {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.btn-save-data {
  background-color: #52c41a;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1.1em;
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn-save-data:hover {
  background-color: #389e08;
}

@media (max-width: 768px) {
  .top-bar, .header-with-button {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }

  .form-row {
    flex-direction: column;
    gap: 5px;
  }

  .form-row label {
    text-align: left;
    width: 100%;
  }

  .member-selection-container {
    flex-direction: column;
  }

  .member-list {
    width: 100%;
  }

  .action-buttons {
    flex-direction: row;
    gap: 20px;
    width: 100%;
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
</style>