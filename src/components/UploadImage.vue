<template>
  <div class="upload-image-wrapper">
    <div class="avatar-uploader" role="button" tabindex="0" @click="openDialog" @keydown.enter="openDialog" @keydown.space.prevent="openDialog">
      <img v-if="modelValue" :src="modelValue" class="avatar" />
      <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
    </div>

    <!-- 素材库弹窗 -->
    <el-dialog title="选择图片 (素材库)" v-model="dialogVisible" width="800px" append-to-body>
      <div class="material-header">
        <el-upload
          action="/api/admin/system/attachment/upload"
          :show-file-list="false"
          :on-success="handleUploadSuccess"
          :on-error="handleUploadError"
          :before-upload="beforeUpload"
          accept="image/*"
          name="file"
        >
          <el-button type="primary">点击上传新图片</el-button>
        </el-upload>
      </div>
      
      <div class="material-list" v-loading="loading">
        <div 
          v-for="item in attachmentList" 
          :key="item.attId" 
          class="material-item"
          :class="{ active: selectedUrl === item.sattDir }"
          @click="selectImage(item.sattDir)"
        >
          <el-image :src="item.sattDir" fit="cover" class="material-img" lazy />
          <div class="material-name" :title="item.name">{{ item.name }}</div>
          <div class="active-mask" v-if="selectedUrl === item.sattDir">
            <el-icon><Select /></el-icon>
          </div>
        </div>
      </div>
      
      <div class="pagination-wrapper" v-if="total > 0">
        <el-pagination
          background
          layout="prev, pager, next"
          :total="total"
          :page-size="limit"
          v-model:current-page="page"
          @current-change="fetchAttachments"
        />
      </div>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmSelection" :disabled="!selectedUrl">确定选择</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, watch, inject } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Select } from '@element-plus/icons-vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])
const axios = inject('axios') || window.axios // fallback if not provided

const dialogVisible = ref(false)
const loading = ref(false)
const attachmentList = ref([])
const total = ref(0)
const page = ref(1)
const limit = ref(18)
const selectedUrl = ref('')

const openDialog = () => {
  selectedUrl.value = props.modelValue || ''
  dialogVisible.value = true
  if (attachmentList.value.length === 0) {
    fetchAttachments()
  }
}

const fetchAttachments = async () => {
  loading.value = true
  try {
    // We assume axios is globally available or injected
    const res = await axios.get('/api/admin/system/attachment/list', {
      params: { page: page.value, limit: limit.value }
    })
    if (res.data && res.data.code === 200) {
      attachmentList.value = res.data.data.records || []
      total.value = res.data.data.total || 0
    }
  } catch (error) {
    console.error('获取素材失败', error)
  } finally {
    loading.value = false
  }
}

const selectImage = (url) => {
  selectedUrl.value = url
}

const confirmSelection = () => {
  emit('update:modelValue', selectedUrl.value)
  dialogVisible.value = false
}

const handleUploadSuccess = (res, file) => {
  if (res.code === 200 && res.data) {
    ElMessage.success('上传成功')
    selectedUrl.value = res.data.sattDir || res.data.attDir
    // 刷新列表以显示最新上传的图片
    page.value = 1
    fetchAttachments()
  } else {
    ElMessage.error(res.msg || '上传失败')
  }
}

const handleUploadError = (err, file, fileList) => {
  console.error('Upload Error:', err)
  ElMessage.error('网络请求失败或接口不可用，请检查控制台网络面板')
}

const beforeUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 5 // Changed to 5MB

  if (!isImage) {
    ElMessage.error('上传文件只能是图片格式!')
  }
  if (!isLt2M) {
    ElMessage.error('上传图片大小不能超过 5MB!')
  }
  return isImage && isLt2M
}
</script>

<style scoped>
.upload-image-wrapper {
  display: inline-block;
}

.avatar-uploader {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
  display: inline-block;
  background-color: #fafafa;
}

.avatar-uploader:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
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
  object-fit: cover;
}

.material-header {
  margin-bottom: 15px;
  display: flex;
  justify-content: flex-end;
}

.material-list {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 10px;
  min-height: 200px;
  max-height: 400px;
  overflow-y: auto;
}

.material-item {
  position: relative;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
}

.material-item:hover {
  box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
}

.material-item.active {
  border-color: var(--el-color-primary);
}

.material-img {
  width: 100%;
  height: 100px;
  display: block;
}

.material-name {
  font-size: 12px;
  padding: 5px;
  text-align: center;
  color: #606266;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  background-color: #f5f7fa;
}

.active-mask {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
  color: #fff;
  font-size: 30px;
}

.pagination-wrapper {
  margin-top: 15px;
  display: flex;
  justify-content: center;
}
</style>
