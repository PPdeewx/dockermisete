<template>
    <TopBar>
        <template #breadcrumbs>
            <Breadcrumb :model="items"/>
        </template>
    </TopBar>

    <div class="content-container">
        <div class="header-with-buttons">
            <h2>ขอลาให้คนอื่น</h2>
            <button class="btn-cancel" @click="goToAdminPage">ยกเลิก</button>
        </div>

        <div class="form-section">
            <form @submit.prevent="submitForm">
                <div class="form-grid">
                    <div class="form-group full-width">
                        <label for="submitter-name">พนักงานผู้ยื่นลา <span class="required">*</span></label>
                        <div class="read-only-text">{{ currentUser?.name || 'กำลังโหลด...' }}</div>
                    </div>

                    <div class="form-group full-width">
                        <label for="employee-name">พนักงานผู้ลา <span class="required">*</span></label>
                        <AutoComplete
                            id="employee-name"
                            v-model="leaveForm.employee"
                            :suggestions="filteredEmployees"
                            @complete="searchEmployees($event)"
                            optionLabel="name"
                            optionValue="id"
                            placeholder="ค้นหาพนักงานผู้ลา..."
                            class="form-autocomplete"
                            :dropdown="true"
                            required
                        />
                    </div>

                    <div class="form-group full-width">
                        <label for="leave-type">ประเภทการลา <span class="required">*</span></label>
                        <div class="radio-group">
                            <label v-for="leaveType in leaveTypes" :key="leaveType.id">
                                <input type="radio" v-model="leaveForm.leaveType" :value="leaveType.id" required>
                                {{ leaveType.name }}
                            </label>
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="startDate">ตั้งแต่วันที่ <span class="required">*</span></label>
                        <input type="date" id="startDate" v-model="leaveForm.startDate" class="form-input" required>
                    </div>

                    <div class="form-group">
                        <label for="endDate">ถึงวันที่ <span class="required">*</span></label>
                        <input type="date" id="endDate" v-model="leaveForm.endDate" class="form-input" required>
                    </div>

                    <div class="form-group full-width">
                        <label>ช่วงเวลา <span class="required">*</span></label>
                        <div class="radio-group">
                            <label><input type="radio" v-model="leaveForm.timePeriod" value="morning"> ครึ่งวันเช้า</label>
                            <label><input type="radio" v-model="leaveForm.timePeriod" value="afternoon"> ครึ่งวันบ่าย</label>
                            <label><input type="radio" v-model="leaveForm.timePeriod" value="full"> ทั้งวัน</label>
                        </div>
                    </div>

                    <div class="form-group full-width">
                        <label for="reason">เหตุผลการลา <span class="required">*</span></label>
                        <textarea id="reason" v-model="leaveForm.reason" class="form-textarea" rows="3" required></textarea>
                    </div>

                    <div class="form-group full-width">
                        <label for="substitute">ผู้ปฏิบัติงานแทน</label>
                        <AutoComplete
                            id="substitute"
                            v-model="leaveForm.substitute"
                            :suggestions="filteredSubstitutes"
                            @complete="searchSubstitutes($event)"
                            optionLabel="name"
                            optionValue="id"
                            placeholder="ค้นหาผู้ปฏิบัติงานแทน..."
                            class="form-autocomplete"
                            :dropdown="true"
                        />
                    </div>

                    <div class="form-group full-width">
                        <label for="approver">หัวหน้างาน <span class="required">*</span></label>
                        <AutoComplete
                            id="approver"
                            v-model="leaveForm.approver"
                            :suggestions="filteredApprovers"
                            @complete="searchApprovers($event)"
                            optionLabel="name"
                            optionValue="id"
                            placeholder="ค้นหาหัวหน้างาน..."
                            class="form-autocomplete"
                            :dropdown="true"
                            required
                        />
                    </div>
                </div>

                <div class="form-actions">
                    <button type="submit" class="btn-submit">ยื่นคำขอ</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
import TopBar from '~/components/Topbar.vue'
import AutoComplete from 'primevue/autocomplete'
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Breadcrumb from 'primevue/breadcrumb'
import type { MenuItem } from 'primevue/menuitem'

const items: MenuItem[] = [
    { label: 'ระบบการปฏิบัติงาน', url: '/admin' },
    { label: 'ขอลาให้คนอื่น', url: '/admin' }
]

const router = useRouter()
const token = ref<string | null>(null)
const showProfileMenu = ref(false)
const currentUser = ref<any>(null)
const employeeList = ref<any[]>([])
const approverList = ref<any[]>([])
const substituteList = ref<any[]>([])
const leaveTypes = ref<any[]>([])
const filteredEmployees = ref<any[]>([])
const filteredSubstitutes = ref<any[]>([])
const filteredApprovers = ref<any[]>([])

