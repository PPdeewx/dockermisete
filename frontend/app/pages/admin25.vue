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
        <li class="nav-item active has-submenu">
          <a href="#" class="nav-link"><i class="fas fa-users"></i> บุคลากร</a>
          <ul class="submenu">
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
        <li class="nav-item">
          <a href="#" class="nav-link"><i class="fas fa-flask"></i> ห้องวิจัย</a>
        </li>
        <li class="nav-item"><a href="#" class="nav-link"><i class="fas fa-calendar-alt"></i> วันหยุด</a></li>
        <li class="nav-item has-submenu">
          <a href="#" class="nav-link"><i class="fas fa-cog"></i> ระบบการปฏิบัติงาน</a>
          <ul class="submenu">
            <li><a href="#" class="submenu-link">ตรวจสอบเวลาทำงาน</a></li>
            <li><a href="#" class="submenu-link">เวลางานคนลาออก</a></li>
            <li><a href="#" class="submenu-link">รายการลาตัวเอง</a></li>
            <li><a href="#" class="submenu-link">รายการลา ETE</a></li>
            <li><a href="#" class="submenu-link">ปฏิบัติงานนอกสถานที่</a></li>
            <li><a href="#" class="submenu-link">รายการอนุมัติการลาปฏิบัติงานนอกสถานที่</a></li>
            <li><a href="#" class="submenu-link">รายการอนุมัติการลา</a></li>
            <li><a href="#" class="submenu-link">ขออนุมัติลา</a></li>
            <li><a href="#" class="submenu-link">ขอลาให้คนอื่น</a></li>
            <li><a href="#" class="submenu-link">ขอปฏิบัติงานนอกสถานที่</a></li>
            <li><a href="#" class="submenu-link">ขอปฏิบัติงานนอกสถานที่ให้คนอื่น</a></li>
            <li><a href="#" class="submenu-link">Upload เวลางาน</a></li>
          </ul>
        </li>
      </ul>
    </div>

    <div class="main-content">
      <div class="top-bar">
        <div class="breadcrumbs">
          <span><i class="fas fa-home"></i> หน้าหลัก > พนักงานปัจจุบัน</span>
        </div>
        <div class="search-actions">
          <input type="text" placeholder="Search" class="search-input">
          <i class="fas fa-search"></i>
        </div>
        <div class="user-profile-container">
          <div class="user-profile" @click="toggleDropdown">
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
        <div class="header-with-button">
          <div class="header-with-icon">
            <i class="fas fa-users"></i>
            <h2>พนักงานปัจจุบัน</h2>
          </div>
          <button class="btn-add-employee"><i class="fas fa-plus-circle"></i> เพิ่มพนักงาน</button>
        </div>

        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>ลำดับที่</th>
                <th></th>
                <th>ชื่อ - นามสกุล</th>
                <th>Role</th>
                <th>Type</th>
                <th>ห้องวิจัย</th>
                <th>สถานะ</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>1</td>
                <td></td>
                <td>นาย admin admin</td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td><i class="fas fa-search-plus action-icon"></i><i class="fas fa-pen action-icon"></i></td>
              </tr>
              <tr v-for="i in 15" :key="i">
                <td>{{ i + 1 }}</td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td><i class="fas fa-search-plus action-icon"></i><i class="fas fa-pen action-icon"></i></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="modal-overlay">
        <div class="modal-content">
          <div class="modal-header">
            <h3>แก้ไขข้อมูล นาย admin admin</h3>
          </div>
          <div class="modal-body">
            <div class="form-row-modal">
              <label>Role :</label>
              <select class="form-select-modal">
                <option value="">กรุณาเลือก</option>
                <option value="admin">admin</option>
                <option value="user">user</option>
              </select>
            </div>
            <div class="form-row-modal">
              <label>Type :</label>
              <select class="form-select-modal">
                <option value="">กรุณาเลือก</option>
                <option value="admin">TEACHER</option>
                <option value="user">OFFICER</option>
                <option value="user">STUDENT</option>
              </select>
            </div>
            <div class="form-row-modal">
              <label>ตำแหน่ง :</label>
              <select class="form-select-modal">
                <option value="">กรุณาเลือก</option>
                <option value="">หัวหน้าศูนย์ฯ</option>
                <option value="">หัวหน้าห้องวิจัย</option>
                <option value="">รองหัวหน้าห้องวิจัย</option>
                <option value="">วิศวกรอาวุโส</option>
                <option value="">วิศวกร</option>
                <option value="">นักวิจัยอาวุโส</option>
                <option value="">นักวิจัย</option>
                <option value="">เจ้าหน้าที่ประสานงานอาวุโส</option>
                <option value="">เจ้าหน้าที่ประสานงาน</option>
                <option value="">เจ้าหน้าที่การเงิน</option>
                <option value="">เจ้าหน้าที่บัญชี</option>
                <option value="">เจ้าหน้าที่พัสดุ</option>
                <option value="">หัวหน้างานธุรการ</option>
                <option value="">แม่บ้าน</option>
                <option value="">อาจารย์</option>
                <option value="">นักศึกษาช่วยงาน</option>
              </select>
            </div>
            <div class="form-row-modal">
              <label>ประเภทการจ้าง :</label>
              <select class="form-select-modal">
                <option value="">กรุณาเลือก</option>
                <option value="">อาจารย์</option>
                <option value="">พนักงานประจำ</option>
                <option value="">พนักงานโครงการ</option>
                <option value="">นักศึกษาปริญญาโท</option>
                <option value="">นักศึกษาปริญญาเอก</option>
              </select>
            </div>
            <div class="form-row-modal">
              <label>ห้องปฏิบัติการ :</label>
              <select class="form-select-modal">
                <option value="">กรุณาเลือก</option>
                <option value="">ห้องวิจัยพลังงานทดแทนและอนุรักษ์พลังงาน</option>
                <option value="">ห้องวิจัยด้านวิศวกรรมและการบริหารจัดการการเปลี่ยนแปลงสภาพภูมิอากาศ</option>
                <option value="">โครงการพัฒนาการศึกษาด้านพลังงาน</option>
              </select>
            </div>
            <div class="form-row-modal">
              <label>สถานะ :</label>
              <select class="form-select-modal">
                <option value="">กรุณาเลือก</option>
                <option value="">ปฎิบัติงาน</option>
                <option value="">ลาออก</option>
                <option value="">พักร้อน</option>
              </select>
            </div>
            <div class="form-row-modal split-fields">
              <div class="input-group">
                <label>รหัสเครื่อง... :</label>
                <input type="text" class="form-input-modal">
              </div>
              <div class="input-group">
                <label>Email :</label>
                <input type="text" class="form-input-modal">
              </div>
            </div>
            <div class="form-row-modal split-fields">
              <div class="input-group">
                <label>ลากิจ :</label>
                <input type="text" class="form-input-modal">
              </div>
              <div class="input-group">
                <label>ลาป่วย :</label>
                <input type="text" class="form-input-modal">
              </div>
            </div>
            <div class="form-row-modal split-fields">
              <div class="input-group">
                <label>ลาพักร้อน :</label>
                <input type="text" class="form-input-modal">
              </div>
              <div class="input-group">
                <label>ลาอื่นๆ :</label>
                <input type="text" class="form-input-modal">
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn-save">บันทึกข้อมูล</button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const isDropdownOpen = ref(false);

