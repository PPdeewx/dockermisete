<template>
  <div class="full-page-container">
    <main class="main-content">
      <TopBar>
        <template #breadcrumbs>หน้าหลัก</template>
      </TopBar>

      <div class="dashboard-container">
        <div class="card-left">
          <div class="card">
            <div class="card-header">
              <i class="fas fa-scroll icon-blue"></i>
              <h4>ประกาศล่าสุด</h4>
            </div>
            <div class="card-body">
              <div class="timeline">
                <div
                  class="timeline-item"
                  v-for="(announcement, index) in announcements"
                  :key="index"
                >
                  <div class="timeline-content">
                    <h5 class="timeline-title">{{ announcement.title }}</h5>
                    <p class="timeline-text">{{ announcement.text }}</p>
                    <span class="timeline-date">{{ announcement.date }}</span>
                  </div>
                  <div class="timeline-indicator">
                    <span class="timeline-time">{{ announcement.time }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="card-right">
          <div class="card">
            <div class="card-header">
              <i class="fas fa-users icon-blue"></i>
              <h4>พนักงานปฏิบัติงานวันนี้</h4>
            </div>
            <div class="card-body-center">
              <div class="donut-chart-container">
                <div
                  class="donut-chart"
                  :style="`--p: ${todayWorkingCount}; --c: #a54687; --b: 10px;`"
                >
                  <span class="donut-label">{{ todayWorkingCount }}</span>
                </div>
              </div>
              <p class="donut-sublabel">{{ todayLabel }}</p>
            </div>
          </div>

          <div class="card">
            <div class="card-header">
              <i class="fas fa-exclamation-triangle icon-yellow"></i>
              <h4>สถิติการลาสายของท่านในปีนี้</h4>
            </div>
            <div class="card-body-center">
              <div class="alert-box">
                <i class="fas fa-exclamation-triangle"></i>
                <p>{{ lateStats.minutes }} นาที / {{ lateStats.fines }} บาท</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="table-card">
        <div class="card-header">
          <i class="fas fa-calendar-times icon-red"></i>
          <h4>คำนวณการลาและทำงานนอกสถานที่ของท่าน 15 วันต่อจากนี้</h4>
        </div>
        <div class="card-body">
          <div class="responsive-table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>วันที่</th>
                  <th>ประเภท</th>
                  <th>ช่วงเวลา</th>
                  <th>สถานะ</th>
                  <th>เหตุผล</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in upcomingActivities" :key="index">
                  <td>{{ item.date }}</td>
                  <td>{{ item.type }}</td>
                  <td>{{ item.period }}</td>
                  <td>{{ item.status }}</td>
                  <td>{{ item.reason }}</td>
                </tr>
                <tr v-if="upcomingActivities.length === 0">
                  <td colspan="5">ไม่มีข้อมูล</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import TopBar from '~/components/Topbar.vue'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const token = ref<string | null>(null)
const user = ref<any>(null)

const todayWorkingCount = ref(0)
const lateStats = ref({ minutes: 0, fines: 0 })
const upcomingActivities = ref<any[]>([])
const todayLabel = ref(new Date().toLocaleDateString('th-TH',{weekday:'short', day:'numeric', month:'short', year:'numeric'}))

const announcements = ref([
  { title: 'การใช้งานระบบเบื้องต้น', text: 'กรุณาตรวจสอบคู่มือการใช้งานแบบฟอร์มการลาต่างๆ', date: '24 Mar 2025', time: '08:30 AM' },
  { title: 'การใช้งานตัวอื่นๆ', text: 'กรุณาตรวจสอบคู่มือและแบบฟอร์มการลา', date: '26 Mar 2025', time: '16:30 PM' },
  { title: 'รายงานปัญหาการใช้งานระบบ', text: 'หากมีปัญหาการใช้งานระบบ กรุณา Capture หน้าจอ พร้อมทั้ง URL แจ้งทางทีมงาน', date: '26 Mar 2025', time: '17:00 PM' },
])

onMounted(async () => {
  token.value = localStorage.getItem("token")
  if (!token.value) { router.push("/login"); return }
  axios.defaults.headers.common['Authorization'] = `Token ${token.value}`

  try {
    const resUser = await axios.get("http://localhost:8000/api/users/me/")
    user.value = resUser.data
    if (user.value.role !== 'employee') { router.push("/login"); return }

    const todayStr = new Date().toISOString().split("T")[0]

    const resWork = await axios.get(`http://localhost:8000/api/attendance/records/?start_date=${todayStr}&end_date=${todayStr}`)
    todayWorkingCount.value = resWork.data.length

    const year = new Date().getFullYear().toString()
    const resLate = await axios.get(`http://localhost:8000/api/attendance/user-attendance/${user.value.id}/`)
    const thisYearRecords = resLate.data.filter((r:any) => r.date.startsWith(year))
    const totalLate = thisYearRecords.reduce((sum:any,r:any) => sum + (r.late_minutes||0), 0)
    lateStats.value = { minutes: totalLate, fines: totalLate * 5 }

    const today = new Date()
    const future15 = new Date(); future15.setDate(today.getDate()+15)
    const resLeave = await axios.get('http://localhost:8000/api/leave/leave-requests/')
    upcomingActivities.value = resLeave.data
      .filter((r:any) => r.user?.id === user.value.id && r.start_date)
      .filter((r:any) => {
        const start = new Date(r.start_date)
        return start >= today && start <= future15
      })
      .map((r:any) => ({
        date: new Date(r.start_date).toLocaleDateString('th-TH'),
        type: r.leave_type?.name || (r.status==='remote' ? 'ทำงานนอกสถานที่' : 'ลา'),
        period: r.period==='full'?'ทั้งวัน':(r.period==='morning'?'ครึ่งเช้า':'ครึ่งบ่าย'),
        status: r.status,
        reason: r.reason
      }))

  } catch (err) {
    console.error(err)
    router.push("/login")
  }
})
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

.dashboard-container {
  display: flex;
  gap: 20px;
}

.card-left {
  flex: 2;
}

.card-right {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.card {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
  margin-bottom: 15px;
}

.card-header h4 {
  margin: 0;
  font-size: 16px;
}

.icon-blue {
  color: #1890ff;
  font-size: 20px;
  margin-right: 10px;
}

.icon-yellow {
  color: #ffc107;
  font-size: 20px;
  margin-right: 10px;
}

.timeline {
  position: relative;
  margin: 0;
  max-height: 260px;
  overflow-y: auto;
  padding-right: 6px;
}

.timeline-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 20px;
  position: relative;
}

.timeline-content {
  border-left: 2px solid #ccc;
  padding-left: 15px;
  margin-left: 80px; 
  position: relative;
  z-index: 1; 
}

.timeline-indicator {
  position: absolute;
  top: 0;
  left: 0;
  width: 70px; 
  text-align: right;
  font-size: 12px;
  color: #888;
  z-index: 2; 
}

.timeline-title {
  margin: 0;
  font-weight: bold;
}

.timeline-text {
  margin: 5px 0;
  font-size: 14px;
  color: #555;
}

.timeline-date {
  font-size: 12px;
  color: #aaa;
}

.timeline-time {
  font-size: 12px;
  color: #888;
}

.card-body-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex-grow: 1;
  text-align: center;
}

