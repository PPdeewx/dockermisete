<template>
    <TopBar > <template #breadcrumbs>
              <Breadcrumb  :model="items"/>

    </template></TopBar>

      <div class="content-container">
        <div class="header-with-buttons">
          <h2><i class="fas fa-calendar-alt"></i> UPLOAD เวลางาน</h2>
        </div>

        <div class="table-controls">
          <div class="upload-container">
            <input type="file" ref="fileInput" accept=".xlsx, .xls" @change="handleFileUpload" style="display: none;" />
            <button class="btn-upload" @click="triggerFileInput">UPLOAD ไฟล์ Excel</button>
            <span v-if="uploadStatus" :class="uploadStatus.class">{{ uploadStatus.message }}</span>
          </div>
          <div class="search-container">
            <div class="input-group">
              <input type="text" id="date-range" placeholder="เลือกช่วงวันที่" class="form-input">
            </div>
            <input type="text" v-model="searchQuery" placeholder="ค้นหาชื่อพนักงาน" class="search-input">
            <button class="btn-search" @click="searchData"><i class="fas fa-search"></i> ค้นหา</button>
          </div>
          <button class="btn-export" @click="exportData">Export</button>
        </div>

        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        <div v-else-if="isLoading" class="loading">กำลังโหลด...</div>
        <div v-else-if="filteredAttendanceRecords.length === 0" class="no-data">ไม่มีข้อมูลการเข้างาน</div>
        <div v-else class="table-container">
          <table>
            <thead>
              <tr>
                <th>วันที่</th>
                <th>รหัสพนักงาน</th>
                <th>ชื่อ - นามสกุล</th>
                <th>เวลาเข้างาน</th>
                <th>เวลาออกงาน</th>
                <th>มาสาย (นาที)</th>
                <th>ออกก่อน (นาที)</th>
                <th>สถานะ</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(record, index) in filteredAttendanceRecords" :key="index">
                <td>{{ formatDate(record.date) }}</td>
                <td>{{ record.employee_code }}</td>
                <td>{{ record.full_name }}</td>
                <td>{{ record.check_in || '-' }}</td>
                <td>{{ record.check_out || '-' }}</td>
                <td>{{ record.late_minutes }}</td>
                <td>{{ record.early_leave_minutes }}</td>
                <td><span :class="statusClass(record.status)">{{ statusDisplay(record.status) }}</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
</template>

<script setup lang="ts">
import TopBar from '~/components/Topbar.vue'

import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

import flatpickr from 'flatpickr'

import Card from 'primevue/card'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'

import Breadcrumb from 'primevue/breadcrumb';

import type { MenuItem } from 'primevue/menuitem';

const items : MenuItem[] = [
  {
    label : 'ระบบการปฏิบัติงาน',url : '/admin'
  },
  {
    label : 'UPLOAD เวลางาน',url : '/admin'
  }
]
const router = useRouter();
const token = ref<string | null>(null);
const showProfileMenu = ref(false);
const currentUser = ref<any>(null);
const fileInput = ref<HTMLInputElement | null>(null);
const uploadStatus = ref<{ message: string; class: string } | null>(null);
const attendanceRecords = ref<any[]>([]);
const searchQuery = ref('');
const dateRange = ref(['', '']);
const isLoading = ref(false);
const errorMessage = ref('');

const toggleProfileMenu = () => {
  showProfileMenu.value = !showProfileMenu.value;
};

const goTo = (path: string) => {
  router.push(path);
};

const triggerFileInput = () => {
  if (fileInput.value) {
    fileInput.value.click();
  }
};

const handleFileUpload = async (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (!input.files || input.files.length === 0) {
    uploadStatus.value = { message: 'กรุณาเลือกไฟล์ Excel', class: 'error' };
    return;
  }

  const file = input.files[0];
  uploadStatus.value = { message: 'กำลังอัปโหลด...', class: 'loading' };

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await axios.post('http://localhost:8000/api/attendance/upload-excel/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    if (response.status === 200 || response.status === 207) {
      uploadStatus.value = {
        message: response.data.message + (response.data.errors ? ` (${response.data.errors.join(', ')})` : ''),
        class: response.data.errors ? 'warning' : 'success',
      };
      await fetchAttendanceRecords();
    } else {
      uploadStatus.value = { message: 'อัปโหลดล้มเหลว', class: 'error' };
    }
  } catch (err) {
    console.error('Upload error:', err);
    uploadStatus.value = { message: 'เกิดข้อผิดพลาดในการอัปโหลด', class: 'error' };
  } finally {
    if (fileInput.value) {
      fileInput.value.value = '';
    }
  }
};

const fetchAttendanceRecords = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    const params: any = {};
    if (dateRange.value[0] && dateRange.value[1]) {
      params.start_date = dateRange.value[0];
      params.end_date = dateRange.value[1];
      console.log('Sending params:', params);
    }
    if (searchQuery.value) {
      params.name = searchQuery.value;
    }

    const response = await axios.get('http://localhost:8000/api/attendance/records/', { params });
    console.log('Received records:', response.data);
    attendanceRecords.value = response.data;
  } catch (err) {
    console.error('Error fetching records:', err);
    errorMessage.value = 'ไม่สามารถดึงข้อมูลการเข้างานได้';
  } finally {
    isLoading.value = false;
  }
};

