<template>
  <div class="full-page-container">
    

    <main class="main-content">
      <TopBar></TopBar>

      <div class="leave-form-container">
        <div class="form-header">
          <div class="header-left">
            <i class="fas fa-calendar-check icon-red"></i>
            <div>
              <h3>ระบบการขออนุญาตปฏิบัติงานนอกสถานที่ให้คนอื่น</h3>
            </div>
          </div>
          <button type="button" class="btn-cancel" @click="cancelForm"><i class="fas fa-times-circle"></i> ยกเลิก</button>
        </div>

        <form @submit.prevent="submitForm" class="leave-form">
          <div class="form-row">
            <div class="form-group full-width">
              <label>ผู้ปฏิบัติงาน *:</label>
              <select v-model="form.employee" class="select-input" required>
                <option disabled value="">เลือกผู้ปฏิบัติงาน</option>
                <option v-for="employee in employees" :key="employee.id" :value="employee.id">
                  {{ employee.name }}
                </option>
              </select>
              <span v-if="errors.employee" class="error">{{ errors.employee }}</span>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group full-width">
              <label>ผู้ร่วมปฏิบัติงาน (เลือกได้หลายคน):</label>
              <select v-model="form.collaborators" class="select-input" multiple>
                <option v-for="person in collaboratorsList" :key="person.id" :value="person.id">
                  {{ person.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group-dates">
              <label>วันที่ *:</label>
              <input type="date" v-model="form.startDate" class="date-input" required />
              <span v-if="errors.startDate" class="error">{{ errors.startDate }}</span>
            </div>
            <div class="form-group-dates">
              <label>ถึงวันที่ *:</label>
              <input type="date" v-model="form.endDate" class="date-input" required />
              <span v-if="errors.endDate" class="error">{{ errors.endDate }}</span>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>ช่วงเวลา *:</label>
              <div class="radio-group">
                <label><input type="radio" value="ครึ่งวันเช้า" v-model="form.period" /> ครึ่งวันเช้า</label>
                <label><input type="radio" value="ครึ่งวันบ่าย" v-model="form.period" /> ครึ่งวันบ่าย</label>
                <label><input type="radio" value="ทั้งวัน" v-model="form.period" /> ทั้งวัน</label>
              </div>
              <span v-if="errors.period" class="error">{{ errors.period }}</span>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group full-width">
              <label>เหตุผล *:</label>
              <input type="text" v-model="form.reason" class="text-input" required />
              <span v-if="errors.reason" class="error">{{ errors.reason }}</span>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group full-width">
              <label>สถานที่ *:</label>
              <input type="text" v-model="form.location" class="text-input" required />
              <span v-if="errors.location" class="error">{{ errors.location }}</span>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group full-width">
              <label>หัวหน้างาน *:</label>
              <select v-model="form.approver" class="select-input" required>
                <option disabled value="">เลือกหัวหน้างาน</option>
                <option v-for="person in approvers" :key="person.id" :value="person.id">
                  {{ person.name }}
                </option>
              </select>
              <span v-if="errors.approver" class="error">{{ errors.approver }}</span>
            </div>
          </div>

          <div class="form-buttons-bottom">
            <button type="submit" class="btn-submit">ขออนุมัติ</button>
          </div>
        </form>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';

import TopBar from '~/components/Topbar.vue'

const router = useRouter();
const route = useRoute();
const user = ref<any>(null);
const employees = ref<any[]>([]);
const approvers = ref<any[]>([]);
const collaboratorsList = ref<any[]>([]);
const showProfileMenu = ref(false);
const errors = ref<any>({});

const form = ref({
  employee: '',
  collaborators: [] as number[],
  startDate: '',
  endDate: '',
  period: 'ทั้งวัน',
  reason: '',
  location: '',
  approver: ''
});

onMounted(async () => {
  const tokenStored = localStorage.getItem("token");
  if (!tokenStored) {
    alert('กรุณาล็อกอินเพื่อใช้งาน');
    router.push("/login");
    return;
  }
  axios.defaults.headers.common['Authorization'] = `Token ${tokenStored}`;

  try {
    const userResponse = await axios.get("http://localhost:8000/api/users/me/");
    user.value = userResponse.data;
    if (user.value.role !== "employee") {
      alert('เฉพาะพนักงานเท่านั้นที่สามารถใช้งานหน้านี้ได้');
      router.push("/login");
      return;
    }

    const employeesResponse = await axios.get("http://localhost:8000/api/users/for-list/");
    employees.value = employeesResponse.data;
    console.log('Employees:', employees.value);

    const approversResponse = await axios.get("http://localhost:8000/api/users/departments/");
    console.log('Departments:', approversResponse.data);
    approvers.value = approversResponse.data.flatMap((dept: any) =>
      dept.approvers.map((approver: any) => ({
        id: approver.id,
        name: `${approver.firstname_th} ${approver.lastname_th}`.trim()
      }))
    );

    const resEmployees = await axios.get("http://localhost:8000/api/users/?role=employee");
    collaboratorsList.value = resEmployees.data
    .filter((u: any) => u.role === "employee")
    .map((u: any) => ({
      id: u.id,
      name: `${u.firstname_th} ${u.lastname_th}`
    }));
    
    console.log('Approvers:', approvers.value);

    if (employees.value.length === 0) {
      alert('ไม่พบรายชื่อผู้ปฏิบัติงาน กรุณาติดต่อผู้ดูแลระบบ');
    }
    if (approvers.value.length === 0) {
      alert('ไม่พบรายชื่อหัวหน้างาน กรุณาติดต่อผู้ดูแลระบบ');
    }
  } catch (err) {
    console.error('Error fetching data:', err);
    if (err.response?.status === 403) {
      alert('คุณไม่มีสิทธิ์เข้าถึงข้อมูลนี้ กรุณาติดต่อผู้ดูแลระบบ');
    } else {
      alert('เกิดข้อผิดพลาดในการโหลดข้อมูล');
    }
    router.push("/login");
  }

  document.addEventListener('click', handleBodyClick);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleBodyClick);
});

function toggleProfileMenu() {
  showProfileMenu.value = !showProfileMenu.value;
}

function handleBodyClick(event: MouseEvent) {
  if (showProfileMenu.value && !(event.target as HTMLElement).closest('.user-profile')) {
    showProfileMenu.value = false;
  }
}

function goTo(path: string) {
  router.push(path);
}

function logout() {
  localStorage.removeItem("token");
  delete axios.defaults.headers.common['Authorization'];
  router.push("/login");
}

const submitForm = async () => {
  errors.value = {};

  if (!form.value.employee) errors.value.employee = 'กรุณาเลือกผู้ปฏิบัติงาน';
  if (!form.value.startDate) errors.value.startDate = 'กรุณาเลือกวันที่เริ่มต้น';
  if (!form.value.endDate) errors.value.endDate = 'กรุณาเลือกวันที่สิ้นสุด';
  if (!form.value.period) errors.value.period = 'กรุณาเลือกช่วงเวลา';
  if (!form.value.reason) errors.value.reason = 'กรุณาระบุเหตุผล';
  if (!form.value.location) errors.value.location = 'กรุณาระบุสถานที่';
  if (!form.value.approver) errors.value.approver = 'กรุณาเลือกหัวหน้างาน';
  if (form.value.startDate && form.value.endDate && form.value.startDate > form.value.endDate) {
    errors.value.endDate = 'วันที่สิ้นสุดต้องไม่มาก่อนวันที่เริ่มต้น';
  }
  if (form.value.employee && form.value.approver && form.value.employee === form.value.approver) {
    errors.value.approver = 'ผู้ปฏิบัติงานและผู้อนุมัติต้องไม่เป็นคนเดียวกัน';
  }

  if (Object.keys(errors.value).length > 0) {
    return;
  }

  try {
    const response = await axios.post("http://localhost:8000/api/work-from-outside/requests/proxy/", {
      user: form.value.employee,
      collaborators: form.value.collaborators,
      start_date: form.value.startDate,
      end_date: form.value.endDate,
      time_period: form.value.period === 'ทั้งวัน' ? 'full' : form.value.period === 'ครึ่งวันเช้า' ? 'morning' : 'afternoon',
      reason: form.value.reason,
      location: form.value.location,
      approver: form.value.approver,
      proxy_user: user.value.id
    });
    console.log('ส่งฟอร์มสำเร็จ:', response.data);
    alert('ส่งคำขอสำเร็จ!');
    router.push('/user7');
  } catch (err) {
    console.error('เกิดข้อผิดพลาด:', err);
    if (err.response?.data?.detail) {
      alert(`เกิดข้อผิดพลาด: ${err.response.data.detail}`);
    } else {
      alert('เกิดข้อผิดพลาดในการส่งคำขอ');
    }
  }
};

const cancelForm = () => {
  console.log('ยกเลิกฟอร์ม');
  router.push('/user');
};


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

.leave-form-container {
  background-color: #ffffff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-header {
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

.form-header h3 {
  margin: 0;
  font-size: 22px;
}

.note {
  font-size: 14px;
  color: #888;
  margin: 5px 0 0;
}

.btn-cancel {
  background: #f1f1f1;
  color: #e74c3c;
  padding: 8px 14px;
  border: 1px solid #e74c3c;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  font-weight: bold;
}

.btn-cancel i {
  margin-right: 5px;
}

.user-info-section {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.user-label {
  font-weight: bold;
  margin-right: 10px;
}

.user-name {
  color: #555;
}

.leave-form {
  padding: 0;
}

.form-row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 15px;
}

.form-group {
  flex: 1 1 45%;
  display: flex;
  flex-direction: column;
}

.form-group-dates {
  flex: 1 1 45%;
  display: flex;
  align-items: center;
  gap: 10px;
}

.form-group label {
  font-weight: bold;
  margin-bottom: 5px;
}

.radio-group {
  display: flex;
  gap: 20px;
}

.text-input,
.select-input,
.date-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 14px;
}

.date-input {
  flex: 1;
}

.form-group-dates label {
  flex-shrink: 0;
  font-weight: bold;
}

.form-group.full-width {
  flex: 1 1 100%;
}

.form-buttons-bottom {
  display: flex;
  justify-content: flex-end;
  margin-top: 30px;
}

.btn-submit {
  background: #4caf50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}
</style>