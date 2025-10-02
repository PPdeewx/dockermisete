<template>
    <TopBar>
        <template #breadcrumbs>
            <Breadcrumb :model="items"/>
        </template>
    </TopBar>

    <div class="dashboard-container">
        <div class="content-container">
            <div class="table-header">
                <h2>เปลี่ยนสถานะพนักงาน</h2>
                <div class="header-actions">
                    <div class="search-container">
                        <span>ค้นหาพนักงาน :</span>
                        <input type="text" v-model="searchQuery" placeholder="ค้นหา..." @input="debounceSearch" />
                    </div>
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
                        <tr v-for="(employee, index) in filteredEmployees" :key="employee.id">
                            <td>{{ index + 1 }}</td>
                            <td>{{ employee.employee_code }}</td>
                            <td>{{ employee.firstname_th }} {{ employee.lastname_th }}</td>
                            <td>{{ employee.email }}</td>
                            <td>{{ employee.groupName || '-' }}</td>
                            <td>{{ employee.phone_number }}</td>
                            <td>{{ employee.status === 'active' ? 'พนักงานปัจจุบัน' : 'ลาออก' }}</td>
                            <td>
                                <select v-model="employee.newStatus" @change="openConfirmDialog(employee)">
                                    <option value="active">พนักงานปัจจุบัน</option>
                                    <option value="resigned">ลาออก</option>
                                </select>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click="closeModal">
        <div class="modal-dialog" @click.stop>
            <div class="modal-header">
                <h3>ยืนยันการเปลี่ยนสถานะ</h3>
                <button class="btn-close" @click="closeModal"><i class="fas fa-times"></i></button>
            </div>
            <div class="modal-body">
                <p v-if="currentEmployee">ยืนยันการเปลี่ยนสถานะของ <strong>{{ currentEmployee.firstname_th }} {{ currentEmployee.lastname_th }}</strong> เป็น "<strong>{{ currentEmployee.newStatus === 'active' ? 'พนักงานปัจจุบัน' : 'ลาออก' }}</strong>"?</p>
                <p v-else>เกิดข้อผิดพลาด กรุณาลองอีกครั้ง</p>
            </div>
            <div class="modal-footer">
                <button class="btn-cancel" @click="closeModal">ยกเลิก</button>
                <button class="btn-confirm" @click="confirmStatusChange" :disabled="isSaving">ยืนยัน{{ isSaving ? '...' : '' }}</button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import TopBar from '~/components/Topbar.vue'
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Breadcrumb from 'primevue/breadcrumb'
import type { MenuItem } from 'primevue/menuitem'

const items: MenuItem[] = [
    { label: 'บุคลากร', url: '/person' },
    { label: 'เปลี่ยนสถานะพนักงาน', url: '/admin' }
]

const searchQuery = ref('')
const employees = ref([])
const router = useRouter()
const token = ref<string | null>(null)
const currentUser = ref<any>(null)
const showModal = ref(false)
const currentEmployee = ref<any>(null)
const isSaving = ref(false)

const loadEmployees = async () => {
    try {
        const res = await axios.get('http://localhost:8000/api/users/filter/', {
            headers: {
                Authorization: `Token ${localStorage.getItem('token')}`,
            },
            params: { status: '' },
        })
        employees.value = res.data.map(emp => ({
            ...emp,
            newStatus: emp.status,
            groupName: emp.groups?.[0] || '-'
        }))
    } catch (err) {
        console.error('Error loading employees:', err)
        alert('ไม่สามารถโหลดข้อมูลพนักงานได้ กรุณาลองใหม่')
    }
}

const filteredEmployees = computed(() => {
    if (!searchQuery.value) return employees.value
    const query = searchQuery.value.trim().toLowerCase()
    return employees.value.filter(emp =>
        [
            emp.firstname_th?.toLowerCase(),
            emp.lastname_th?.toLowerCase(),
            emp.employee_code?.toLowerCase(),
            emp.email?.toLowerCase(),
            emp.groupName?.toLowerCase(),
            emp.phone_number?.toLowerCase()
        ].some(field => field && field.includes(query))
    )
})

const debounce = (fn: Function, delay: number) => {
    let timeoutId: NodeJS.Timeout | null = null
    return (...args: any[]) => {
        if (timeoutId) clearTimeout(timeoutId)
        timeoutId = setTimeout(() => fn(...args), delay)
    }
}

const debounceSearch = debounce(() => {
}, 300)

const openConfirmDialog = (employee: any) => {
    currentEmployee.value = employee
    showModal.value = true
}

const closeModal = () => {
    if (currentEmployee.value) {
        currentEmployee.value.newStatus = currentEmployee.value.status
    }
    showModal.value = false
    currentEmployee.value = null
}

const confirmStatusChange = async () => {
    if (!currentEmployee.value) {
        alert('ไม่พบข้อมูลพนักงาน กรุณาลองใหม่')
        closeModal()
        return
    }

    isSaving.value = true
    try {
        const payload: any = { status: currentEmployee.value.newStatus }
        if (currentEmployee.value.newStatus === 'resigned') {
            payload.exit_date = new Date().toISOString().split('T')[0]
        }
        await axios.patch(`http://localhost:8000/api/users/${currentEmployee.value.id}/`, payload, {
            headers: { Authorization: `Token ${localStorage.getItem('token')}` },
        })
        currentEmployee.value.status = currentEmployee.value.newStatus
        alert('เปลี่ยนสถานะเรียบร้อยแล้ว')
        closeModal()
    } catch (err: any) {
        console.error('Error saving status:', err)
        alert(err.response?.data?.detail || 'เกิดข้อผิดพลาดในการเปลี่ยนสถานะ กรุณาลองใหม่')
    } finally {
        isSaving.value = false
    }
}

onMounted(async () => {
    loadEmployees()
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
        currentUser.value = me.data
        if (currentUser.value.role !== 'admin') {
            router.push('/login')
            return
        }
    } catch (err) {
        console.error('Error fetching user:', err)
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

.dashboard-container {
    padding: 20px;
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
    transition: border-color 0.3s;
}

.search-container input:focus {
    border-color: #4CAF50;
    outline: none;
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
    font-weight: 600;
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
    background-color: #fff;
    cursor: pointer;
}

/* Modal Styles */
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
    z-index: 1000;
    animation: fadeIn 0.3s ease-in-out;
}

.modal-dialog {
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    width: 90%;
    max-width: 500px;
    max-height: 80vh;
    overflow-y: auto;
    animation: slideIn 0.3s ease-in-out;
}

.modal-header {
    padding: 20px;
    border-bottom: 1px solid #eee;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.modal-header h3 {
    margin: 0;
    color: #333;
    font-size: 20px;
}

.btn-close {
    background: none;
    border: none;
    font-size: 16px;
    cursor: pointer;
    color: #888;
    transition: color 0.3s;
}

.btn-close:hover {
    color: #333;
}

.modal-body {
    padding: 20px;
    text-align: center;
}

.modal-body p {
    margin: 0 0 20px 0;
    line-height: 1.5;
    color: #555;
}

.modal-footer {
    padding: 15px 20px;
    border-top: 1px solid #eee;
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}

.btn-confirm, .btn-cancel {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    font-size: 14px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.btn-confirm {
    background-color: #4CAF50;
    color: white;
}

.btn-confirm:hover {
    background-color: #45a049;
}

.btn-confirm:disabled {
    background-color: #a5d6a7;
    cursor: not-allowed;
}

.btn-cancel {
    background-color: #f44336;
    color: white;
}

.btn-cancel:hover {
    background-color: #da190b;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideIn {
    from { transform: translateY(-20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}
</style>