const searchData = async () => {
  await fetchAttendanceRecords();
};

const exportData = () => {
  const data = filteredAttendanceRecords.value.map(record => ({
    วันที่: formatDate(record.date),
    รหัสพนักงาน: record.employee_code,
    'ชื่อ - นามสกุล': record.full_name,
    เวลาเข้างาน: record.check_in || '-',
    เวลาออกงาน: record.check_out || '-',
    'มาสาย (นาที)': record.late_minutes,
    'ออกก่อน (นาที)': record.early_leave_minutes,
    สถานะ: statusDisplay(record.status),
  }));

  const ws = XLSX.utils.json_to_sheet(data);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, 'Attendance');
  XLSX.write_file(wb, 'attendance_records.xlsx');
};

const filteredAttendanceRecords = computed(() => {
  let filtered = attendanceRecords.value;
  if (searchQuery.value) {
    filtered = filtered.filter(record =>
      record.full_name.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  }
  if (dateRange.value[0] && dateRange.value[1]) {
    const start = new Date(dateRange.value[0]).setHours(0, 0, 0, 0);
    const end = new Date(dateRange.value[1]).setHours(23, 59, 59, 999);
    filtered = filtered.filter(record => {
      const recordDate = new Date(record.date).getTime();
      return recordDate >= start && recordDate <= end;
    });
  }
  return filtered;
});

const statusClass = (status: string | null) => {
  const classes: { [key: string]: string } = {
    normal: 'status-normal',
    leave: 'status-leave',
    remote: 'status-remote',
    absent: 'status-absent',
    '': 'status-absent',
    null: 'status-absent',
  };
  return classes[status as string] || 'status-absent';
};

const statusDisplay = (status: string | null) => {
  const displays: { [key: string]: string } = {
    normal: 'ปกติ',
    leave: 'ลา',
    remote: 'ปฏิบัติงานนอกสถานที่',
    absent: 'ขาดงาน',
    '': 'ขาดงาน',
    null: 'ขาดงาน',
  };
  return displays[status as string] || 'ขาดงาน';
};

const formatDate = (dateStr: string) => {
  if (!dateStr) return '-';
  const date = new Date(dateStr);
  return date.toISOString().split('T')[0];
};

onMounted(async () => {
  if (typeof window !== 'undefined') {
    token.value = localStorage.getItem('token');
  }

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

    flatpickr('#date-range', {
      mode: 'range',
      dateFormat: 'Y-m-d',
      enableTime: false,
      allowInput: true,
      closeOnSelect: false,
      onChange: (selectedDates) => {
        dateRange.value = selectedDates.length === 2 
          ? selectedDates.map(date => date.toISOString().split('T')[0])
          : ['', ''];
        console.log('Selected date range:', dateRange.value);
      },
    });

    await fetchAttendanceRecords();
  } catch (err) {
    console.error('Error during mount:', err);
    router.push('/login');
  }
});

const logout = () => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('token');
  }
  delete axios.defaults.headers.common['Authorization'];
  router.push('/login');
};
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

.header-with-buttons {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 20px;
}

.header-with-buttons h2 {
  font-size: 24px;
  font-weight: bold;
}

.header-with-buttons h2 i {
  margin-right: 10px;
  color: #ff9800;
}

.table-controls {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-bottom: 20px;
  gap: 10px;
}

.btn-upload {
  background-color: #1890ff;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  font-weight: bold;
}

.btn-upload:hover {
  background-color: #096dd9;
}

.search-container {
  display: flex;
  gap: 10px;
  align-items: center;
}

.search-input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-input:focus {
  outline: none;
}

.btn-search {
  background-color: #1890ff;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
}

.btn-search:hover {
  background-color: #096dd9;
}

.btn-export {
  background-color: #fff;
  color: #1890ff;
  border: 1px solid #1890ff;
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
}

.btn-export:hover {
  background-color: #f0f2f5;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

thead th {
  background-color: #007bff;
  color: white;
}

.save-actions {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.btn-save {
  background-color: #52c41a;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.2s;
}

.btn-save:hover {
  background-color: #389e08;
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

.upload-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.upload-container .success {
  color: green;
}

.upload-container .error {
  color: red;
}

.upload-container .warning {
  color: orange;
}

.upload-container .loading {
  color: blue;
}

.error-message {
  color: red;
  margin: 10px 0;
  padding: 10px;
  background: #ffebee;
  border-radius: 4px;
}

.loading {
  color: blue;
  margin: 10px 0;
  text-align: center;
}

.no-data {
  color: gray;
  margin: 10px 0;
  text-align: center;
}

.status-normal {
  background-color: #4caf50;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
}

.status-leave {
  background-color: #ff9800;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
}

.status-remote {
  background-color: #2196f3;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
}

.status-absent {
  background-color: #f44336;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
}

.input-group {
  display: flex;
  flex-direction: column;
}

.form-input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style>