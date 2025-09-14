<template>
  <div class="full-page-container">
    <header class="app-header">
      <div class="header-content">
        <span>ระบบงานศูนย์วิจัยเทคโนโลยีเพื่อสิ่งแวดล้อม คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเชียงใหม่</span>
      </div>
    </header>

    <div class="content-wrapper">
      <div class="password-reset-card">
        <div class="card-header">
          <h2 class="card-title">Trouble logging in?</h2>
          <p class="card-subtitle">
            Enter your email, phone, or username and we'll send you a link to get back into your account.
          </p>
        </div>

        <div class="card-body">
          <input v-model="email" type="text" class="email-input" placeholder="Enter your email" />
          <button class="send-email-button" @click="handleForgotPassword">
            Send email
          </button>
          <p v-if="message" class="success-message">{{ message }}</p>
        </div>

        <NuxtLink to="/login" class="login-link-btn">
            Back to login
        </NuxtLink>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";

const email = ref("");
const message = ref("");

async function handleForgotPassword() {
  try {
    await axios.post("http://localhost:8000/api/users/password-reset/", {
      email: email.value,
    });
    message.value = "📩 เราส่งลิ้งสำหรับรีเซ็ตรหัสผ่านไปที่อีเมลแล้ว";
  } catch (err) {
    console.error(err);
    message.value = "❌ ไม่พบอีเมลนี้ในระบบ หรือเกิดข้อผิดพลาด";
  }
}
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;700&display=swap');

* {
  box-sizing: border-box;
  font-family: 'Inter', 'Prompt', sans-serif;
}

body, html {
  margin: 0;
  padding: 0;
  height: 100%;
}

.full-page-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f0f2f5;
}

.app-header {
  background-color: #093273;
  color: white;
  padding: 15px 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  text-align: left;
}

.content-wrapper {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.password-reset-card {
  background-color: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 450px;
  text-align: center;
}

.card-header {
  margin-bottom: 20px;
}

.lock-icon {
  font-size: 50px;
  color: #555;
  margin-bottom: 15px;
}

.card-title {
  font-size: 24px;
  font-weight: bold;
  margin: 0;
}

.card-subtitle {
  font-size: 14px;
  color: #666;
  margin: 10px 0 0;
  line-height: 1.5;
}

.card-body {
  margin-bottom: 20px;
}

.email-input {
  width: 100%;
  padding: 10px 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
  margin-bottom: 10px;
}

.success-message {
  color: #28a745;
  font-size: 12px;
  margin: 10px 0;
}

.send-email-button {
  width: 100%;
  padding: 12px;
  background-color: #133a79;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.send-email-button:hover {
  background-color: #0f2e59;
}

.login-link-btn {
  display: block;
  width: 100%;
  padding: 12px;
  background-color: #e9ecef;
  color: #555;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
  text-decoration: none;
  text-align: center;
  margin-top: 20px;
}

.login-link-btn:hover {
  background-color: #dee2e6;
}

</style>