.donut-chart-container {
  position: relative;
  width: 120px;
  height: 120px;
  margin-bottom: 10px;
}

.donut-chart {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: radial-gradient(closest-side, white 79%, transparent 80% 100%),
              conic-gradient(var(--c) calc(var(--p) * 1%), #eee 0);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.donut-label {
  position: absolute;
  font-size: 36px;
  font-weight: bold;
  color: #a54687;
}

.donut-sublabel {
  font-size: 12px;
  color: #888;
  margin-top: 5px;
}

.alert-box {
  background-color: #fff3cd;
  color: #856404;
  border: 1px solid #ffeeba;
  padding: 15px;
  border-radius: 5px;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.alert-box i {
  margin-right: 10px;
}

.alert-box p {
  margin: 0;
  font-weight: bold;
}

@media (max-width: 992px) {
  .dashboard-container {
    flex-direction: column;
  }
}

@media (max-width: 768px) {
  .sidebar {
    width: 200px;
  }
  .top-bar {
    padding: 10px;
  }
  .user-profile .username {
    display: none;
  }
}

.table-card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.responsive-table-wrapper {
    overflow-x: auto;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th, td {
    border: 1px solid #ddd;
    padding: 12px;
    text-align: left;
    white-space: nowrap;
}

th {
    background-color: #f2f2f2;
    font-weight: bold;
}

tr:nth-child(even) {
    background-color: #fafafa;
}
</style>