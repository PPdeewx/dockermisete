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
                <label for="requester">ผู้ปฏิบัติงาน *: <span class="required">*</span></label>
                <AutoComplete
                  id="requester"
                  v-model="form.requester"
                  :suggestions="filteredEmployees"
                  @complete="searchEmployees"
                  optionLabel="name"
                  placeholder="ค้นหาพนักงาน..."
                  :dropdown="true"
                  required
                />
              </div>
          </div>

          <div class="form-row">
            <div class="form-group full-width">
              <div class="member-selection-section" v-if="!loading">
                <div class="section-header">
                  <h3>ผู้ร่วมปฏิบัติงาน (Optional)</h3>
                </div>
                <div class="member-selection-container">
                  <div class="member-list">
                    <div class="list-title">
                      พนักงานทั้งหมด ({{ unassignedEmployees.length }} คน)
                    </div>
                    <AutoComplete
                      v-model="selectedEmployeeToAssign"
                      :suggestions="filteredUnassigned"
                      @complete="searchUnassigned"
                      optionLabel="name"
                      placeholder="ค้นหาพนักงาน..."
                      :dropdown="true"
                      class="form-input"
                    />
                  </div>

                  <div class="action-buttons">
                    <button class="btn-action-move" type="button" @click="assignSelected">
                      <i class="fas fa-angle-right"></i>
                    </button>
                    <button class="btn-action-move" type="button" @click="unassignSelected">
                      <i class="fas fa-angle-left"></i>
                    </button>
                  </div>

                  <div class="member-list">
                    <div class="list-title">
                      ผู้ร่วมปฏิบัติงาน ({{ assignedEmployees.length }} คน)
                    </div>
                    <AutoComplete
                      v-model="selectedEmployeeToUnassign"
                      :suggestions="filteredAssigned"
                      @complete="searchAssigned"
                      optionLabel="name"
                      placeholder="ค้นหาพนักงาน..."
                      :dropdown="true"
                      class="form-input"
                    />
                  </div>
                </div>
              </div>
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
              <label>หัวหน้างาน <span class="required">*</span></label>
              <AutoComplete
                v-model="form.approver"
                :suggestions="filteredSupervisors"
                @complete="searchSupervisor"
                optionLabel="name"
                placeholder="เลือกหัวหน้างาน..."
                :dropdown="true"
                class="form-input"
              />
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
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

import TopBar from '~/components/Topbar.vue';

const router = useRouter();
const user = ref<any>(null);

const employees = ref<any[]>([]);
const supervisorList = ref<any[]>([]);
const filteredSupervisors = ref<any[]>([]);
const filteredEmployees = ref<any[]>([]);

const unassignedEmployees = ref<any[]>([]);
const assignedEmployees = ref<any[]>([]);
const selectedEmployeeToAssign = ref<any>(null);
const selectedEmployeeToUnassign = ref<any>(null);
const filteredUnassigned = ref<any[]>([]);
const filteredAssigned = ref<any[]>([]);

const selectedSupervisor = ref<any>(null);

const errors = ref<any>({});

const form = ref({
  requester: null,        // จะเก็บ object ของผู้ปฏิบัติงาน
  startDate: '',
  endDate: '',
  period: 'ทั้งวัน',
  reason: '',
  location: '',
  approver: null          // จะเก็บ object ของหัวหน้างาน
});

// ฟังก์ชันค้นหา
const searchEmployees = (event: { query: string }) => {
  const query = event.query.toLowerCase();
  filteredEmployees.value = employees.value.filter(emp =>
    emp.name.toLowerCase().includes(query)
  );
};

const searchSupervisor = (event: { query: string }) => {
  const query = event.query.toLowerCase();
  filteredSupervisors.value = supervisorList.value.filter(s =>
    s.name.toLowerCase().includes(query)
  );
};

const searchUnassigned = (event: { query: string }) => {
  const query = event.query.toLowerCase();
  filteredUnassigned.value = unassignedEmployees.value.filter(emp =>
    emp.name.toLowerCase().includes(query)
  );
};
const searchAssigned = (event: { query: string }) => {
  const query = event.query.toLowerCase();
  filteredAssigned.value = assignedEmployees.value.filter(emp =>
    emp.name.toLowerCase().includes(query)
  );
};