const leaveForm = reactive({
    employee: '',
    leaveType: '',
    startDate: '',
    endDate: '',
    timePeriod: 'full',
    reason: '',
    approver: '',
    substitute: '',
    created_by_admin: true,
})

const toggleProfileMenu = () => {
    showProfileMenu.value = !showProfileMenu.value
}

const goToAdminPage = () => {
    router.push('/admin')
}

const searchEmployees = (event: any) => {
    const query = event.query.trim().toLowerCase()
    filteredEmployees.value = query
        ? employeeList.value.filter(user =>
              user.name.toLowerCase().includes(query)
          )
        : employeeList.value
}

const searchSubstitutes = (event: any) => {
    const query = event.query.trim().toLowerCase()
    filteredSubstitutes.value = query
        ? substituteList.value.filter(user =>
              user.name.toLowerCase().includes(query)
          )
        : substituteList.value
}

const searchApprovers = (event: any) => {
    const query = event.query.trim().toLowerCase()
    filteredApprovers.value = query
        ? approverList.value.filter(user =>
              user.name.toLowerCase().includes(query)
          )
        : approverList.value
}

const validateForm = () => {
    if (!leaveForm.employee) {
        alert('กรุณาเลือกพนักงานผู้ลา')
        return false
    }
    if (!leaveForm.leaveType) {
        alert('กรุณาเลือกประเภทการลา')
        return false
    }
    if (!leaveForm.startDate || !leaveForm.endDate) {
        alert('กรุณากรอกวันที่และถึงวันที่')
        return false
    }
    if (new Date(leaveForm.startDate) > new Date(leaveForm.endDate)) {
        alert('วันที่สิ้นสุดต้องไม่เร็วกว่าวันที่เริ่มต้น')
        return false
    }
    if (!leaveForm.timePeriod) {
        alert('กรุณาเลือกช่วงเวลา')
        return false
    }
    if (!leaveForm.reason) {
        alert('กรุณากรอกเหตุผลการลา')
        return false
    }
    if (!leaveForm.approver) {
        alert('กรุณาเลือกหัวหน้างาน')
        return false
    }
    return true
}

const submitForm = async () => {
    if (!validateForm()) return

    const payload = {
        on_behalf_of_id: leaveForm.employee,
        leave_type_id: leaveForm.leaveType,
        start_date: leaveForm.startDate,
        end_date: leaveForm.endDate,
        period: leaveForm.timePeriod,
        reason: leaveForm.reason,
        approver_id: leaveForm.approver,
        substitute_id: leaveForm.substitute || null,
        created_by_admin: leaveForm.created_by_admin,
    }

    try {
        const response = await axios.post(
            'http://localhost:8000/api/leave/leave-requests/',
            payload,
            {
                headers: { Authorization: `Token ${token.value}` },
            }
        )
        alert('ยื่นคำขอสำเร็จ')
        router.push('/admin14')
    } catch (error: any) {
        console.error('Error submitting form:', error.response?.data)
        alert(
            error.response?.data?.detail ||
            JSON.stringify(error.response?.data) ||
            'เกิดข้อผิดพลาดในการยื่นคำขอ'
        )
    }
}

const logout = () => {
    if (typeof window !== 'undefined') {
        localStorage.removeItem('token')
    }
    delete axios.defaults.headers.common['Authorization']
    router.push('/login')
}

onMounted(async () => {
    if (typeof window !== 'undefined') {
        token.value = localStorage.getItem('token')
    }

    if (!token.value) {
        router.push('/login')
        return
    }

    axios.defaults.headers.common['Authorization'] = `Token ${token.value}`

    try {
        const meResponse = await axios.get('http://localhost:8000/api/users/me/')
        currentUser.value = meResponse.data

        if (currentUser.value.role !== 'admin') {
            router.push('/login')
            return
        }

        const usersResponse = await axios.get('http://localhost:8000/api/users/for-list/')
        employeeList.value = usersResponse.data
            .filter((user: any) => user.id !== currentUser.value.id)
            .map((user: any) => ({
                id: user.id,
                name: user.name,
            }))
        approverList.value = usersResponse.data
            .filter((user: any) => user.role === 'admin' || user.role === 'manager')
            .map((user: any) => ({
                id: user.id,
                name: user.name,
            }))
        substituteList.value = usersResponse.data
            .filter((user: any) => user.id !== currentUser.value.id)
            .map((user: any) => ({
                id: user.id,
                name: user.name,
            }))

        const leaveTypesResponse = await axios.get('http://localhost:8000/api/leave/leave-types/')
        leaveTypes.value = leaveTypesResponse.data
        leaveForm.leaveType = leaveTypes.value.find((lt: any) => lt.name === 'ลาป่วย')?.id || ''
        if (!leaveForm.leaveType) {
            console.warn('Warning: No leave type ID found for ลาป่วย')
        }
    } catch (error) {
        console.error('Error during initialization:', error)
        router.push('/login')
    }
})

