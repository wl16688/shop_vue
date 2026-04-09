<template>
  <div>
    <el-card>
            <el-form :inline="true" class="demo-form-inline" size="default">
        <el-form-item label="用户信息：">
          <el-input v-model="searchQuery.keyword" placeholder="昵称/手机号" clearable style="width: 200px;"></el-input>
        </el-form-item>
        <el-form-item label="分销等级：">
          <el-select v-model="searchQuery.level" placeholder="全部" clearable style="width: 150px;">
            <el-option label="普通分销员" value="1"></el-option>
            <el-option label="高级分销员" value="2"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
          <el-button @click="resetData">重置</el-button>
        </el-form-item>
      </el-form>
            <div style="margin-bottom: 15px;">
        <el-button type="warning" @click="handleExport">导出分销员数据</el-button>
      </div>
      <el-table :data="tableData" style="width: 100%" v-loading="loading" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column prop="uid" label="UID" width="80" align="center" />
        <el-table-column prop="user_info" label="分销员信息" min-width="180" align="left">
          <template #default="scope">
            <div style="display: flex; align-items: center;">
              <el-avatar :size="40" :src="scope.row.avatar" style="margin-right: 10px;"></el-avatar>
              <div>
                <div style="font-weight: bold; font-size: 13px;">{{ scope.row.nickname }}</div>
                <div style="font-size: 12px; color: #999;">{{ scope.row.phone }}</div>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="level_name" label="分销等级" width="100" align="center">
          <template #default="scope">
            <el-tag size="small" type="warning">{{ scope.row.level_name }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="spread_count" label="推广人数" width="100" align="center" />
        <el-table-column prop="order_count" label="推广订单" width="100" align="center" />
        <el-table-column prop="brokerage_price" label="累计佣金" width="120" align="center">
          <template #default="scope">
            <span style="color: #f56c6c;">￥{{ scope.row.brokerage_price }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="推广资格" width="100" align="center">
          <template #default="scope">
            <el-switch v-model="scope.row.status" :active-value="1" :inactive-value="0" />
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="成为分销员时间" min-width="160" align="center" />
        <el-table-column label="操作" width="150" align="center" fixed="right">
          <template #default="scope">
            <el-button size="small" type="primary" link @click="handleDetail(scope.row)">分销订单</el-button>
            <el-button size="small" type="danger" link>取消资格</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div style="margin-top: 20px; text-align: right;">
        <el-pagination background layout="total, sizes, prev, pager, next, jumper" :total="total" />
      </div>
    </el-card>

    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px">
      <el-form label-width="100px" :model="form" ref="formRef">
        <el-form-item label="名称" required>
          <el-input v-model="form.name" placeholder="请输入名称"></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="form.status" :active-value="1" :inactive-value="0" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input type="textarea" v-model="form.remark" placeholder="请输入备注"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog title="分销员管理详情" v-model="detailVisible" width="500px">
      <el-descriptions border :column="1">
        <el-descriptions-item label="ID">{{ detailData.id }}</el-descriptions-item>
        <el-descriptions-item label="名称">{{ detailData.name }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="detailData.status === 1 ? 'success' : 'danger'">{{ detailData.status === 1 ? '启用' : '禁用' }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ detailData.createTime }}</el-descriptions-item>
        <el-descriptions-item label="备注">{{ detailData.remark || '无' }}</el-descriptions-item>
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
  keyword: ''
})

const form = reactive({
  id: null,
  name: '',
  status: 1,
  remark: ''
})

const fetchData = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/extend/agent_agent_manage_index/list', { params: searchQuery })
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
  dialogTitle.value = '添加分销员管理'
  form.id = null
  form.name = ''
  form.status = 1
  form.remark = ''
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑分销员管理'
  form.id = row.id
  form.name = row.name
  form.status = row.status
  form.remark = row.remark || ''
  dialogVisible.value = true
}

const handleDetail = async (row) => {
  try {
    const res = await axios.get(`/api/admin/extend/agent_agent_manage_index/detail?id=${row.id}`)
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
    const res = await axios.post(`/api/admin/extend/agent_agent_manage_index/save`, row)
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
      const res = await axios.post(`/api/admin/extend/agent_agent_manage_index/delete`, { id: row.id })
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
      const res = await axios.post(`/api/admin/extend/agent_agent_manage_index/delete`, { ids })
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

const handleExport = async () => {
  ElMessage.success('开始导出数据...')
  try {
    const res = await axios.get(`/api/admin/extend/agent_agent_manage_index/export`, { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', '分销员管理_export.csv')
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch(e) {
    ElMessage.error('导出失败')
  }
}

const submitForm = async () => {
  try {
    const res = await axios.post(`/api/admin/extend/agent_agent_manage_index/save`, form)
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
