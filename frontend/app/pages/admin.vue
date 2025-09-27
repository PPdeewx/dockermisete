<template>
  <div class="full-page-container">
    <Sidebar />
    <div class="main-content">
      <TopBar />

      <div class="dashboard-container">

        <Card class="mb-3">
          <template #title>ประกาศ</template>
          <ul>
            <li v-for="(item, i) in announcements" :key="i">
              <strong>{{ item.title }}</strong> - {{ item.date }} {{ item.time }}
            </li>
          </ul>
        </Card>

        <DataTable :value="activities" tableStyle="min-width: 50rem" showGridlines stripedRows>
          <Column field="date" header="วันที่"></Column>
          <Column field="employee" header="พนักงาน"></Column>
          <Column field="type" header="ประเภท"></Column>
          <Column field="period" header="ช่วงเวลา"></Column>
          <Column field="status" header="สถานะ"></Column>
          <Column field="reason" header="เหตุผล"></Column>
        </DataTable>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Sidebar from '~/components/Sidebar.vue'
import TopBar from '~/components/Topbar.vue'

const announcements = ref([
  { title: 'การใช้งานระบบเบื้องต้น', date: '26 Mar 2025', time: '08:30 AM' },
  { title: 'การใช้งานตัวอื่นๆ', date: '26 Mar 2025', time: '16:30 PM' },
  { title: 'รายงานปัญหาการใช้งานระบบ', date: '26 Mar 2025', time: '17:00 PM' }
])

const activities = ref([
  { date: '2025-12-13', employee: 'Username', type: 'ลาป่วย', period: 'ทั้งวัน', status: 'รออนุมัติ', reason: 'ไม่สบาย' },
  { date: '2025-12-14', employee: 'Username', type: 'ลากิจ', period: 'ครึ่งวันเช้า', status: 'อนุมัติ', reason: 'ธุระส่วนตัว' },
  { date: '2025-12-15', employee: 'Username', type: 'ทำงานนอกสถานที่', period: 'ทั้งวัน', status: 'อนุมัติ', reason: 'ประชุมลูกค้า' }
])

console.log("announcements:", announcements.value)
console.log("activities:", activities.value)
</script>


<style scoped>
.full-page-container {
  display: flex;
  height: 100vh;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  padding: 1rem;
}

.dashboard-container {
  padding: 1rem 0;
}

.mb-3 {
  margin-bottom: 1rem;
}
</style>