const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value;
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

.search-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.search-input {
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.search-actions .fas {
  color: #555;
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

.btn-add-employee {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
}

.btn-add-employee:hover {
  background-color: #218838;
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

.action-icon {
  cursor: pointer;
  margin-right: 10px;
  color: #555;
}

.action-icon:hover {
  color: #007bff;
}

/* Modal specific styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  width: 90%;
  max-width: 600px;
}

.modal-header h3 {
  margin: 0;
  font-size: 20px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
  margin-bottom: 15px;
}

.modal-body {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-row-modal {
  display: flex;
  align-items: center;
  gap: 10px;
}

.form-row-modal label {
  font-weight: bold;
  width: 150px;
  text-align: right;
  white-space: nowrap;
}

.form-row-modal .form-select-modal,
.form-row-modal .form-input-modal {
  flex-grow: 1;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.split-fields {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.input-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.input-group label {
  width: auto;
  min-width: 80px;
  text-align: right;
}

.input-group input {
  flex-grow: 1;
}

.modal-footer {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.btn-save {
  background-color: #52c41a;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
}

.btn-save:hover {
  background-color: #389e08;
}

@media (max-width: 768px) {
  .top-bar {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  .search-actions {
    width: 100%;
    justify-content: space-between;
  }
  .search-input {
    flex-grow: 1;
  }
  .header-with-button {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  .form-row-modal, .split-fields {
    grid-template-columns: 1fr;
    flex-direction: column;
  }
  .form-row-modal label, .input-group label {
    text-align: left;
    width: auto;
  }
  .input-group {
    flex-direction: column;
    align-items: flex-start;
  }
  .input-group input {
    width: 100%;
  }
}
</style>