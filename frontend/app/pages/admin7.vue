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
            <li><a href="#" class="submenu-link active">เพิ่มบุคลากรภายนอก</a></li>
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
          <span><i class="fas fa-home"></i> หน้าหลัก > บุคลากร > เพิ่มบุคลากรภายนอก</span>
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
        <div class="form-header">
          <h2>เพิ่มบุคลากรภายนอก</h2>
          <button class="btn-cancel" @click.prevent="cancelForm">
            <i class="fas fa-times"></i> ยกเลิก
          </button>
        </div>
        <form @submit.prevent="submitForm">
          <div class="form-row">
            <div class="form-group">
              <label for="thai-name-prefix">คำนำหน้าชื่อ *</label>
              <select id="thai-name-prefix" v-model="form.thaiNamePrefix" required>
                <option value="">กรุณาเลือก</option>
                <option v-for="prefix in thaiNamePrefixOptions" :key="prefix" :value="prefix">
                  {{ prefix }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label for="english-name-prefix">ชื่อภาษาอังกฤษ *</label>
              <select id="english-name-prefix" v-model="form.englishNamePrefix" required>
                <option value="">กรุณาเลือก</option>
                <option v-for="prefix in englishNamePrefixOptions" :key="prefix" :value="prefix">
                  {{ prefix }}
                </option>
              </select>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="thai-name">ชื่อภาษาไทย *</label>
              <input type="text" id="thai-name" v-model="form.thaiName" required />
            </div>
            <div class="form-group">
              <label for="english-name">ชื่อภาษาอังกฤษ *</label>
              <input type="text" id="english-name" v-model="form.englishName" required />
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="thai-surname">นามสกุลภาษาไทย *</label>
              <input type="text" id="thai-surname" v-model="form.thaiSurname" required />
            </div>
            <div class="form-group">
              <label for="english-surname">นามสกุลภาษาอังกฤษ *</label>
              <input type="text" id="english-surname" v-model="form.englishSurname" required />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="email">Email *</label>
              <input type="email" id="email" v-model="form.email" required />
            </div>
            <div class="form-group">
              <label for="phone">เบอร์โทรศัพท์ *</label>
              <input type="tel" id="phone" v-model="form.phone" required />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="department">หน่วยงาน :</label>
              <input type="text" id="department" v-model="form.department" />
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
import { ref, reactive } from 'vue';

const isDropdownOpen = ref(false);

const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value;
};

// ตัวเลือกสำหรับ dropdowns
const thaiNamePrefixOptions = ref(['นาย', 'นาง', 'นางสาว']);
const englishNamePrefixOptions = ref(['Mr.', 'Mrs.', 'Ms.']);

const form = reactive({
  thaiNamePrefix: '',
  englishNamePrefix: '',
  thaiName: '',
  thaiSurname: '',
  englishName: '',
  englishSurname: '',
  email: '',
  phone: '',
  department: '',
});

const submitForm = () => {
  console.log('Form data submitted:', form);
};

const cancelForm = () => {
  resetForm();
  console.log('Form has been canceled.');
};

const resetForm = () => {
  Object.assign(form, {
    thaiNamePrefix: '',
    englishNamePrefix: '',
    thaiName: '',
    thaiSurname: '',
    englishName: '',
    englishSurname: '',
    email: '',
    phone: '',
    department: '',
  });
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
</style>