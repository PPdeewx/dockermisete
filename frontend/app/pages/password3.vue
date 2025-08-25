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
          <h2>Set Your Password</h2>
          <p class="instruction-text">Please create a password for your account</p>
          
          <div class="input-group">
            <input 
              :type="showPassword1 ? 'text' : 'password'" 
              placeholder="New password" 
              class="password-input" 
            />
            <i 
              :class="['fas', showPassword1 ? 'fa-eye' : 'fa-eye-slash', 'password-toggle-icon']" 
              @click="togglePasswordVisibility(1)">
            </i>
          </div>
          
          <div class="input-group">
            <input 
              :type="showPassword2 ? 'text' : 'password'" 
              placeholder="Confirm password" 
              class="password-input" 
            />
            <i 
              :class="['fas', showPassword2 ? 'fa-eye' : 'fa-eye-slash', 'password-toggle-icon']" 
              @click="togglePasswordVisibility(2)">
            </i>
          </div>

          <p class="password-hint">Your password must be at least 8 characters long and contain letters and numbers</p>
          
          <button class="set-button" @click="goToLogin">Set password</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: '6PasswordView',
  setup() {
    const showPassword1 = ref(false);
    const showPassword2 = ref(false);
    const router = useRouter();

    const togglePasswordVisibility = (inputNumber) => {
      if (inputNumber === 1) {
        showPassword1.value = !showPassword1.value;
      } else if (inputNumber === 2) {
        showPassword2.value = !showPassword2.value;
      }
    };

    const goToLogin = () => {
      // Navigate to the login page (root path)
      router.push('/');
    };

    return {
      showPassword1,
      showPassword2,
      togglePasswordVisibility,
      goToLogin,
    };
  }
};
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
  padding: 10px 20px;
  text-align: left;
  font-size: 14px;
  box-sizing: border-box;
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

.profile-text {
  font-size: 16px;
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
  text-align: left;
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
  transition: background-color 0.3s ease;
  margin-top: 15px;
}

.set-button:hover {
  background-color: #305488;
}

.password-hint {
    font-size: 12px;
    color: #999;
    margin-top: 10px;
}
</style>