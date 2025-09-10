<template>
  <div class="full-page-container">
    <div class="sidebar">
      <div class="sidebar-header">
        <span>MIS ETE</span>
      </div>
      <ul class="nav-menu">
        <li class="nav-item">
          <a href="#" class="nav-link"><i class="fas fa-home"></i> หน้าหลัก</a>
        </li>
        <li class="nav-item has-submenu active">
          <a href="#" class="nav-link"><i class="fas fa-users"></i> บุคลากร</a>
          <ul class="submenu active">
            <li><a href="#" class="submenu-link">พนักงานปัจจุบัน</a></li>
            <li><a href="#" class="submenu-link">พนักงานที่ลาออก</a></li>
            <li><a href="#" class="submenu-link">บุคลากรภายนอก</a></li>
            <li><a href="#" class="submenu-link">พนักงาน EDDP</a></li>
            <li><a href="#" class="submenu-link">เพิ่ม/แก้ไข/ลบ พนักงาน</a></li>
            <li><a href="#" class="submenu-link">เพิ่มบุคลากรภายนอก</a></li>
            <li><a href="#" class="submenu-link">เปลี่ยนสถานะพนักงาน</a></li>
            <li><a href="#" class="submenu-link active">กำหนดโควต้าลา(ทั้งหมด)</a></li>
          </ul>
        </li>
        <li class="nav-item"><a href="#" class="nav-link"><i class="fas fa-flask"></i> ห้องวิจัย</a></li>
        <li class="nav-item"><a href="#" class="nav-link"><i class="fas fa-calendar-alt"></i> วันหยุด</a></li>
        <li class="nav-item"><a href="#" class="nav-link"><i class="fas fa-cog"></i> ระบบการปฏิบัติงาน</a></li>
      </ul>
    </div>

    <div class="main-content">
      <div class="top-bar">
        <div class="breadcrumbs">
          <span><i class="fas fa-home"></i> หน้าหลัก > บุคลากร > กำหนดโควต้าลา(ทั้งหมด)</span>
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
        <div class="quota-controls">
          <div class="filter-group">
            <div class="filter-item">
              <label for="status-filter">สถานะพนักงาน</label>
              <select id="status-filter" v-model="filter.status">
                <option value="ทั้งหมด">ทั้งหมด</option>
                <option value="active">พนักงานปัจจุบัน</option>
                <option value="resigned">พนักงานที่ลาออก</option>
              </select>
            </div>
            <div class="filter-item">
              <label for="department-filter">ห้องวิจัย</label>
              <select id="department-filter" v-model="filter.department">
                <option value="ทั้งหมด">ทั้งหมด</option>
                <option v-for="dept in departments" :key="dept.id" :value="dept.id">{{ dept.name_th }}</option>
              </select>
            </div>
            <div class="filter-item">
              <label for="search-name">ค้นหา</label>
              <input type="text" id="search-name" v-model="filter.search" placeholder="ค้นหาชื่อ" />
            </div>
          </div>
        </div>

        <div class="table-responsive">
          <table>
            <thead>
              <tr>
                <th>ลำดับที่</th>
                <th>ชื่อ-นามสกุล</th>
                <th>สถานะพนักงาน</th>
                <th>ห้องวิจัย</th>
                <th v-for="type in leaveTypes" :key="type.id">{{ type.name }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(emp, index) in filteredEmployees" :key="emp.id">
                <td>{{ index + 1 }}</td>
                <td>{{ emp.firstname_th }} {{ emp.lastname_th }}</td>
                <td>{{ emp.status === 'active' ? 'พนักงานปัจจุบัน' : 'พนักงานที่ลาออก' }}</td>
                <td>{{ emp.department?.name_th }}</td>
                <td v-for="type in leaveTypes" :key="type.id">
                  <input
                    type="number"
                    :value="quotas[emp.id]?.[type.id] ?? 0"
                    @input="onQuotaChange(emp.id, type.id, $event.target.value)"
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="form-actions">
          <button class="btn-submit" @click="saveQuotaChanges">บันทึกข้อมูล</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const token = ref<string | null>(null)

const currentUser = ref<any>(null)
const showProfileMenu = ref(false)
const toggleProfileMenu = () => { showProfileMenu.value = !showProfileMenu.value }

const filter = reactive({
  status: 'ทั้งหมด',
  department: 'ทั้งหมด',
  search: ''
})

const departments = ref([])
const leaveTypes = ref([])
const employees = ref([])

const quotas = reactive<{ [userId: number]: { [leaveTypeId: number]: number } }>({})

const filteredEmployees = computed(() => {
  return employees.value.filter(emp => {
    const statusMatch = filter.status === 'ทั้งหมด' || emp.status === filter.status
    const deptMatch = filter.department === 'ทั้งหมด' || emp.department?.id === Number(filter.department)
    const searchMatch = emp.firstname_th.toLowerCase().includes(filter.search.toLowerCase()) ||
                        emp.lastname_th.toLowerCase().includes(filter.search.toLowerCase())
    return statusMatch && deptMatch && searchMatch
  })
})

onMounted(async () => {
  if (typeof window !== "undefined") token.value = localStorage.getItem("token")
  if (!token.value) { router.push('/login'); return }

  axios.defaults.headers.common['Authorization'] = `Token ${token.value}`

  try {
    const me = await axios.get('http://localhost:8000/api/users/me/')
    currentUser.value = me.data
    if (currentUser.value.role !== 'admin') router.push('/login')
  } catch (err) {
    console.error(err)
    router.push('/login')
  }

  const resUsers = await axios.get('http://localhost:8000/api/users/')
  employees.value = resUsers.data

  const resTypes = await axios.get('http://localhost:8000/api/leave/leave-types/')
  leaveTypes.value = resTypes.data

  const resQuotas = await axios.get('http://localhost:8000/api/leave/leave-quotas/')
  resQuotas.data.forEach((q: any) => {
    const userId = q.user.id || q.user
    const leaveTypeId = q.leave_type.id || q.leave_type
    if (!quotas[userId]) quotas[userId] = {}
    quotas[userId][leaveTypeId] = q.quota_total
  })

  const resDept = await axios.get('http://localhost:8000/api/users/departments/')
  departments.value = resDept.data
})

const onQuotaChange = (userId: number, typeId: number, value: number) => {
  if (!quotas[userId]) quotas[userId] = {}
  quotas[userId][typeId] = Number(value)
}

const saveQuotaChanges = async () => {
  const payload: any[] = []
  for (const userId in quotas) {
    for (const typeId in quotas[userId]) {
      payload.push({
        user: parseInt(userId),
        leave_type: parseInt(typeId),
        quota_total: quotas[userId][typeId],
        year: new Date().getFullYear()
      })
    }
  }
  try {
    await axios.post('http://localhost:8000/api/leave/leave-quotas/bulk_update/', payload)
    alert('บันทึกข้อมูลเรียบร้อย')
  } catch (err) {
    console.error(err)
    alert('เกิดข้อผิดพลาด')
  }
}

function logout() {
  if (typeof window !== "undefined") localStorage.removeItem("token")
  delete axios.defaults.headers.common['Authorization']
  router.push("/login")
}

function goTo(path: string) {
  router.push(path)
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
  width: 300px;
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

.quota-controls {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 20px;
}

.filter-group {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.filter-item {
  display: flex;
  flex-direction: column;
}

.filter-item label {
  font-weight: bold;
  margin-bottom: 5px;
}

.filter-item select,
.filter-item input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.quota-default {
  display: flex;
  align-items: flex-end;
  gap: 10px;
}

.quota-default span {
  font-weight: bold;
  margin-right: 5px;
}

.quota-default input {
  width: 80px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center;
}

.btn-default {
  padding: 8px 15px;
  border-radius: 5px;
  background-color: #1890ff;
  color: white;
  border: none;
  cursor: pointer;
  white-space: nowrap;
}

.table-responsive {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

thead th {
  background-color: #f5f5f5;
  padding: 12px;
  text-align: left;
  border-bottom: 2px solid #ddd;
}

tbody td {
  padding: 12px;
  border-bottom: 1px solid #eee;
}

tbody tr:hover {
  background-color: #fafafa;
}

tbody input[type="number"] {
  width: 80px;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center;
}

.form-actions {
  margin-top: 30px;
  text-align: center;
}

.btn-submit {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.2s;
}

.btn-submit:hover {
  background-color: #45a049;
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