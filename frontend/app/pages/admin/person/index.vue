<template>
    <TopBar > <template #breadcrumbs>
              <Breadcrumb  :model="items"/>

    </template></TopBar>

  <div class="dashboard-container">


    <Card class="mb-3">
      <template #title>ประกาศ</template>
      <ul>
        <li v-for="(item, i) in announcements" :key="i">
          <strong>{{ item.title }}</strong> - {{ item.date }} {{ item.time }}
        </li>
      </ul>
    </Card>
    <Card>
      <template #title>
        พนักงานปัจจุบัน
        <Button icon="pi pi-plus" label="เพิ่มพนักงาน" class="p-button-success p-ml-2" @click="goToAdd"/>
      </template>

      <div class="p-mb-3 p-d-flex p-jc-end">
        <span class="p-mr-2">ค้นหา:</span>
        <InputText v-model="search" placeholder="ค้นหา..." class="p-inputtext-sm" />
      </div>

      <DataTable :value="filteredEmployees" tableStyle="min-width: 50rem" stripedRows responsiveLayout="scroll">
        <Column header="ลำดับที่" :body="(_, { rowIndex }) => rowIndex + 1" style="width: 60px" />
        <Column field="employee_code" header="รหัส" />
        <Column field="username" header="Username" />
        <Column field="department.name_th" header="Lab" />
        <Column header="ชื่อภาษาไทย" :body="emp => emp.firstname_th + ' ' + emp.lastname_th" />
        <Column field="phone_number" header="เบอร์โทรศัพท์" />
        <Column field="email" header="Email" />

        
        <Column header="Actions" style="width: 180px">
          <template #body="slotProps">
            <Button icon="pi pi-eye" class="p-button-text" @click="viewEmployee(slotProps.data.id)" />
            <Button icon="pi pi-pencil" class="p-button-text" @click="editEmployee(slotProps.data.id)" />
            <Button icon="pi pi-trash" class="p-button-text p-button-danger" @click="deleteEmployee(slotProps.data.id)" />
          </template>
        </Column>
      </DataTable>
    </Card>
  </div>
</template>

<script setup lang="ts">
import TopBar from '~/components/Topbar.vue'

import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

import Card from 'primevue/card'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'

import Breadcrumb from 'primevue/breadcrumb';

import type { MenuItem } from 'primevue/menuitem';

const items : MenuItem[] = [
  {
    label : 'บุคลากร',url : '/person'
  },
  {
    label : 'พนักงานปัจจุบัน',url : '/person'
  }
]

const router = useRouter()
const search = ref('')
const showEditModal = ref(false)

const employees = ref<any[]>([])
const filteredEmployees = computed(() => {
  if (!search.value) return employees.value
  return employees.value.filter(emp =>
    (emp.firstname_th + ' ' + emp.lastname_th).includes(search.value) ||
    emp.email.includes(search.value) ||
    (emp.employee_code || '').includes(search.value)
  )
})


const announcements = ref([
  { title: 'การใช้งานระบบเบื้องต้น', date: '26 Mar 2025', time: '08:30 AM' },
  { title: 'การใช้งานตัวอื่นๆ', date: '26 Mar 2025', time: '16:30 PM' },
  { title: 'รายงานปัญหาการใช้งานระบบ', date: '26 Mar 2025', time: '17:00 PM' }
])

const goTo = (path: string) => router.push(path)
const goToAdd = () => router.push('/admin6')
const logout = () => {
  localStorage.removeItem('token')
  delete axios.defaults.headers.common['Authorization']
  router.push('/login')
}

const viewEmployee = (id: number) => router.push(`/admin24/${id}`)

const editEmployee = async (id: number) => {
  const res = await axios.get(`http://localhost:8000/api/users/${id}/`)
  console.log('Edit:', res.data) 
  showEditModal.value = true
}

const deleteEmployee = async (id: number) => {
  if (!confirm('คุณต้องการลบพนักงานคนนี้หรือไม่?')) return
  await axios.delete(`http://localhost:8000/api/users/${id}/`)
  employees.value = employees.value.filter(emp => emp.id !== id)
}

const loadEmployees = async () => {
  const res = await axios.get('http://localhost:8000/api/users/filter/?status=active')
  employees.value = res.data
}

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) return router.push('/login')
  axios.defaults.headers.common['Authorization'] = `Token ${token}`
  await loadEmployees()
})
</script>

