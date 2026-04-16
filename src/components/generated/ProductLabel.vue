<template>
  <div class="label-container">
    <el-row :gutter="20">
      <!-- 左侧分类树 -->
      <el-col :span="6">
        <el-card class="box-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>标签分组</span>
              <el-button type="primary" link @click="handleAddCate">新增</el-button>
            </div>
          </template>
          <div class="cate-list">
            <div 
              class="cate-item" 
              :class="{ active: currentCate === '' }" 
              @click="handleCateSelect('')"
            >
              全部标签
            </div>
            <div 
              class="cate-item" 
              :class="{ active: currentCate === item.id }" 
              v-for="item in cateList" 
              :key="item.id"
              @click="handleCateSelect(item.id)"
            >
              <span class="cate-name">{{ item.name }}</span>
              <div class="cate-actions">
                <el-icon @click.stop="handleEditCate(item)"><Edit /></el-icon>
                <el-icon @click.stop="handleDeleteCate(item)"><Delete /></el-icon>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 右侧标签列表 -->
      <el-col :span="18">
        <el-card shadow="never">
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
            <el-button type="primary" plain @click="handleAdd">新增标签</el-button>
            <el-button type="danger" plain @click="handleBatchDelete">批量删除</el-button>
          </div>
          
          <el-table :data="tableData" style="width: 100%" v-loading="loading" @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="55" />
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="labelName" label="标签名称" />
            <el-table-column prop="labelCate" label="所属分组">
              <template #default="scope">
                {{ getCateName(scope.row.labelCate) }}
              </template>
            </el-table-column>
            <el-table-column prop="sort" label="排序" width="80" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-switch v-model="scope.row.status" :active-value="1" :inactive-value="0" @change="handleStatusChange(scope.row)" />
              </template>
            </el-table-column>
            <el-table-column prop="addTime" label="创建时间" width="180">
              <template #default="scope">
                {{ formatTime(scope.row.addTime) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="handleEdit(scope.row)">编辑</el-button>
                <el-button size="small" type="primary" link @click="handleDetail(scope.row)">详情</el-button>
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
      </el-col>
    </el-row>

    <!-- 分组表单 -->
    <el-dialog :title="cateDialogTitle" v-model="cateDialogVisible" width="500px">
      <el-form label-width="100px" :model="cateForm">
        <el-form-item label="分组名称" required>
          <el-input v-model="cateForm.name" placeholder="请输入分组名称"></el-input>
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="cateForm.sort" :min="0" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="cateForm.isShow" :active-value="1" :inactive-value="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="cateDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitCateForm">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 标签表单 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px">
      <el-form label-width="100px" :model="form" ref="formRef">
        <el-form-item label="所属分组" required>
          <el-select v-model="form.labelCate" placeholder="请选择分组" style="width: 100%;">
            <el-option v-for="item in cateList" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="标签名称" required>
          <el-input v-model="form.labelName" placeholder="请输入标签名称"></el-input>
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.sort" :min="0" />
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

    <!-- 标签详情 -->
    <el-dialog title="商品标签详情" v-model="detailVisible" width="500px">
      <el-descriptions border :column="1">
        <el-descriptions-item label="ID">{{ detailData.id }}</el-descriptions-item>
        <el-descriptions-item label="标签名称">{{ detailData.labelName }}</el-descriptions-item>
        <el-descriptions-item label="所属分组">{{ getCateName(detailData.labelCate) }}</el-descriptions-item>
        <el-descriptions-item label="排序">{{ detailData.sort }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="detailData.status === 1 ? 'success' : 'danger'">{{ detailData.status === 1 ? '启用' : '禁用' }}</el-tag>
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
import { Edit, Delete } from '@element-plus/icons-vue'

const axios = inject('axios')

// === 分组相关 ===
const cateList = ref([])
const currentCate = ref('')
const cateDialogVisible = ref(false)
const cateDialogTitle = ref('新增分组')
const cateForm = reactive({
  id: null,
  name: '',
  sort: 0,
  isShow: 1
})

const fetchCateList = async () => {
  try {
    const res = await axios.get('/api/admin/store/product_label_cate/list')
    if (res.data.code === 200) {
      cateList.value = res.data.data
    }
  } catch (error) {
    ElMessage.error('获取分组失败')
  }
}

const getCateName = (id) => {
  const cate = cateList.value.find(c => c.id === id)
  return cate ? cate.name : '未知分组'
}

const handleCateSelect = (id) => {
  currentCate.value = id
  searchQuery.page = 1
  searchQuery.labelCate = id
  fetchData()
}

const handleAddCate = () => {
  cateDialogTitle.value = '新增分组'
  cateForm.id = null
  cateForm.name = ''
  cateForm.sort = 0
  cateForm.isShow = 1
  cateDialogVisible.value = true
}

const handleEditCate = (row) => {
  cateDialogTitle.value = '编辑分组'
  cateForm.id = row.id
  cateForm.name = row.name
  cateForm.sort = row.sort
  cateForm.isShow = row.isShow
  cateDialogVisible.value = true
}

const handleDeleteCate = (row) => {
  ElMessageBox.confirm('确认删除该分组吗? 删除后分组下的标签将不受影响但可能无法筛选', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    try {
      const res = await axios.post(`/api/admin/store/product_label_cate/delete`, { id: row.id })
      if (res.data.code === 200) {
        ElMessage.success('删除成功')
        if (currentCate.value === row.id) {
          handleCateSelect('')
        }
        fetchCateList()
      }
    } catch(e) {
      ElMessage.error('网络错误')
    }
  }).catch(() => {})
}

const submitCateForm = async () => {
  if (!cateForm.name) return ElMessage.warning('分组名称不能为空')
  try {
    const res = await axios.post(`/api/admin/store/product_label_cate/save`, cateForm)
    if (res.data.code === 200) {
      ElMessage.success('保存成功')
      cateDialogVisible.value = false
      fetchCateList()
    } else {
      ElMessage.error(res.data.msg || '保存失败')
    }
  } catch(e) {
    ElMessage.error('网络错误')
  }
}

// === 标签相关 ===
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
  labelCate: '',
  page: 1,
  limit: 10
})

