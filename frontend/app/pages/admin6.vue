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
            <li><a href="#" class="submenu-link active">เพิ่ม/แก้ไข/ลบ พนักงาน</a></li>
            <li><a href="#" class="submenu-link">เพิ่มบุคลากรภายนอก</a></li>
            <li><a href="#" class="submenu-link">เปลี่ยนสถานะพนักงาน</a></li>
            <li><a href="#" class="submenu-link">กำหนดโควต้าลา(ทั้งหมด)</a></li>
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
          <span><i class="fas fa-home"></i> หน้าหลัก > บุคลากร > เพิ่ม/แก้ไข พนักงาน</span>
        </div>
        <div class="user-profile-container">
          <div class="user-profile" @click="toggleProfileMenu">
            <i class="fas fa-bell"></i>
            <i class="fas fa-user-circle"></i>
            <span class="username">{{ currentUser?.username }} ตำแหน่ง: {{ currentUser?.role }}</span>
            <i :class="['fas', showProfileMenu ? 'fa-chevron-up' : 'fa-chevron-down']"></i>

            <div class="user-profile-menu" v-if="showProfileMenu">
              <button class="menu-item" @click.stop="goTo('/admin')">
                <i class="fas fa-user"></i>
                <span>ดูข้อมูลส่วนตัว</span>
              </button>
              <button class="menu-item" @click.stop="goTo('/admin')">
                <i class="fas fa-edit"></i>
                <span>แก้ไขข้อมูลส่วนตัว</span>
              </button>
              <button class="menu-item" @click.stop="goTo('/admin')">
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
        <div class="form-header">
          <h2>เพิ่ม / แก้ไข พนักงาน</h2>
          <button class="btn-cancel" @click.prevent="cancelForm">
            <i class="fas fa-times"></i> ยกเลิก
          </button>
        </div>
        <form @submit.prevent="submitForm">
          <div class="form-group-container">
            <div class="form-group">
              <label for="username">Username *</label>
              <input type="text" id="username" v-model="form.username" required />
            </div>
            <div class="form-group">
              <label for="password">Password *</label>
              <input type="password" id="password" v-model="form.password" required />
            </div>
            <div class="form-group">
              <label for="confirm-password">Phone *</label>
              <input type="phone" id="phone" v-model="form.phone" required/>
            </div>
            <div class="form-group">
              <label for="email">Email *</label>
              <input type="email" id="email" v-model="form.email" required />
            </div>
            <div class="form-group">
              <label for="emp-code">EMP Code *</label>
              <input type="text" id="emp-code" v-model="form.empCode" required />
            </div>
             <div class="form-group">
              <label for="taf-code">TAF Code *</label>
              <input type="text" id="taf-code" v-model="form.tafCode" required />
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="thai-name-prefix">คำนำหน้าชื่อไทย *</label>
              <select id="thai-name-prefix" v-model="form.thaiNamePrefix" required>
                <option value="">กรุณาเลือก</option>
                <option v-for="prefix in thaiNamePrefixOptions" :key="prefix" :value="prefix">
                  {{ prefix }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label for="thai-name">ชื่อภาษาไทย *</label>
              <input type="text" id="thai-name" v-model="form.thaiName" required />
            </div>
            <div class="form-group">
              <label for="thai-surname">นามสกุลภาษาไทย *</label>
              <input type="text" id="thai-surname" v-model="form.thaiSurname" required />
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="english-name-prefix">คำนำหน้าชื่ออังกฤษ *</label>
              <select id="english-name-prefix" v-model="form.englishNamePrefix">
                <option value="">กรุณาเลือก</option>
                <option v-for="prefix in englishNamePrefixOptions" :key="prefix" :value="prefix">
                  {{ prefix }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label for="english-name">ชื่อภาษาอังกฤษ *</label>
              <input type="text" id="english-name" v-model="form.englishName"/>
            </div>
            <div class="form-group">
              <label for="english-surname">นามสกุลภาษาอังกฤษ *</label>
              <input type="text" id="english-surname" v-model="form.englishSurname"/>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="position">ที่อยุ่ *</label>
              <input type="text" id="position" v-model="form.position"/>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="employment-type">ประเภทการจ้างงาน *</label>
              <select id="employment-type" v-model="form.group" required>
                <option value="">กรุณาเลือก</option>
                <option v-for="group in groupOptions" :key="group.value" :value="group.value">
                  {{ group.label }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label for="room">ห้องวิจัย *</label>
              <select id="room" v-model="form.room">
                <option value="">เลือกห้องวิจัย</option>
                <option v-for="room in roomOptions" :key="room" :value="room">
                  {{ room }}
                </option>
              </select>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="personnel-type">สถานะ *</label>
              <select id="personnel-type" v-model="form.status" required>
                <option value="">กรุณาเลือก</option>
                <option v-for="status in statusOptions" :key="status.value" :value="status.value">
                  {{ status.label }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>ระดับผู้ใช้ *</label>
              <div class="radio-group">
                <label><input type="radio" name="user-level" value="admin" v-model="form.userLevel" /> Admin</label>
                <label><input type="radio" name="user-level" value="employee" v-model="form.userLevel" /> User</label>
              </div>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="start-date">วันที่เริ่มทำงาน *</label>
              <input type="date" id="start-date" v-model="form.startDate" required />
            </div>
          </div>


          <p class="small-text">กรณีเป็นหัวหน้าพนักงาน</p>

          <div class="form-row">
            <div class="form-group">
              <label for="vacation-leave">สิทธิลาพักร้อน (วัน) :</label>
              <input type="number" id="vacation-leave" v-model="form.vacationLeave" />
            </div>
            <div class="form-group">
              <label for="sick-leave">สิทธิลาป่วย (วัน) :</label>
              <input type="number" id="sick-leave" v-model="form.sickLeave" />
            </div>
            <div class="form-group">
              <label for="personal-leave">สิทธิลากิจ (วัน) :</label>
              <input type="number" id="personal-leave" v-model="form.personalLeave" />
            </div>
            <div class="form-group">
              <label for="other-leave">สิทธิลาอื่นๆ (วัน) :</label>
              <input type="number" id="other-leave" v-model="form.otherLeave" />
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-submit">บันทึกข้อมูล</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const thaiNamePrefixOptions = ['นาย', 'นาง', 'นางสาว']
const englishNamePrefixOptions = ['Mr.', 'Mrs.', 'Ms.', 'Dr.']

const roomOptions = ref<string[]>([])

const groupOptions = [
  { value: 'regular', label: 'พนักงานประจำ' },
  { value: 'manager', label: 'ผู้บริหาร' },
  { value: 'temporary', label: 'พนักงานชั่วคราว' },
  { value: 'developer', label: 'Developer' },
]

const statusOptions = [
  { value: 'active', label: 'พนักงานปัจจุบัน' },
  { value: 'resigned', label: 'ลาออก' },
]

const departments = ref<any[]>([])

const router = useRouter()
const route = useRoute()

const currentUser = ref<any>(null)

const token = ref<string | null>(null);
const showProfileMenu = ref(false)
const toggleProfileMenu = () => {
  showProfileMenu.value = !showProfileMenu.value
}

const form = reactive({
  id: null,
  username: '',
  password: '',
  phone: '',
  email: '',
  empCode: '',
  tafCode: '', 
  thaiNamePrefix: '',
  thaiName: '',
  thaiSurname: '',
  englishNamePrefix: '',
  englishName: '',
  englishSurname: '',
  room: '', 
  position: '',
  group: '',
  status: '',
  userLevel: 'user', 
  startDate: '',
  initialLeave: 'yes',
  vacationLeave: 5.0,
  sickLeave: 30.0,
  personalLeave: 10.0,
  otherLeave: 0.0,
})


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
    currentUser.value = me.data

    if (currentUser.value.role !== 'admin') {
      router.push('/login')
      return
    }
  } catch (err) {
    console.error(err)
    router.push('/login')
  }

  try {
    const res = await axios.get('http://localhost:8000/api/users/departments/')
    const departmentsData = res.data
    roomOptions.value = departmentsData.map((d: any) => `${d.name_th}`)
  } catch (err) {
    console.error("Failed to load departments:", err)
  }

  if (route.params.id) {
    const res = await axios.get(`http://localhost:8000/api/users/${route.params.id}/`)
    const user = res.data
    form.id = user.id
    form.username = user.username
    form.phone = user.phone_number
    form.email = user.email
    form.empCode = user.employee_code
    form.tafCode = user.time_attendance_code
    form.thaiNamePrefix = user.prefix_th
    form.thaiName = user.firstname_th
    form.thaiSurname = user.lastname_th
    form.englishNamePrefix = user.prefix_en
    form.englishName = user.firstname_en
    form.englishSurname = user.lastname_en
    form.room = user.department ? `${user.department.name_th}` : ''
    form.userLevel = user.role
    form.startDate = user.start_date
    form.vacationLeave = user.quota_vacation
    form.sickLeave = user.quota_sick
    form.personalLeave = user.quota_casual
  }
})

const submitForm = async () => {
  if (form.password && form.password) {
    alert('รหัสผ่านไม่ถูกต้อง')
    return
  }

  const payload = {
    username: form.username,
    employee_code: form.empCode,
    time_attendance_code: form.tafCode,
    prefix_th: form.thaiNamePrefix,
    firstname_th: form.thaiName,
    lastname_th: form.thaiSurname,
    prefix_en: form.englishNamePrefix,
    firstname_en: form.englishName,
    lastname_en: form.englishSurname,
    phone_number: form.phone,
    email: form.email,
    department: form.room || null,
    role: form.userLevel,                    
    group: form.group,  
    start_date: form.startDate,
    quota_vacation: form.vacationLeave,
    quota_sick: form.sickLeave,
    quota_casual: form.personalLeave,
    status: form.status,
    password: form.password || undefined, 
  }

  try {
    if (form.id) {
      
      await axios.put(`http://localhost:8000/api/users/${form.id}/`, payload)
      alert("อัปเดตข้อมูลสำเร็จ")
    } else {
      
      await axios.post('http://localhost:8000/api/users/create/', payload)
      alert("เพิ่มพนักงานสำเร็จ")
    }
    router.push('/admin2') 
  } catch (err: any) {
    console.error(err.response?.data || err)
    alert("เกิดข้อผิดพลาด")
  }
}

const cancelForm = () => {
  router.push('/admin2')
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
  width: 280px;
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

.form-group-container,
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

.radio-group {
  display: flex;
  gap: 15px;
  align-items: center;
  flex-wrap: wrap;
}

.radio-group label {
  font-weight: normal;
  display: flex;
  align-items: center;
  gap: 5px;
}

.small-text {
  font-size: 0.9em;
  color: #888;
  margin-bottom: 10px;
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