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
        <li class="nav-item active has-submenu">
          <a href="#" class="nav-link"><i class="fas fa-cog"></i> ระบบการปฏิบัติงาน</a>
          <ul class="submenu">
            <li><a href="/admin12" class="submenu-link">ตรวจสอบเวลาทำงาน</a></li>
            <li><a href="/admin13" class="submenu-link">เวลางานคนลาออก</a></li>
            <li><a href="/admin14" class="submenu-link">รายการลาตัวเอง</a></li>
            <li><a href="/admin15" class="submenu-link">รายการลา ETE</a></li>
            <li><a href="/admin16" class="submenu-link">ปฏิบัติงานนอกสถานที่</a></li>
            <li><a href="/admin17" class="submenu-link">รายการอนุมัติการลาปฏิบัติงานนอกสถานที่</a></li>
            <li><a href="#" class="submenu-link active">รายการอนุมัติการลา</a></li>
            <li><a href="/admin19" class="submenu-link">ขออนุมัติลา</a></li>
            <li><a href="/admin20" class="submenu-link">ขอลาให้คนอื่น</a></li>
            <li><a href="/admin21" class="submenu-link">ขอปฏิบัติงานนอกสถานที่</a></li>
            <li><a href="/admin22" class="submenu-link">ขอปฏิบัติงานนอกสถานที่ให้คนอื่น</a></li>
            <li><a href="/admin23" class="submenu-link">Upload เวลางาน</a></li>
          </ul>
        </li>
      </ul>
    </div>

    <div class="main-content">
      <div class="top-bar">
        <div class="breadcrumbs">
          <span><i class="fas fa-home"></i> หน้าหลัก > รายการอนุมัติการลา</span>
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
          <h2><i class="fas fa-calendar-check"></i> รายการอนุมัติการลา</h2>
        </div>
        
        <div class="search-container">
          <div class="input-group">
            <label for="date-range">ช่วงวันที่</label>
            <input type="text" id="date-range" placeholder="ช่วงวันที่" class="form-input" v-model="dateRange">
          </div>
          <div class="input-group">
            <label for="room-select">ห้องวิจัย</label>
            <select id="room-select" class="form-select" v-model="selectedRoom">
              <option value="">ทั้งหมด</option>
              <option v-for="room in roomList" :key="room.id" :value="room.id">
                {{ room.name }}
              </option>
            </select>
          </div>
          <button class="btn-search" @click="search">ค้นหา</button>
        </div>
        
        <div class="approval-table-container">
          <table class="approval-table">
            <thead>
              <tr>
                <th>วันที่</th>
                <th>ชื่อ - นามสกุล</th>
                <th>ห้องวิจัย</th>
                <th>ประเภทการลา</th>
                <th>ช่วงเวลา</th>
                <th>ผู้อนุมัติ</th>
                <th>สถานะ</th>
                <th>การอนุมัติ</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in filteredApprovalList" :key="index">
                <td>{{ item.date }}</td>
                <td>{{ item.name }}</td>
                <td>{{ item.room }}</td>
                <td>{{ item.type }}</td>
                <td>{{ item.time }}</td>
                <td>{{ item.approver }}</td>
                <td>
                  <span :class="`status-badge status-${item.status}`">
                    {{ item.status_th }}
                  </span>
                </td>
                <td>
                  <select v-model="item.action" class="action-select" @change="updateApproval(item)">
                    <option value="pending">รออนุมัติ</option>
                    <option value="approve">อนุมัติ</option>
                    <option value="reject">ไม่อนุมัติ</option>
                  </select>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
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

const dateRange = ref('');
const selectedRoom = ref('');

const roomList = ref<any[]>([])

const approvalList = ref<any[]>([])

const filteredApprovalList = computed(() => {
  return approvalList.value.filter(item => {
    const roomMatch = !selectedRoom.value || item.room_id === selectedRoom.value;
    return roomMatch;
  });
});

const search = () => {
  fetchApprovals();
};

