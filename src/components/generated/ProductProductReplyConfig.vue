<template>
  <div>
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>商品评论设置</span>
        </div>
      </template>

      <el-form ref="formRef" :model="form" label-width="200px" style="max-width: 600px;" v-loading="loading">
        <!-- 积分奖励配置 -->
        <el-divider content-position="left">评价积分奖励</el-divider>
        <el-form-item label="评价积分奖励开关">
          <el-switch v-model="form.reply_point_switch" active-value="1" inactive-value="0" />
          <div style="color: #999; font-size: 12px; line-height: 1.5; margin-top: 5px;">
            开启后用户评价商品将获得积分奖励
          </div>
        </el-form-item>
        <el-form-item label="单次评价赠送积分" v-if="form.reply_point_switch === '1'">
          <el-input-number v-model="form.reply_point_once" :min="0" />
        </el-form-item>
        <el-form-item label="每天最多赠送积分次数" v-if="form.reply_point_switch === '1'">
          <el-input-number v-model="form.reply_point_day" :min="0" />
        </el-form-item>

        <!-- 经验奖励配置 -->
        <el-divider content-position="left">评价经验奖励</el-divider>
        <el-form-item label="评价经验奖励开关">
          <el-switch v-model="form.reply_exp_switch" active-value="1" inactive-value="0" />
          <div style="color: #999; font-size: 12px; line-height: 1.5; margin-top: 5px;">
            开启后用户评价商品将获得经验奖励
          </div>
        </el-form-item>
        <el-form-item label="单次评价赠送经验" v-if="form.reply_exp_switch === '1'">
          <el-input-number v-model="form.reply_exp_once" :min="0" />
        </el-form-item>
        <el-form-item label="每天最多赠送经验次数" v-if="form.reply_exp_switch === '1'">
          <el-input-number v-model="form.reply_exp_day" :min="0" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm">保存设置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, inject } from 'vue'
import { ElMessage } from 'element-plus'

const axios = inject('axios')
const loading = ref(false)

const form = reactive({
  reply_point_switch: '0',
  reply_point_once: 0,
  reply_point_day: 0,
  reply_exp_switch: '0',
  reply_exp_once: 0,
  reply_exp_day: 0
})

const fetchConfig = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/system/config/reply_config')
    if (res.data.code === 200 && res.data.data) {
      const config = res.data.data
      form.reply_point_switch = config.reply_point_switch || '0'
      form.reply_point_once = Number(config.reply_point_once) || 0
      form.reply_point_day = Number(config.reply_point_day) || 0
      form.reply_exp_switch = config.reply_exp_switch || '0'
      form.reply_exp_once = Number(config.reply_exp_once) || 0
      form.reply_exp_day = Number(config.reply_exp_day) || 0
    }
  } catch (error) {
    ElMessage.error('获取配置失败')
  } finally {
    loading.value = false
  }
}

const submitForm = async () => {
  try {
    const res = await axios.post(`/api/admin/system/config/reply_config/save`, form)
    if (res.data.code === 200) {
      ElMessage.success('保存成功')
      fetchConfig()
    } else {
      ElMessage.error(res.data.msg || '保存失败')
    }
  } catch(e) {
    ElMessage.error('网络错误')
  }
}

onMounted(() => {
  fetchConfig()
})
</script>

<style scoped>
.box-card {
  margin: 20px;
}
.card-header {
  font-weight: bold;
}
</style>
