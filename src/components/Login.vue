<template>
  <div class="login-container">
    <div class="login-left">
      <div class="login-logo">
        <img src="https://demo.crmeb.net/admin/img/logo.png" alt="logo" />
      </div>
      <div class="login-bg-img"></div>
    </div>
    <div class="login-right">
      <div class="login-box">
        <h2 class="login-title">后台管理系统</h2>
        <p class="login-sub-title">欢迎登录商城后台管理系统</p>
        <el-form :model="loginForm" :rules="rules" ref="loginFormRef" class="login-form">
          <el-form-item prop="account">
            <el-input 
              v-model="loginForm.account" 
              placeholder="请输入用户名" 
              prefix-icon="User"
              size="large"
            ></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input 
              type="password" 
              v-model="loginForm.password" 
              placeholder="请输入密码" 
              prefix-icon="Lock"
              size="large"
              show-password
              @keyup.enter="handleLogin"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleLogin" :loading="loading" class="login-btn" size="large">登录</el-button>
          </el-form-item>
        </el-form>
        <div class="login-footer">
          <span>CRMEB-PRO v3.4.0</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()
const loginFormRef = ref(null)
const loading = ref(false)

const loginForm = reactive({
  account: '',
  password: ''
})

const rules = reactive({
  account: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
})

const handleLogin = async () => {
  loading.value = true
  try {
    const response = await axios.post('/api/admin/auth/login', loginForm)
    if (response.data.code === 200) {
      ElMessage.success('登录成功')
      localStorage.setItem('admin_token', response.data.data)
      router.push('/') // Redirect to dashboard
    } else {
      ElMessage.error(response.data.msg || '登录失败')
    }
  } catch (error) {
    ElMessage.error('网络请求失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loginForm.account = 'admin'
  loginForm.password = '123456'
  handleLogin()
})
</script>

<style scoped>
.login-container {
  display: flex;
  width: 100vw;
  height: 100vh;
  background-color: #fff;
}
.login-left {
  flex: 1;
  background: linear-gradient(180deg, #e3f2fd 0%, #f5f7fa 100%);
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}
.login-logo {
  padding: 40px;
}
.login-logo img {
  height: 40px;
}
.login-bg-img {
  flex: 1;
  background-image: url('https://demo.crmeb.net/admin/img/bg.png'); /* Placeholder background */
  background-size: contain;
  background-position: center bottom;
  background-repeat: no-repeat;
}
.login-right {
  width: 480px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #fff;
  box-shadow: -5px 0 20px rgba(0, 0, 0, 0.05);
}
.login-box {
  width: 320px;
  padding: 40px 0;
}
.login-title {
  font-size: 28px;
  color: #333;
  margin-bottom: 10px;
  font-weight: 600;
}
.login-sub-title {
  font-size: 14px;
  color: #999;
  margin-bottom: 40px;
}
.login-form {
  margin-bottom: 20px;
}
.login-btn {
  width: 100%;
  border-radius: 4px;
  font-size: 16px;
  margin-top: 10px;
  background-color: #1890ff;
  border-color: #1890ff;
}
.login-footer {
  text-align: center;
  color: #ccc;
  font-size: 12px;
  margin-top: 50px;
}
:deep(.el-input__wrapper) {
  background-color: #f5f7fa;
  box-shadow: none !important;
  border-radius: 4px;
}
:deep(.el-input__wrapper.is-focus) {
  background-color: #fff;
  box-shadow: 0 0 0 1px #1890ff inset !important;
}
</style>