const form = reactive({
  id: null,
  labelCate: '',
  labelName: '',
  status: 1,
  sort: 0,
  type: 0,
  styleType: 1
})

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp * 1000)
  return date.toLocaleString('zh-CN', { hour12: false }).replace(/\//g, '-')
}

const fetchData = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/store/product_label/list', { params: searchQuery })
    if (res.data.code === 200) {
      tableData.value = res.data.data.records
      total.value = res.data.data.total
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const resetData = () => {
  searchQuery.keyword = ''
  searchQuery.page = 1
  fetchData()
}

const handleSelectionChange = (val) => {
  selectedRows.value = val
}

const handleAdd = () => {
  dialogTitle.value = '添加商品标签'
  form.id = null
  form.labelCate = currentCate.value || (cateList.value.length > 0 ? cateList.value[0].id : '')
  form.labelName = ''
  form.status = 1
  form.sort = 0
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑商品标签'
  form.id = row.id
  form.labelCate = row.labelCate
  form.labelName = row.labelName
  form.status = row.status
  form.sort = row.sort || 0
  dialogVisible.value = true
}

const handleDetail = async (row) => {
  try {
    const res = await axios.get(`/api/admin/store/product_label/detail?id=${row.id}`)
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
    const res = await axios.post(`/api/admin/store/product_label/save`, {
      id: row.id,
      status: row.status
    })
    if (res.data.code === 200) {
      ElMessage.success('状态修改成功')
    } else {
      ElMessage.error(res.data.msg || '状态修改失败')
      row.status = row.status === 1 ? 0 : 1
    }
  } catch(e) {
    ElMessage.error('网络错误')
    row.status = row.status === 1 ? 0 : 1
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除该记录吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    try {
      const res = await axios.post(`/api/admin/store/product_label/delete`, { id: row.id })
      if (res.data.code === 200) {
        ElMessage.success('删除成功')
        fetchData()
      }
    } catch(e) {}
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
      const res = await axios.post(`/api/admin/store/product_label/delete`, { ids })
      if (res.data.code === 200) {
        ElMessage.success('批量删除成功')
        fetchData()
      }
    } catch(e) {}
  }).catch(() => {})
}

const submitForm = async () => {
  if (!form.labelCate) return ElMessage.warning('请选择所属分组')
  if (!form.labelName) return ElMessage.warning('请输入标签名称')
  try {
    const res = await axios.post(`/api/admin/store/product_label/save`, form)
    if (res.data.code === 200) {
      ElMessage.success('保存成功')
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
  fetchCateList()
  fetchData()
})
</script>

<style scoped>
.label-container {
  height: 100%;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.cate-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.cate-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.3s;
  background-color: #f5f7fa;
}
.cate-item:hover {
  background-color: #ecf5ff;
}
.cate-item.active {
  background-color: #e6f1fc;
  color: #409eff;
  font-weight: bold;
}
.cate-actions {
  display: none;
  gap: 10px;
  color: #909399;
}
.cate-item:hover .cate-actions {
  display: flex;
}
.cate-actions .el-icon:hover {
  color: #409eff;
}
</style>
