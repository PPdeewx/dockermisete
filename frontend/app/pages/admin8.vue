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
            <li><a href="#" class="submenu-link active">เปลี่ยนสถานะพนักงาน</a></li>
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
          <span><i class="fas fa-home"></i> หน้าหลัก > บุคลากร > เปลี่ยนสถานะพนักงาน</span>
        </div>
        <div class="user-profile-container">
          <div class="user-profile" @click="toggleDropdown">
            <i class="fas fa-bell"></i>
            <i class="fas fa-user-circle"></i>
            <span class="username">Username ตำแหน่ง: Admin</span>
            <i class="fas fa-chevron-down" :class="{ 'rotate': isDropdownOpen }"></i>
          </div>
          <div class="dropdown-menu" v-if="isDropdownOpen">
            <a href="#" class="dropdown-item"><i class="fas fa-user"></i> ดูข้อมูลส่วนตัว</a>
            <a href="#" class="dropdown-item"><i class="fas fa-user-edit"></i> แก้ไขข้อมูลส่วนตัว</a>
            <a href="#" class="dropdown-item"><i class="fas fa-fingerprint"></i> เปลี่ยนรหัสผ่าน</a>
            <a href="#" class="dropdown-item"><i class="fas fa-sign-out-alt"></i> ออกจากระบบ</a>
          </div>
        </div>
      </div>

      <div class="content-container">
        <div class="table-header">
          <h2>เปลี่ยนสถานะพนักงาน</h2>
          <div class="header-actions">
            <div class="search-container">
              <span>ค้นหาพนักงาน :</span>
              <input type="text" v-model="searchQuery" placeholder="ค้นหา..." />
            </div>
            <button class="btn-save" @click="saveChanges">
              <i class="fas fa-plus"></i> บันทึกการเปลี่ยนแปลง
            </button>
          </div>
        </div>
        <div class="table-responsive">
          <table>
            <thead>
              <tr>
                <th>ลำดับที่</th>
                <th>รหัสพนักงาน</th>
                <th>ชื่อ - นามสกุล</th>
                <th>Email</th>
                <th>ตำแหน่ง</th>
                <th>เบอร์โทรศัพท์</th>
                <th>สถานะปัจจุบัน</th>
                <th>เปลี่ยนสถานะ</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(employee, index) in filteredEmployees" :key="index">
                <td>{{ index + 1 }}</td>
                <td>{{ employee.id }}</td>
                <td>{{ employee.name }}</td>
                <td>{{ employee.email }}</td>
                <td>{{ employee.position }}</td>
                <td>{{ employee.phone }}</td>
                <td>{{ employee.currentStatus }}</td>
                <td>
                  <select v-model="employee.newStatus">
                    <option value="ปฏิบัติงาน">ปฏิบัติงาน</option>
                    <option value="ลาออก">ลาออก</option>
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
import { ref, reactive, computed } from 'vue';

const isDropdownOpen = ref(false);
const searchQuery = ref('');

const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value;
};

const employees = reactive([
  {
    id: 'E-001',
    name: 'สมชาย เจริญสุข',
    email: 'somchai@example.com',
    position: 'นักวิจัย',
    phone: '081-123-4567',
    currentStatus: 'ปฏิบัติงาน',
    newStatus: 'ปฏิบัติงาน',
  },
  {
    id: 'E-002',
    name: 'สมหญิง รักดี',
    email: 'somying@example.com',
    position: 'วิศวกรอาวุโส',
    phone: '089-765-4321',
    currentStatus: 'ปฏิบัติงาน',
    newStatus: 'ปฏิบัติงาน',
  },
  {
    id: 'E-003',
    name: 'เอกชัย มีชัย',
    email: 'aekachai@example.com',
    position: 'เจ้าหน้าที่ประสานงาน',
    phone: '098-111-2222',
    currentStatus: 'ปฏิบัติงาน',
    newStatus: 'ปฏิบัติงาน',
  },
  {
    id: 'E-004',
    name: 'อรุณี สว่างจิต',
    email: 'arunee@example.com',
    position: 'นักวิจัย',
    phone: '081-999-8888',
    currentStatus: 'ปฏิบัติงาน',
    newStatus: 'ปฏิบัติงาน',
  },
]);

const filteredEmployees = computed(() => {
  if (!searchQuery.value) {
    return employees;
  }
  const query = searchQuery.value.toLowerCase();
  return employees.filter(employee => {
    return (
      employee.name.toLowerCase().includes(query) ||
      employee.id.toLowerCase().includes(query) ||
      employee.email.toLowerCase().includes(query)
    );
  });
});

const saveChanges = () => {
  const changes = employees.filter(emp => emp.currentStatus !== emp.newStatus);
  if (changes.length > 0) {
    console.log('Changes to be saved:', changes);
    alert('บันทึกการเปลี่ยนแปลงเรียบร้อยแล้ว');
    changes.forEach(emp => {
      emp.currentStatus = emp.newStatus;
    });
  } else {
    alert('ไม่มีการเปลี่ยนแปลงสถานะพนักงาน');
  }
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
  width: 270px;
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

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 20px;
}

.table-header h2 {
  font-weight: bold;
  font-size: 24px;
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.search-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.search-container input {
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.btn-save {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  background-color: #4CAF50;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-save:hover {
  background-color: #45a049;
}

.btn-save i {
  margin-right: 5px;
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

select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
</style>