// เพิ่ม watch เพื่อตรวจสอบการเปลี่ยนแปลงของค่า
watch(() => leaveForm.employee, (newVal) => {
    if (newVal) {
        const input = document.querySelector('#employee-name .p-autocomplete-input');
        if (input) input.classList.add('has-value');
    } else {
        const input = document.querySelector('#employee-name .p-autocomplete-input');
        if (input) input.classList.remove('has-value');
    }
});
watch(() => leaveForm.substitute, (newVal) => {
    if (newVal) {
        const input = document.querySelector('#substitute .p-autocomplete-input');
        if (input) input.classList.add('has-value');
    } else {
        const input = document.querySelector('#substitute .p-autocomplete-input');
        if (input) input.classList.remove('has-value');
    }
});
watch(() => leaveForm.approver, (newVal) => {
    if (newVal) {
        const input = document.querySelector('#approver .p-autocomplete-input');
        if (input) input.classList.add('has-value');
    } else {
        const input = document.querySelector('#approver .p-autocomplete-input');
        if (input) input.classList.remove('has-value');
    }
});
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;700&display=swap');

* {
    box-sizing: border-box;
    font-family: 'Noto Sans Thai', sans-serif;
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

.btn-cancel {
    background-color: #f44336;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1em;
}

.btn-cancel:hover {
    background-color: #d32f2f;
}

.form-section {
    padding: 10px 0;
}

.form-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
}

.form-group {
    display: flex;
    flex-direction: column;
}

.form-group.full-width {
    grid-column: 1 / -1;
}

.form-group label {
    font-weight: bold;
    margin-bottom: 5px;
    display: flex;
    align-items: center;
}

.form-group label .required {
    color: red;
    margin-left: 4px;
}

.read-only-text {
    padding: 10px 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: #f5f5f5;
    color: #555;
}

.radio-group {
    display: flex;
    gap: 20px;
    align-items: center;
    flex-wrap: wrap;
}

.radio-group label {
    font-weight: normal;
    display: flex;
    align-items: center;
    gap: 5px;
    cursor: pointer;
}

.form-input,
.form-textarea {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 1em;
}

.form-input[type="date"] {
    width: auto;
}

.form-textarea {
    resize: vertical;
}

.form-autocomplete {
    width: 100%;
}

.form-autocomplete :deep(.p-autocomplete-input) {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 1em;
    background-color: #fff;
    transition: border-color 0.3s ease, background-color 0.3s ease;
}

.form-autocomplete :deep(.p-autocomplete-input.has-value) {
    background-color: #f5f5f5;
    color: #555;
    border-color: #ccc;
}

.form-autocomplete :deep(.p-autocomplete-input:focus) {
    border-color: #007bff;
    outline: none;
    box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
    background-color: #fff;
}

.form-autocomplete :deep(.p-autocomplete-input:hover) {
    border-color: #999;
}

.form-autocomplete :deep(.p-autocomplete-dropdown) {
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
    border-left: none;
    background-color: #f5f5f5;
    color: #333;
}

.form-autocomplete :deep(.p-autocomplete-panel) {
    border: 1px solid #ccc;
    border-radius: 4px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    background-color: #ffffff;
    margin-top: 4px;
    z-index: 1000;
}

.form-autocomplete :deep(.p-autocomplete-item) {
    padding: 8px 12px;
    border-bottom: 1px solid #eee;
    color: #333;
    transition: background-color 0.2s;
}

.form-autocomplete :deep(.p-autocomplete-item:hover) {
    background-color: #f5f5f5;
}

.form-autocomplete :deep(.p-autocomplete-item:last-child) {
    border-bottom: none;
}

.form-actions {
    display: flex;
    justify-content: center;
    margin-top: 30px;
}

.btn-submit {
    background-color: #52c41a;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1em;
    transition: background-color 0.2s;
}

.btn-submit:hover {
    background-color: #389e08;
}

@media (max-width: 768px) {
    .form-grid {
        grid-template-columns: 1fr;
    }
}
</style>