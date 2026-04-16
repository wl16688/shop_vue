<template>
  <div>
    <el-card>
      <el-form :inline="true" class="demo-form-inline" size="default">
        <el-form-item label="品牌名称：">
          <el-input v-model="searchQuery.keyword" placeholder="请输入品牌名称" clearable style="width: 200px;" @keyup.enter="fetchData"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">搜索</el-button>
        </el-form-item>
      </el-form>
      <div style="margin-bottom: 15px;">
        <el-button type="primary" plain @click="handleAdd">新增</el-button>
        <el-button type="danger" plain @click="handleBatchDelete">批量删除</el-button>
      </div>
      <el-table :data="tableData" style="width: 100%" v-loading="loading" @selection-change="handleSelectionChange">
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column prop="brandName" label="品牌名称" min-width="120" align="center" />
        <el-table-column prop="sort" label="排序" width="80" align="center" />
        <el-table-column prop="isShow" label="状态" width="100" align="center">
          <template #default="scope">
            <el-switch v-model="scope.row.isShow" :active-value="1" :inactive-value="0" @change="handleStatusChange(scope.row)" />
          </template>
        </el-table-column>
        <el-table-column prop="addTime" label="创建时间" min-width="160" align="center">
          <template #default="scope">
            {{ formatTime(scope.row.addTime) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" align="center" fixed="right">
          <template #default="scope">
            <el-button size="small" type="primary" link @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" link @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div style="margin-top: 20px; text-align: right;">
        <el-pagination
          background
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          v-model:current-page="searchQuery.page"
          v-model:page-size="searchQuery.limit"
          @size-change="fetchData"
          @current-change="fetchData"
        />
      </div>
    </el-card>

    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px">
      <el-form label-width="100px" :model="form" ref="formRef">
        <el-form-item label="品牌名称" required>
          <el-input v-model="form.brandName" placeholder="请输入品牌名称"></el-input>
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.sort" :min="0" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="form.isShow" :active-value="1" :inactive-value="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog title="商品品牌详情" v-model="detailVisible" width="500px">
      <el-descriptions border :column="1">
        <el-descriptions-item label="ID">{{ detailData.id }}</el-descriptions-item>
        <el-descriptions-item label="品牌名称">{{ detailData.brandName }}</el-descriptions-item>
        <el-descriptions-item label="排序">{{ detailData.sort }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="detailData.isShow === 1 ? 'success' : 'danger'">{{ detailData.isShow === 1 ? '显示' : '隐藏' }}</el-tag>
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
  keyword: '',
  page: 1,
  limit: 10
})

const form = reactive({
  id: null,
  brandName: '',
  sort: 0,
  isShow: 1
})

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp * 1000)
  return date.toLocaleString('zh-CN', { hour12: false }).replace(/\//g, '-')
}

const fetchData = async () => {
  loading.value = true
  try {
    const res = await axios.post('/api/admin/store/product/brand/list', searchQuery)
    if (res.data.code === 200) {
      tableData.value = res.data.data.records || res.data.data || []
      total.value = res.data.data.total !== undefined ? res.data.data.total : (res.data.data.length || 0)
    } else {
      ElMessage.error(res.data.msg || '获取数据失败')
    }
  } catch (error) {
    if (!error.response || error.response.status !== 401) {
      ElMessage.error(error.response?.data?.msg || '获取列表失败')
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
  dialogTitle.value = '添加品牌'
  form.id = null
  form.brandName = ''
  form.sort = 0
  form.isShow = 1
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑品牌'
  form.id = row.id
  form.brandName = row.brandName
  form.sort = row.sort || 0
  form.isShow = row.isShow
  dialogVisible.value = true
}

const handleDetail = async (row) => {
  try {
    const res = await axios.get(`/api/admin/store/product/brand/detail?id=${row.id}`)
    if (res.data.code === 200) {
      detailData.value = res.data.data
    } else {
      detailData.value = { ...row }
    }
  } catch(e) {
    detailData.value = { ...row }
  }
  detailVisible.value = true
}

const handleStatusChange = async (row) => {
  try {
    const res = await axios.post(`/api/admin/store/product/brand/save`, row)
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
      const res = await axios.post(`/api/admin/store/product/brand/delete`, { id: row.id })
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
      const res = await axios.post(`/api/admin/store/product/brand/delete`, { ids })
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
    const res = await axios.post(`/api/admin/store/product/brand/save`, form)
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
