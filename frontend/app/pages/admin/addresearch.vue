<template>
    <TopBar > <template #breadcrumbs>
              <Breadcrumb  :model="items"/>

    </template></TopBar>

      <div class="content-container">
        <div class="header-with-button">
          <div class="header-with-icon">
            <i class="fas fa-flask"></i>
            <h2>{{ isEditMode ? 'แก้ไข' : 'เพิ่ม' }} ห้องวิจัย</h2>
          </div>
          <button class="btn-cancel" @click="goToAdmin10Page"><i class="fas fa-times"></i> ยกเลิก</button>
        </div>

        <div v-if="loading" class="loading">กำลังโหลด...</div>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

        <div class="form-section" v-if="!loading">
          <div class="form-row">
            <label for="labNameTh">ชื่อห้องปฏิบัติการภาษาไทย * :</label>
            <div class="input-container">
              <input type="text" id="labNameTh" v-model="form.labNameTh" class="form-input" required />
              <span class="input-description">กรุณากรอกชื่อห้องปฏิบัติการภาษาไทย</span>
            </div>
          </div>
          <div class="form-row">
            <label for="labNameEn">ชื่อห้องปฏิบัติการอังกฤษ * :</label>
            <div class="input-container">
              <input type="text" id="labNameEn" v-model="form.labNameEn" class="form-input" required />
              <span class="input-description">กรุณากรอกชื่อห้องปฏิบัติการภาษาอังกฤษ</span>
            </div>
          </div>
          <div class="form-row">
            <label for="labNameAbbr">ชื่อย่อห้องวิจัย :</label>
            <div class="input-container">
              <input type="text" id="labNameAbbr" v-model="form.labNameAbbr" class="form-input" />
              <span class="input-description">มีหรือไม่มีก็ได้</span>
            </div>
          </div>
          <div class="form-row">
            <label for="labHead">หัวหน้าห้องวิจัย :</label>
            <div class="input-container">
              <select id="labHead" v-model="form.labHead" class="form-input">
                <option value="">กรุณาเลือกหัวหน้าห้องวิจัย</option>
                <option v-for="employee in allEmployees" :key="employee.id" :value="employee.id">
                  {{ employee.firstname_th }} {{ employee.lastname_th }}
                </option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <label for="labDesc">คำอธิบายห้องวิจัย * :</label>
            <div class="input-container">
              <textarea id="labDesc" v-model="form.labDesc" class="form-input textarea-input" required></textarea>
            </div>
          </div>
        </div>

        <div class="member-selection-section" v-if="!loading">
          <div class="section-header">
            <h3>พนักงานในห้องวิจัย:</h3>
            <span>รายชื่อในช่องด้านขวามือ คือ พนักงานในห้องวิจัย</span>
          </div>
          <div class="member-selection-container">
            <div class="member-list">
              <div class="list-title">พนักงานที่ไม่ได้สังกัด</div>
              <ul class="employee-list">
                <li v-for="employee in unassignedEmployees" :key="employee.id" @click="selectEmployee(employee)">
                  {{ employee.firstname_th }} {{ employee.lastname_th }}
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
                  {{ employee.firstname_th }} {{ employee.lastname_th }}
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div class="button-footer">
          <button class="btn-save-data" @click="saveData"><i class="fas fa-save"></i> บันทึกข้อมูล</button>
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
    label : 'ห้องวิจัย',url : '/research'
  },
  {
    label : 'เพิ่มวิจัย',url : '/addresearch'
  }
]
const router = useRouter();
const route = useRoute();
const token = ref<string | null>(null);
const currentUser = ref<any>(null);
const showProfileMenu = ref(false);
const loading = ref(false);
const errorMessage = ref('');

const form = reactive({
  labNameTh: '',
  labNameEn: '',
  labNameAbbr: '',
  labHead: '',
  labDesc: ''
});

