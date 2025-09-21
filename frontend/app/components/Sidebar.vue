<template>
  <div class="sidebar">
    <div class="sidebar-header">
      <span>MIS ETE</span>
    </div>
    <ul class="nav-menu">
      <li class="nav-item">
        <a @click.prevent="goTo('/')" class="nav-link"><i class="fas fa-home"></i> หน้าหลัก</a>
      </li>
      <li class="nav-item has-submenu">
        <a @click.prevent="goTo('/admin2')" class="nav-link"><i class="fas fa-users"></i> บุคลากร</a>
      </li>
      <li class="nav-item">
        <a @click.prevent="goTo('/admin10')" class="nav-link"><i class="fas fa-flask"></i> ห้องวิจัย</a>
      </li>
      <li class="nav-item">
        <a @click.prevent="goTo('/admin11')" class="nav-link"><i class="fas fa-calendar-alt"></i> วันหยุด</a>
      </li>
      <li class="nav-item">
        <a @click.prevent="goTo('/admin12')" class="nav-link"><i class="fas fa-cog"></i> ระบบการปฏิบัติงาน</a>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()
const goTo = (path: string) => {
  router.push(path)
}
</script>

<style scoped>

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
  cursor: pointer;
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
</style>
