<template>
  <div>
    <el-card>
      <el-form :inline="true" class="demo-form-inline">
        <el-form-item label="关键字">
          <el-input v-model="searchQuery.keyword" placeholder="请输入关键字搜索" clearable></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">搜索</el-button>
          <el-button @click="resetData">重置</el-button>
        </el-form-item>
      </el-form>
      <div style="margin-bottom: 15px;">
        <el-button type="primary" plain @click="handleAdd">新增</el-button>
        <el-button type="danger" plain @click="handleBatchDelete">批量删除</el-button>
      </div>
      <el-table :data="tableData" style="width: 100%" v-loading="loading" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column prop="name" label="表单名称" min-width="120" align="center" />
        <el-table-column prop="coverImage" label="封面图" width="100" align="center">
          <template #default="scope">
            <el-image style="width: 40px; height: 40px" :src="scope.row.coverImage" fit="contain" v-if="scope.row.coverImage" />
            <span v-else>无</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="是否使用" width="100" align="center">
          <template #default="scope">
            <el-switch v-model="scope.row.status" :active-value="1" :inactive-value="0" @change="handleStatusChange(scope.row)" />
          </template>
        </el-table-column>
        <el-table-column prop="addTime" label="创建时间" min-width="160" align="center">
          <template #default="scope">
            {{ formatTime(scope.row.addTime) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="scope">
            <el-button size="small" type="primary" link @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="primary" link @click="handleDetail(scope.row)">查看详情</el-button>
            <el-button size="small" type="danger" link @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div style="margin-top: 20px; text-align: right;">
        <el-pagination background layout="total, sizes, prev, pager, next, jumper" :total="total" />
      </div>
    </el-card>

    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px">
      <el-form label-width="100px" :model="form" ref="formRef">
        <el-form-item label="表单名称" required>
          <el-input v-model="form.name" placeholder="请输入表单名称"></el-input>
        </el-form-item>
        <el-form-item label="封面图">
          <UploadImage v-model="form.coverImage" />
        </el-form-item>
        <el-form-item label="表单数据">
          <el-input type="textarea" :rows="4" v-model="form.value" placeholder="请输入表单JSON数据"></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="form.status" :active-value="1" :inactive-value="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog title="系统表单收集数据详情" v-model="detailVisible" width="500px">
      <el-descriptions border :column="1">
        <el-descriptions-item label="ID">{{ detailData.id }}</el-descriptions-item>
        <el-descriptions-item label="表单名称">{{ detailData.name }}</el-descriptions-item>
        <el-descriptions-item label="封面图">
          <el-image style="width: 40px; height: 40px" :src="detailData.coverImage" fit="contain" v-if="detailData.coverImage" />
          <span v-else>无</span>
        </el-descriptions-item>
        <el-descriptions-item label="是否使用">
          <el-tag :type="detailData.status === 1 ? 'success' : 'danger'">{{ detailData.status === 1 ? '启用' : '禁用' }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="表单数据">
          <pre style="white-space: pre-wrap; word-wrap: break-word;">{{ detailData.value }}</pre>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ formatTime(detailData.addTime) }}</el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="detailVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, inject } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import UploadImage from '../UploadImage.vue'

const axios = inject('axios')
const tableData = ref([])
const total = ref(0)
const loading = ref(false)

const dialogVisible = ref(false)
const dialogTitle = ref('新增')
const detailVisible = ref(false)
const detailData = ref({})
const selectedRows = ref([])

const searchQuery = reactive({
  keyword: ''
})

const form = reactive({
  id: null,
  name: '',
  coverImage: '',
  value: '',
  status: 1
})

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp * 1000)
  return date.toLocaleString('zh-CN', { hour12: false }).replace(/\//g, '-')
}

const fetchData = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/system/form/index', { params: searchQuery })
    if (res.data.code === 200) {
      tableData.value = res.data.data.records || res.data.data
      total.value = res.data.data.total || res.data.data.length
    } else {
      ElMessage.error(res.data.msg || '获取数据失败')
    }
  } catch (error) {
    if (!error.response || error.response.status !== 401) {
      ElMessage.error('获取列表失败')
    }
  } finally {
    loading.value = false
  }
}

const resetData = () => {
  searchQuery.keyword = ''
  fetchData()
}

const handleSelectionChange = (val) => {
  selectedRows.value = val
}

const handleAdd = () => {
  dialogTitle.value = '添加表单'
  form.id = null
  form.name = ''
  form.coverImage = ''
  form.value = ''
  form.status = 1
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑表单'
  form.id = row.id
  form.name = row.name
  form.coverImage = row.coverImage || ''
  form.value = row.value || ''
  form.status = row.status
  dialogVisible.value = true
}

const handleDetail = (row) => {
  detailData.value = { ...row }
  detailVisible.value = true
}

const handleStatusChange = async (row) => {
  try {
    const res = await axios.post(`/api/admin/system/form/save`, row)
    if (res.data.code === 200) {
      ElMessage.success('状态修改成功')
    } else {
      ElMessage.error(res.data.msg || '状态修改失败')
    }
  } catch(e) {
    ElMessage.error('网络错误')
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除该记录吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    try {
      const res = await axios.post(`/api/admin/system/form/delete`, { id: row.id })
      if (res.data.code === 200) {
        ElMessage.success(res.data.msg || '删除成功')
        fetchData()
      } else {
        ElMessage.error(res.data.msg || '删除失败')
      }
    } catch(e) {
      ElMessage.error('网络错误')
    }
  }).catch(() => {})
}

const handleBatchDelete = () => {
  if (selectedRows.value.length === 0) {
    return ElMessage.warning('请选择要删除的数据')
  }
  ElMessageBox.confirm(`确认删除选中的 ${selectedRows.value.length} 条记录吗?`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    const ids = selectedRows.value.map(item => item.id)
    try {
      const res = await axios.post(`/api/admin/system/form/delete`, { ids })
      if (res.data.code === 200) {
        ElMessage.success('批量删除成功')
        fetchData()
      } else {
        ElMessage.error(res.data.msg || '删除失败')
      }
    } catch(e) {
      ElMessage.error('网络错误')
    }
  }).catch(() => {})
}

const submitForm = async () => {
  try {
    const res = await axios.post(`/api/admin/system/form/save`, form)
    if (res.data.code === 200) {
      ElMessage.success(res.data.msg || '保存成功')
      dialogVisible.value = false
      fetchData()
    } else {
      ElMessage.error(res.data.msg || '保存失败')
    }
  } catch(e) {
    ElMessage.error('网络错误')
  }
}

onMounted(() => {
  fetchData()
})
</script>