const allEmployees = ref<any[]>([]);
const unassignedEmployees = ref<any[]>([]);
const assignedEmployees = ref<any[]>([]);
const selectedUnassigned = ref<any>(null);
const selectedAssigned = ref<any>(null);
const deptId = ref<number | null>(null);
const isEditMode = computed(() => !!deptId.value);

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

const selectEmployee = (employee: any) => {
  selectedUnassigned.value = employee;
};

const unselectEmployee = (employee: any) => {
  selectedAssigned.value = employee;
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

const saveData = async () => {
  if (!form.labNameTh || !form.labNameEn || !form.labDesc) {
    errorMessage.value = 'กรุณากรอกข้อมูลที่จำเป็นทั้งหมด';
    return;
  }

  const payload = {
    name_th: form.labNameTh,
    name_en: form.labNameEn,
    name_abbr: form.labNameAbbr,
    description: form.labDesc,
    approvers: form.labHead ? [form.labHead] : [],
    personnel: assignedEmployees.value.map(emp => emp.id)
  };

  try {
    loading.value = true;
    errorMessage.value = '';
    if (isEditMode.value) {
      await axios.put(`http://localhost:8000/api/users/departments/${deptId.value}/`, payload, {
        headers: { Authorization: `Token ${token.value}` }
      });
    } else {
      await axios.post('http://localhost:8000/api/users/departments/', payload, {
        headers: { Authorization: `Token ${token.value}` }
      });
    }
    router.push('/admin10');
  } catch (err: any) {
    errorMessage.value = err.response?.data?.detail || 'ไม่สามารถบันทึกข้อมูลได้';
    console.error('Error saving department:', err);
  } finally {
    loading.value = false;
  }
};

const loadDepartment = async (id: number) => {
  try {
    loading.value = true;
    errorMessage.value = '';
    const response = await axios.get(`http://localhost:8000/api/users/departments/${id}/`, {
      headers: { Authorization: `Token ${token.value}` }
    });
    const dept = response.data;
    form.labNameTh = dept.name_th;
    form.labNameEn = dept.name_en;
    form.labNameAbbr = dept.name_abbr || '';
    form.labDesc = dept.description || '';
    form.labHead = dept.approvers && dept.approvers.length > 0 ? dept.approvers[0].id : '';

    assignedEmployees.value = allEmployees.value.filter(emp =>
      dept.personnel.includes(`${emp.firstname_th} ${emp.lastname_th}`)
    );
    unassignedEmployees.value = allEmployees.value.filter(emp =>
      !dept.personnel.includes(`${emp.firstname_th} ${emp.lastname_th}`)
    );
  } catch (err: any) {
    errorMessage.value = 'ไม่สามารถโหลดข้อมูลห้องวิจัยได้';
    console.error('Error loading department:', err);
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
  } catch (err) {
    console.error('Error fetching user:', err);
    router.push('/login');
    return;
  }

  try {
    loading.value = true;
    const response = await axios.get('http://localhost:8000/api/users/', {
      headers: { Authorization: `Token ${token.value}` }
    });
    allEmployees.value = response.data;
    unassignedEmployees.value = [...allEmployees.value];
  } catch (err) {
    errorMessage.value = 'ไม่สามารถโหลดรายชื่อพนักงานได้';
    console.error('Error loading employees:', err);
  } finally {
    loading.value = false;
  }

  deptId.value = Number(route.query.deptId) || null;
  if (deptId.value) {
    await loadDepartment(deptId.value);
  }
});

function logout() {
  localStorage.removeItem("token");
  delete axios.defaults.headers.common['Authorization'];
  router.push("/login");
}
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;700&display=swap');

* {
  box-sizing: border-box;
  font-family: 'Noto Sans Thai', sans-serif;
}

.loading {
  text-align: center;
  font-size: 1.2rem;
  margin: 2rem 0;
}
.error-message {
  color: red;
  text-align: center;
  margin: 1rem 0;
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