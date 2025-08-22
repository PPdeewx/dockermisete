<template>
  <div class="full-page-container">
    <header class="app-header">
      <div class="header-content">
        <span>ระบบงานศูนย์วิจัยเทคโนโลยีเพื่อสิ่งแวดล้อม คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเชียงใหม่</span>
      </div>
    </header>

    <div class="login-wrapper">
      <div class="login-card">
        <div class="logo">
          <img src="/ete.png" />
        </div>

        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="username">Username :</label>
            <input type="text" v-model="username" required placeholder="Enter your username" />
          </div>

          <div class="form-group">
            <label for="password">Password :</label>
            <input :type="showPassword ? 'text' : 'password'" v-model="password" required placeholder="Enter your password" />
          </div>

          <NuxtLink to="/password" class="password-link-btn">
            Forgot Password?
          </NuxtLink>

          <button type="submit" class="login-btn">
            Login
          </button>

        </form>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const username = ref('');
const password = ref('');
const showPassword = ref(false);

function handleLogin() {
  router.push({ path: '/user', query: { username: username.value } });
}



function goToRecovery() {
  router.push('/forgot-recovery');
}
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;700&display=swap');

* {
  box-sizing: border-box;
  font-family: 'Noto Sans Thai', sans-serif;
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

.login-wrapper {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.logo img {
  width: 240px;
  margin: 1rem auto;
}

.form-group {
  margin-bottom: 1.2rem;
  position: relative;
  text-align: left;
}

.form-group label {
  font-weight: bold;
  display: block;
}

.form-group input {
  width: 100%;
  padding: 0.6rem;
  font-size: 1rem;
  margin-top: 0.3rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.toggle {
  position: absolute;
  right: 10px;
  top: 34px;
  background: none;
  border: none;
  cursor: pointer;
  color: #888;
}

.login-btn {
  background-color: #0d3b66;
  color: white;
  padding: 0.6rem 1rem;
  width: 100%;
  border: none;
  border-radius: 5px;
  margin-top: 0.5rem;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
}

.or-separator {
  margin: 1rem 0;
  font-weight: bold;
  color: #888;
}

.google-login-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background-color: white;
  border: 1px solid #ccc;
  padding: 0.5rem;
  width: 100%;
  border-radius: 5px;
  cursor: pointer;
}

.google-login-btn img {
  width: 18px;
}

.forgot-password {
  text-align: right;
  font-size: 14px;
  margin-top: 5px;
  cursor: pointer;
}
</style>