const currentUser = ref<any>(null)

async function fetchDepartments() {
  try {
    const res = await axios.get("http://localhost:8000/api/users/departments/");
    roomList.value = res.data.map((d:any) => ({
      id: d.id,
      name: d.name_th
    }));
  } catch (err) {
    console.error("โหลดห้องวิจัยไม่สำเร็จ", err)
  }
}

async function fetchApprovals() {
  try {
    const res = await axios.get("http://localhost:8000/api/leave/leave-requests/");
    approvalList.value = res.data.map((item: any) => ({
      id: item.id,
      date: item.start_date === item.end_date 
              ? item.start_date 
              : `${item.start_date} - ${item.end_date}`,
      name: item.on_behalf_of_name 
            || `${item.user?.firstname_th || ''} ${item.user?.lastname_th || ''}`,
      type: item.leave_type?.name || "-",
      time: item.period,
      approver: item.approver 
        ? (item.approver.firstname_th || item.approver.lastname_th
            ? `${item.approver.firstname_th || ''} ${item.approver.lastname_th || ''}`.trim()
            : (item.approver.full_name || item.approver.username || "-"))
        : (item.user?.department?.approvers?.map((a:any) => `${a.firstname_th} ${a.lastname_th}`).join(", ") || "หัวหน้าห้องวิจัย"),
      status: item.status,
      status_th: statusMap[item.status] || item.status,
      action: item.status,
      room: item.user?.department?.name_th 
            || item.user?.department?.name 
            || item.department_name 
            || "-",
      room_id: item.user?.department?.id || null
    }));
  } catch (err) {
    console.error("โหลดรายการลาไม่สำเร็จ", err)
  }
}

const statusMap: Record<string, string> = {
  pending: "รออนุมัติ",
  approved: "อนุมัติแล้ว",
  rejected: "ไม่อนุมัติ",
  cancelled: "ยกเลิก"
};

async function updateApproval(item: any) {
  try {
    if (item.action === "approve") {
      await axios.post(`http://localhost:8000/api/leave/leave-requests/${item.id}/approve/`);
    } else if (item.action === "reject") {
      await axios.post(`http://localhost:8000/api/leave/leave-requests/${item.id}/reject/`);
    }
    fetchApprovals();
  } catch (err) {
    console.error("อัปเดตสถานะไม่สำเร็จ", err)
  }
}

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
    await fetchDepartments()
    await fetchApprovals()
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

.header-with-button h2 {
  font-size: 24px;
  font-weight: bold;
}

.header-with-button h2 i {
  margin-right: 10px;
  color: #ff9800;
}

.search-container {
  display: flex;
  align-items: flex-end;
  gap: 15px;
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f8f8f8;
  border-radius: 8px;
  border: 1px solid #eee;
  flex-wrap: wrap;
}

.input-group {
  display: flex;
  flex-direction: column;
}

.input-group label {
  font-size: 0.9em;
  color: #666;
  margin-bottom: 5px;
}

.form-input,
.form-select {
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1em;
  min-width: 150px;
}

.btn-search {
  background-color: #1890ff;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
}

.btn-search:hover {
  background-color: #096dd9;
}

.approval-table-container {
  overflow-x: auto;
}

.approval-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.approval-table th,
.approval-table td {
  border: 1px solid #e0e0e0;
  padding: 12px 15px;
  text-align: left;
  white-space: nowrap;
}

.approval-table th {
  background-color: #f2f2f2;
  font-weight: bold;
}

.approval-table tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.9em;
  white-space: nowrap;
}

.status-badge.status-pending {
  background-color: #fffbe6;
  color: #faad14;
  border: 1px solid #ffe58f;
}

.status-badge.status-approved {
  background-color: #f6ffed;
  color: #52c41a;
  border: 1px solid #b7eb8f;
}

.status-badge.status-rejected {
  background-color: #fff1f0;
  color: #f5222d;
  border: 1px solid #ffccc7;
}

.action-select {
  padding: 6px 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
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