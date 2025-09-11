<template>
  <div class="full-page-container">
    <div class="sidebar">
      <div class="sidebar-header">
        <span>MIS ETE</span>
      </div>
      <ul class="nav-menu">
        <li class="nav-item">
          <NuxtLink to="/admin16" class="nav-link">
            <i class="fas fa-home"></i> หน้าหลัก
          </NuxtLink>
        </li>
        <li class="nav-item has-submenu active">
          <a href="#" class="nav-link"><i class="fas fa-users"></i> บุคลากร</a>
          <ul class="submenu active">
            <li><a href="#" class="submenu-link active">พนักงานปัจจุบัน</a></li>
            <li><a href="#" class="submenu-link">พนักงานที่ลาออก</a></li>
            <li><a href="#" class="submenu-link">บุคลากรภายนอก</a></li>
            <li><a href="#" class="submenu-link">พนักงาน EDDP</a></li>
            <li><a href="#" class="submenu-link">เพิ่ม/แก้ไข/ลบ พนักงาน</a></li>
            <li><a href="#" class="submenu-link">เพิ่มบุคลากรภายนอก</a></li>
            <li><a href="#" class="submenu-link">เปลี่ยนสถานะพนักงาน</a></li>
            <li><a href="#" class="submenu-link">กำหนดโควต้าลา(ทั้งหมด)</a></li>
          </ul>
        </li>
        <li class="nav-item">
          <NuxtLink to="/admin10" class="nav-link">
            <i class="fas fa-flask"></i> ห้องวิจัย
          </NuxtLink>
        </li>
        <li class="nav-item">
          <NuxtLink to="/admin11" class="nav-link">
            <i class="fas fa-calendar-alt"></i> วันหยุด
          </NuxtLink>
        </li>
        <li class="nav-item">
          <NuxtLink to="/admin12" class="nav-link">
            <i class="fas fa-cog"></i> ระบบการปฏิบัติงาน
          </NuxtLink>
        </li>
      </ul>
    </div>

    <div class="main-content">
      <div class="top-bar">
        <div class="breadcrumbs">
          <span><i class="fas fa-home"></i> หน้าหลัก > บุคลากร > พนักงานปัจจุบัน</span>
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
          <div class="left-section">
            <i class="fas fa-user-circle title-icon"></i>
            <h2>พนักงานปัจจุบัน</h2>
          </div>
          <button class="add-button" @click="goToAdd"><i class="fas fa-plus"></i> เพิ่มพนักงาน</button>
        </div>

        <div class="search-and-table-container">
          <div class="search-bar-container">
            <label for="search">SEARCH :</label>
            <input v-model="search" type="text" id="search" class="search-input" placeholder="ค้นหา...">
          </div>

          <div class="responsive-table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>ลำดับที่</th>
                  <th>รหัส</th>
                  <th>Username</th>
                  <th>Lab</th>
                  <th>ชื่อภาษาไทย</th>
                  <th>เบอร์โทรศัพท์</th>
                  <th>Email</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(emp, index) in filteredEmployees" :key="emp.id">
                  <td>{{ index + 1 }}</td>
                  <td>{{ emp.employee_code }}</td>
                  <td>{{ emp.username }}</td>
                  <td>{{ emp.department?.name_th || '-' }}</td>
                  <td>{{ emp.firstname_th }} {{ emp.lastname_th }}</td>
                  <td>{{ emp.phone_number }}</td>
                  <td>{{ emp.email }}</td>
                  <td>
                    <button @click="viewEmployee(emp.id)">👁️</button>
                    <button @click="editEmployee(emp.id)">✏️</button>
                    <button @click="deleteEmployee(emp.id)">❌</button>
                  </td>
                </tr>
                <tr v-if="filteredEmployees.length === 0">
                  <td colspan="8" style="text-align:center;">ไม่พบข้อมูล</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showEditModal" class="modal-overlay">
      <div class="modal-content">
        <form @submit.prevent="saveEdit">
          <div class="modal-header">
            <h3><i class="fas fa-user-edit"></i> แก้ไขข้อมูล: {{ form.firstname_th }} {{ form.lastname_th }}</h3>
          </div>
          <div class="modal-body">
            <div class="form-row-modal">
              <label>Username :</label>
              <input v-model="form.username" type="text" class="form-input-modal" disabled />
            </div>
            <div class="form-row-modal">
              <label>Email :</label>
              <input v-model="form.email" type="email" class="form-input-modal" />
            </div>
            <div class="form-row-modal">
              <label>เบอร์โทร :</label>
              <input v-model="form.phone_number" type="text" class="form-input-modal" />
            </div>
            <div class="form-row-modal">
              <label>Role :</label>
              <select v-model="form.role" class="form-select-modal">
                <option value="">กรุณาเลือก</option>
                <option value="admin">Admin</option>
                <option value="employee">User</option>
              </select>
            </div>
            <div class="form-row-modal">
              <label>ตำแหน่ง :</label>
              <select v-model="form.position" class="form-select-modal">
                <option v-for="g in groups" :key="g.value" :value="g.value">
                  {{ g.label }}
                </option>
              </select>
            </div>
            <div class="form-row-modal">
              <label>ห้องวิจัย :</label>
              <select v-model="form.department.id" class="form-select-modal">
                <option v-for="lab in departments" :key="lab.id" :value="lab.id">
                  {{ lab.name_th }}
                </option>
              </select>
            </div>
            <div class="form-row-modal">
              <label>สถานะ :</label>
              <select v-model="form.status" class="form-select-modal">
                <option value="active">พนักงานปัจจุบัน</option>
                <option value="resigned">ลาออก</option>
              </select>
            </div>
            <div class="form-row-modal split-fields">
              <div class="input-group">
                <label>ลากิจ :</label>
                <input v-model="form.quota_casual" type="number" class="form-input-modal" />
              </div>
              <div class="input-group">
                <label>ลาป่วย :</label>
                <input v-model="form.quota_sick" type="number" class="form-input-modal" />
              </div>
            </div>
            <div class="form-row-modal split-fields">
              <div class="input-group">
                <label>ลาพักร้อน :</label>
                <input v-model="form.quota_vacation" type="number" class="form-input-modal" />
              </div>
              <div class="input-group">
                <label>ลาอื่นๆ :</label>
                <input v-model="form.quota_other" type="number" class="form-input-modal" />
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn-save" type="submit">บันทึกข้อมูล</button>
            <button type="button" class="btn-cancel" @click="showEditModal=false">ยกเลิก</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, reactive } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const token = ref<string | null>(null);
