<template>
  <div class="set-password-container">
    <div class="header">
      ระบบงานศูนย์วิจัยเทคโนโลยีเพื่อสิ่งแวดล้อม คณบดีวิศวกรรมศาสตร์ มหาวิทยาลัยเชียงใหม่
    </div>

    <div class="content-wrapper">
      <div class="password-box">
        <div class="profile-section">
          <div class="profile-image">
            <span class="profile-text">Profile</span>
          </div>
          <p class="user-name">นาย admin admin</p>
          <p class="user-email">asdgqwe@example.com</p>
        </div>

        <div class="set-form">
          <h2>Reset Your Password</h2>
          <p class="instruction-text">Please enter your new password below</p>

          <div class="input-group">
            <input 
              v-model="newPassword"
              :type="showNewPassword ? 'text' : 'password'" 
              placeholder="New password" 
              class="password-input"
            />
            <i class="fas password-toggle-icon" 
               :class="showNewPassword ? 'fa-eye' : 'fa-eye-slash'" 
               @click="toggleNewPassword"></i>
          </div>

          <div class="input-group">
            <input 
              v-model="confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'" 
              placeholder="Confirm new password" 
              class="password-input"
            />
            <i class="fas password-toggle-icon" 
               :class="showConfirmPassword ? 'fa-eye' : 'fa-eye-slash'" 
               @click="toggleConfirmPassword"></i>
          </div>

          <button class="set-button" @click="goToLogin">Reset password</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const newPassword = ref('');
const confirmPassword = ref('');
const showNewPassword = ref(false);
const showConfirmPassword = ref(false);

function toggleNewPassword() {
  showNewPassword.value = !showNewPassword.value;
}

function toggleConfirmPassword() {
  showConfirmPassword.value = !showConfirmPassword.value;
}

function goToLogin() {
  if (newPassword.value !== confirmPassword.value) {
    alert('Passwords do not match!');
    return;
  }
  router.push('/login');
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;700&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

.set-password-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5; 
  font-family: 'Noto Sans Thai', sans-serif;
}

.header {
  width: 100%;
  background-color: #093273; 
  color: white;
  padding: 15px 20px;
  text-align: left;
  font-size: 16px;
}

.content-wrapper {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.password-box {
  background-color: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 450px; 
}

.profile-section {
  padding-bottom: 20px;
  border-bottom: 1px solid #e0e0e0;
  margin-bottom: 20px;
}

.profile-image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 2px solid #ccc;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto 10px;
  background-color: #f7f7f7;
  color: #888;
}

.user-name {
  font-size: 18px;
  font-weight: bold;
  margin: 0;
}

.user-email {
  font-size: 14px;
  color: #777;
  margin: 5px 0 0;
}

.set-form h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 10px;
}

.instruction-text {
  font-size: 14px;
  color: #777;
  margin-bottom: 25px;
  line-height: 1.5;
}

.input-group {
  position: relative;
  margin-bottom: 15px;
}

.password-input {
  width: 100%;
  padding: 12px 40px 12px 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
  box-sizing: border-box; 
}

.password-toggle-icon {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
  cursor: pointer;
}

.set-button {
  width: 100%;
  padding: 12px;
  background-color: #3f68a8; 
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 18px;
  cursor: pointer;
  margin-top: 15px;
  transition: background-color 0.3s ease;
}

.set-button:hover {
  background-color: #305488;
}
</style>