// ฟังก์ชันย้ายพนักงาน
const assignSelected = () => {
  if (selectedEmployeeToAssign.value) {
    const emp = selectedEmployeeToAssign.value;
    assignedEmployees.value.push(emp);
    unassignedEmployees.value = unassignedEmployees.value.filter(e => e.id !== emp.id);
    selectedEmployeeToAssign.value = null;
  }
};
const unassignSelected = () => {
  if (selectedEmployeeToUnassign.value) {
    const emp = selectedEmployeeToUnassign.value;
    unassignedEmployees.value.push(emp);
    assignedEmployees.value = assignedEmployees.value.filter(e => e.id !== emp.id);
    selectedEmployeeToUnassign.value = null;
  }
};

// โหลดข้อมูลเมื่อหน้า mount
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

    const employeesResponse = await axios.get("http://localhost:8000/api/users/for-list/");
    employees.value = employeesResponse.data.filter((u: any) => !u.groups.includes("บุคลากรภายนอก"));

    const resEmployees = await axios.get("http://localhost:8000/api/users/?role=employee");
    unassignedEmployees.value = resEmployees.data
      .filter((u: any) => !u.groups.includes("บุคลากรภายนอก"))
      .map((u: any) => ({
        id: u.id,
        name: `${u.firstname_th} ${u.lastname_th}`.trim()
      }));

    const resDept = await axios.get("http://localhost:8000/api/users/departments/");
    supervisorList.value = resDept.data.flatMap((dept: any) =>
      dept.approvers.map((a: any) => ({
        id: a.id,
        name: `${a.firstname_th} ${a.lastname_th}`.trim()
      }))
    );

  } catch (err) {
    console.error('Error fetching data:', err);
    alert('เกิดข้อผิดพลาดในการโหลดข้อมูล');
    router.push("/login");
  }
});

// Submit form
const submitForm = async () => {
  errors.value = {};

  if (!form.value.requester) errors.value.requester = 'กรุณาเลือกผู้ปฏิบัติงาน';
  if (!form.value.startDate) errors.value.startDate = 'กรุณาเลือกวันที่เริ่มต้น';
  if (!form.value.endDate) errors.value.endDate = 'กรุณาเลือกวันที่สิ้นสุด';
  if (!form.value.period) errors.value.period = 'กรุณาเลือกช่วงเวลา';
  if (!form.value.reason) errors.value.reason = 'กรุณาระบุเหตุผล';
  if (!form.value.location) errors.value.location = 'กรุณาระบุสถานที่';
  if (!form.value.approver) errors.value.approver = 'กรุณาเลือกหัวหน้างาน';

  if (Object.keys(errors.value).length > 0) return;

  try {
    const payload = {
      user: form.value.requester.id, // ส่ง ID ของ requester
      collaborators: assignedEmployees.value.map(e => e.id), // ส่ง list ของ ID
      start_date: form.value.startDate,
      end_date: form.value.endDate,
      time_period: form.value.period === 'ทั้งวัน' ? 'full' : form.value.period === 'ครึ่งวันเช้า' ? 'morning' : 'afternoon',
      reason: form.value.reason,
      location: form.value.location,
      approver: form.value.approver.id, // ส่ง ID ของ approver
      proxy_user: user.value.id
    };

    const response = await axios.post(
      "http://localhost:8000/api/work-from-outside/requests/proxy/",
      payload
    );
    console.log("Payload ก่อนส่ง:", payload);
    console.log('ส่งฟอร์มสำเร็จ:', response.data);
    alert('ส่งคำขอสำเร็จ!');
    router.push('/user');
  } catch (err: any) {
    console.error('เกิดข้อผิดพลาด:', err.response?.data || err);
    alert('เกิดข้อผิดพลาดในการส่งคำขอ: ' + JSON.stringify(err.response?.data));
  }
};

const cancelForm = () => {
  router.push('/user');
};
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

.read-only-text { background: #f4f4f4; padding: 6px; border-radius: 4px; }
.selected-list { margin-top: 5px; padding-left: 20px; }
.form-actions { margin-top: 20px; }
</style>