<template>
  <div class="full-page-container">
    <main class="main-content">
      <TopBar />

      <div class="leave-form-container">
        <div class="form-header">
          <div class="header-left">
            <i class="fas fa-file-alt icon-red"></i>
            <div><h3>ระบบการยื่นใบลาแทนคนอื่น</h3></div>
          </div>
          <button type="button" class="btn-cancel" @click="cancelForm">
            <i class="fas fa-times-circle"></i> ยกเลิก
          </button>
        </div>

        <div class="user-info-section">
          <span class="user-label">พนักงานผู้ลาแทน :</span>
          <span class="user-name">{{ user?.prefix_th }} {{ user?.firstname_th }} {{ user?.lastname_th }}</span>
        </div>

        <form @submit.prevent="submitForm" class="leave-form">
          <div class="form-row">
            <div class="form-group full-width">
              <label for="employee-name">พนักงานผู้ลา *</label>
              <AutoComplete
                id="employee-name"
                v-model="form.employee"
                :suggestions="filteredEmployees"
                @complete="searchEmployees"
                optionLabel="name"
                placeholder="ค้นหาพนักงานผู้ลา..."
                :dropdown="true"
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group full-width">
              <label>ประเภทการลา *</label>
              <div class="radio-group">
                <label v-for="type in leaveTypes" :key="type.id">
                  <input type="radio" :value="type.id" v-model="form.leaveTypeId" />
                  {{ type.name }}
                </label>
              </div>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group-dates">
              <label>ลาตั้งแต่วันที่ *:</label>
              <input type="date" v-model="form.startDate" class="date-input" />
            </div>
            <div class="form-group-dates">
              <label>ถึงวันที่ *:</label>
              <input type="date" v-model="form.endDate" class="date-input" />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group full-width">
              <label>ช่วงเวลาการลา *</label>
              <div class="radio-group">
                <label v-for="(label, key) in HALF_CHOICES" :key="key">
                  <input type="radio" :value="key" v-model="form.period" /> {{ label }}
                </label>
              </div>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group full-width">
              <label>เหตุผลการลา *:</label>
              <input type="text" v-model="form.reason" class="text-input" />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group full-width">
              <label for="approver">ผู้อนุมัติการลา *</label>
              <AutoComplete
                id="approver"
                v-model="form.approver"
                :suggestions="filteredApprovers"
                @complete="searchApprovers"
                optionLabel="name"
                placeholder="ค้นหาหัวหน้างาน..."
                :dropdown="true"
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group full-width">
              <label for="substitute">ผู้ปฏิบัติงานแทน *</label>
              <AutoComplete
                id="substitute"
                v-model="form.substitute"
                :suggestions="filteredSubstitutes"
                @complete="searchSubstitutes"
                optionLabel="name"
                placeholder="ค้นหาผู้ปฏิบัติงานแทน..."
                :dropdown="true"
              />
            </div>
          </div>

          <div class="form-buttons-bottom">
            <button type="submit" class="btn-submit">ขออนุมัติลา</button>
          </div>
        </form>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import TopBar from '~/components/Topbar.vue'

const HALF_CHOICES: Record<string, string> = {
  full: 'ทั้งวัน',
  morning: 'ครึ่งเช้า',
  afternoon: 'ครึ่งบ่าย'
}

const router = useRouter()
const user = ref<any>(null)

const form = ref({
  employee: null,
  leaveTypeId: '',
  startDate: '',
  endDate: '',
  period: 'full',
  reason: '',
  approver: null,
  substitute: null
})

const employeeList = ref<any[]>([])
const approverList = ref<any[]>([])
const substituteList = ref<any[]>([])
const leaveTypes = ref<any[]>([])

const filteredEmployees = ref<any[]>([])
const filteredApprovers = ref<any[]>([])
const filteredSubstitutes = ref<any[]>([])

const searchEmployees = (event: any) => {
  const query = event.query.toLowerCase()
  filteredEmployees.value = employeeList.value.filter((u) =>
    u.name.toLowerCase().includes(query)
  )
}
const searchApprovers = (event: any) => {
  const query = event.query.toLowerCase()
  filteredApprovers.value = approverList.value.filter((u) =>
    u.name.toLowerCase().includes(query)
  )
}
const searchSubstitutes = (event: any) => {
  const query = event.query.toLowerCase()
  filteredSubstitutes.value = substituteList.value.filter((u) =>
    u.name.toLowerCase().includes(query)
  )
}

const loadUsers = async () => {
  const usersResponse = await axios.get('http://localhost:8000/api/users/for-list/')
  const users = usersResponse.data

  const internalUsers = users.filter((u: any) => !u.is_external)

  employeeList.value = internalUsers.filter((u: any) => u.id !== user.value?.id)

  approverList.value = internalUsers.filter(
    (u: any) => u.role === 'admin' || u.groups.includes('ผู้บริหาร')
  )

  substituteList.value = internalUsers.filter((u: any) => u.id !== user.value?.id )
}

const loadLeaveTypes = async () => {
  const response = await axios.get('http://localhost:8000/api/leave/leave-types/')
  leaveTypes.value = response.data
}

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    router.push('/login')
    return
  }
  axios.defaults.headers.common['Authorization'] = `Token ${token}`

  const me = await axios.get('http://localhost:8000/api/users/me/')
  user.value = me.data

  await Promise.all([loadUsers(), loadLeaveTypes()])
})

const submitForm = async () => {
  const payload = {
    on_behalf_of_id: form.value.employee?.id,
    leave_type_id: form.value.leaveTypeId,
    start_date: form.value.startDate,
    end_date: form.value.endDate,
    period: form.value.period,
    reason: form.value.reason,
    approver_id: form.value.approver?.id,
    substitute_id: form.value.substitute?.id || null
  }

  if (!payload.on_behalf_of_id || !payload.leave_type_id || !payload.start_date || !payload.end_date || !payload.reason || !payload.approver_id) {
    alert('กรุณากรอกข้อมูลให้ครบ')
    return
  }

  await axios.post('http://localhost:8000/api/leave/leave-requests/', payload)
  alert('ส่งคำขอลาสำเร็จ!')
  router.push('/user/leave-history')
}

const cancelForm = () => router.push('/user')
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