const employees = ref<any[]>([]);
const search = ref("");
const showEditModal = ref(false);
const form = reactive<any>({
  id: null,
  username: '',
  email: '',
  phone_number: '',
  role: '',
  status: '',
  position: '',
  department: '',
  quota_vacation: 0,
  quota_sick: 0,
  quota_casual: 0,
  quota_other: 0
});

const currentUser = ref<any>(null);
const showProfileMenu = ref(false);

const toggleProfileMenu = () => {
  showProfileMenu.value = !showProfileMenu.value;
};

const handleBodyClick = (event: MouseEvent) => {
  if (showProfileMenu.value && !(event.target as HTMLElement).closest('.user-profile')) {
    showProfileMenu.value = false;
  }
};

const goToAdd = () => router.push('/admin6');

const goTo = (path: string) => {
  router.push(path);
};

const departments = ref<any[]>([]);
const groups = ref<any[]>([]);

const loadGroups = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/users/groups/');
    groups.value = res.data.map((g: any) => ({ value: g.name, label: g.name }));
  } catch (err) {
    console.error(err);
  }
};

const loadDepartments = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/users/departments/');
    departments.value = res.data;
  } catch (err) {
    console.error(err);
  }
};

const loadEmployees = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/users/filter/?status=active');
    employees.value = res.data;
  } catch (err) {
    console.error(err);
  }
};

const viewEmployee = (id: number) => {
  router.push(`/admin24/${id}`);
};

const editEmployee = async (id: number) => {
  try {
    const res = await axios.get(`http://localhost:8000/api/users/${id}/`);
    form.id = res.data.id;
    form.username = res.data.username;
    form.email = res.data.email;
    form.phone_number = res.data.phone_number;
    form.role = res.data.role || '';
    form.position = res.data.groupName || (res.data.groups?.[0]?.name || '');
    form.status = res.data.status || 'active';
    form.quota_casual = res.data.quota_casual || 0;
    form.quota_sick = res.data.quota_sick || 0;
    form.quota_vacation = res.data.quota_vacation || 0;
    form.quota_other = res.data.quota_other || 0;
    form.department = res.data.department || { id: null, name_th: '' };
    showEditModal.value = true;
  } catch (err) {
    console.error(err);
    alert("โหลดข้อมูลไม่สำเร็จ");
  }
};

const saveEdit = async () => {
  try {
    const payload = {
      email: form.email,
      phone_number: form.phone_number,
      role: form.role,
      groups: form.position ? [form.position] : [],
      status: form.status,
      department: form.department.id || null,
      quota_casual: form.quota_casual,
      quota_sick: form.quota_sick,
      quota_vacation: form.quota_vacation,
      quota_other: form.quota_other
    };

    await axios.patch(`http://localhost:8000/api/users/${form.id}/`, payload);
    alert("แก้ไขข้อมูลสำเร็จ");
    showEditModal.value = false;
    loadEmployees();
  } catch (err: any) {
    console.error(err.response?.data || err);
    alert("แก้ไขไม่สำเร็จ: " + JSON.stringify(err.response?.data));
  }
};

const deleteEmployee = async (id: number) => {
  if (!confirm("คุณต้องการลบพนักงานคนนี้หรือไม่?")) return;
  try {
    await axios.delete(`http://localhost:8000/api/users/${id}/`);
    employees.value = employees.value.filter(emp => emp.id !== id);
    alert("ลบพนักงานสำเร็จ");
  } catch (err) {
    console.error(err);
    alert("ไม่สามารถลบได้");
  }
};

onMounted(async () => {
  token.value = localStorage.getItem("token");
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
    await loadEmployees();
    loadGroups();
    loadDepartments();
  } catch (err) {
    console.error(err);
    router.push('/login');
  }

  document.addEventListener('click', handleBodyClick);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleBodyClick);
});

const filteredEmployees = computed(() => {
  if (!search.value) return employees.value;
  return employees.value.filter(emp =>
    (emp.firstname_th + " " + emp.lastname_th).includes(search.value) ||
    emp.email.includes(search.value) ||
    (emp.employee_code || "").includes(search.value)
  );
});

function logout() {
  if (typeof window !== "undefined") localStorage.removeItem("token")
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

.logo {
  width: 40px;
  height: 40px;
  margin-right: 10px;
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
  justify-content: space-between;
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

.nav-item.has-submenu .arrow {
  transition: transform 0.3s ease-in-out;
}

.nav-item.has-submenu.active .arrow {
  transform: rotate(90deg);
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
  position: relative;
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

.left-section {
  display: flex;
  align-items: center;
}

.title-icon {
  font-size: 24px;
  color: #888;
  margin-right: 10px;
}

h2 {
  margin: 0;
  font-size: 20px;
}

.add-button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.add-button:hover {
  background-color: #45a049;
}

.search-and-table-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.search-bar-container {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 10px;
}

.search-input {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 8px 12px;
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

/* modal style */
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
.btn-cancel{
  background:#6c757d;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  }
</style>