<template>
  <div class="config-container">
    <el-container class="config-layout">
      <!-- Left Sidebar for Configuration Categories -->
      <el-aside width="200px" class="config-aside">
        <el-menu :default-active="activeTab" class="config-menu" @select="handleSelectTab">
          <el-sub-menu index="system">
            <template #title>
              <el-icon><Setting /></el-icon>
              <span>系统设置</span>
            </template>
            <el-menu-item index="base">基础配置</el-menu-item>
            <el-menu-item index="upload">上传配置</el-menu-item>
          </el-sub-menu>
          <el-sub-menu index="service">
            <template #title>
              <el-icon><Service /></el-icon>
              <span>服务设置</span>
            </template>
            <el-menu-item index="sms">一号通配置</el-menu-item>
            <el-menu-item index="express">物流配置</el-menu-item>
            <el-menu-item index="payment">支付配置</el-menu-item>
          </el-sub-menu>
        </el-menu>
      </el-aside>

      <!-- Main Content Area for Configuration Form -->
      <el-main class="config-main" v-loading="loading">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <span>{{ currentTabName }}</span>
            </div>
          </template>

          <el-form label-width="150px" class="config-form">
            <!-- Render different forms based on activeTab -->
            <template v-if="activeTab === 'sms'">
              <el-alert title="一号通短信服务配置。请先在第三方平台申请账号。" type="info" show-icon style="margin-bottom: 20px" />
              <el-form-item label="短信平台状态">
                <el-radio-group v-model="smsConfig.status">
                  <el-radio :label="1">开启</el-radio>
                  <el-radio :label="0">关闭</el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="一号通账号">
                <el-input v-model="smsConfig.account" placeholder="请输入一号通账号" />
                <div class="form-tip">购买一号通服务后分配的账号</div>
              </el-form-item>
              <el-form-item label="一号通密码">
                <el-input v-model="smsConfig.password" type="password" show-password placeholder="请输入一号通密码" />
              </el-form-item>
              <el-form-item label="短信签名">
                <el-input v-model="smsConfig.sign" placeholder="请输入短信签名，例如：中农普惠" />
              </el-form-item>
            </template>

            <template v-else-if="activeTab === 'base'">
              <el-form-item label="网站名称">
                <el-input v-model="baseConfig.siteName" placeholder="请输入网站名称" />
              </el-form-item>
              <el-form-item label="网站LOGO">
                <el-upload class="avatar-uploader" action="#" :show-file-list="false">
                  <img v-if="baseConfig.logo" :src="baseConfig.logo" class="avatar" />
                  <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
                </el-upload>
              </el-form-item>
              <el-form-item label="版权信息">
                <el-input v-model="baseConfig.copyright" placeholder="请输入版权信息" />
              </el-form-item>
              <el-form-item label="备案号">
                <el-input v-model="baseConfig.icp" placeholder="请输入备案号" />
              </el-form-item>
            </template>
            
            <template v-else>
              <el-empty :description="`${currentTabName} 尚未实现具体字段，等待后端接入`" />
            </template>

            <el-form-item v-if="activeTab === 'sms' || activeTab === 'base'">
              <el-button type="primary" @click="saveAllConfig">提交</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Setting, Service, Plus } from '@element-plus/icons-vue'
import axios from 'axios'

const loading = ref(false)
const activeTab = ref('sms')

const tabNames = {
  base: '基础配置',
  upload: '上传配置',
  sms: '一号通配置',
  express: '物流配置',
  payment: '支付配置'
}

const currentTabName = computed(() => tabNames[activeTab.value] || '系统配置')

const smsConfig = ref({
  status: 1,
  account: '',
  password: '',
  sign: '中农普惠'
})

const baseConfig = ref({
  siteName: '中农普惠商城',
  logo: 'https://demo.crmeb.net/admin/img/logo.png',
  copyright: 'Copyright © 2023 中农普惠',
  icp: '京ICP备12345678号'
})

const handleSelectTab = (index) => {
  activeTab.value = index
}

const fetchConfigs = async () => {
  loading.value = true
  try {
    // 模拟获取配置
    await new Promise(resolve => setTimeout(resolve, 500))
  } catch (error) {
    ElMessage.error('获取配置失败')
  } finally {
    loading.value = false
  }
}

const saveAllConfig = async () => {
  loading.value = true
  try {
    // 模拟保存配置
    await new Promise(resolve => setTimeout(resolve, 800))
    ElMessage.success('配置提交成功')
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchConfigs()
})
</script>

<style scoped>
.config-container {
  height: 100%;
}
.config-layout {
  height: 100%;
  background-color: #fff;
  border-radius: 4px;
}
.config-aside {
  border-right: 1px solid #e6e6e6;
}
.config-menu {
  border-right: none;
}
.config-main {
  padding: 20px;
}
.card-header {
  font-weight: bold;
}
.config-form {
  max-width: 800px;
}
.form-tip {
  font-size: 12px;
  color: #999;
  line-height: 1.5;
  margin-top: 5px;
}
.avatar-uploader {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}
.avatar-uploader:hover {
  border-color: var(--el-color-primary);
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  text-align: center;
  line-height: 100px;
}
.avatar {
  width: 100px;
  height: 100px;
  display: block;
}
</style>
