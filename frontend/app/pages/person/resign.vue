<template>
    <TopBar > <template #breadcrumbs>
              <Breadcrumb  :model="items"/>

    </template></TopBar>

  <div class="dashboard-container">


      <Card>
        <template #title>
          พนักงานที่ลาออก
          <Button
            icon="pi pi-plus"
            label="เปลี่ยนสถานะ"
            class="p-button-success p-ml-2"
            @click="goTo('/admin8')"
          />
        </template>

        <div class="p-inputgroup p-mb-3">
          <span class="p-inputgroup-addon">SEARCH</span>
          <InputText v-model="search" placeholder="ค้นหาพนักงาน..." />
        </div>

        <DataTable :value="resignedEmployees" stripedRows responsiveLayout="scroll">
          <Column header="ลำดับ" :body="(_, { rowIndex }) => rowIndex + 1" style="width: 60px" />
          <Column field="employee_code" header="รหัส" />
          <Column field="username" header="Username" />
          <Column field="groupName" header="Lab" />
          <Column header="ชื่อภาษาไทย" :body="emp => emp.firstname_th + ' ' + emp.lastname_th" />
          <Column field="phone_number" header="เบอร์โทรศัพท์" />
          <Column field="email" header="Email" />
          <Column header="Actions" style="width: 180px">
            <template #body="slotProps">
              <Button
                label="เปลี่ยนสถานะ"
                icon="pi pi-refresh"
                class="p-button-success p-button-sm"
                @click="reinstateEmployee(slotProps.data)"
              />
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
    label : 'บุคลากร',url : '/admin'
  },
  {
    label : 'พนักงานที่ลาออก',url : '/admin'
  }
]

const router = useRouter()
const search = ref('')
const employees = ref<any[]>([])

const goTo = (path: string) => router.push(path)

const resignedEmployees = computed(() =>
  employees.value.filter(emp => emp.status === 'resigned')
)

const loadEmployees = async () => {
  const token = localStorage.getItem('token')
  if (!token) return router.push('/login')

  const res = await axios.get('http://localhost:8000/api/users/filter/?status=resigned', {
    headers: { Authorization: `Token ${token}` }
  })
  employees.value = res.data.map(emp => ({
    ...emp,
    groupName: emp.groups?.[0] || '-'
  }))
}

const reinstateEmployee = async (emp: any) => {
  await axios.patch(`http://localhost:8000/api/users/${emp.id}/`, { status: 'active', exit_date: null })
  emp.status = 'active'
}

onMounted(async () => {
  await loadEmployees()
})
</script>

<style scoped>
.full-page-container {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding: 1rem;
  background: #f8f9fa;
}
</style>
