<template>
  <div>
    <el-card>
            <el-form :inline="true" class="demo-form-inline" size="default">
        <el-form-item label="商品信息：">
          <el-input v-model="searchQuery.keyword" placeholder="商品名称" clearable style="width: 200px;"></el-input>
        </el-form-item>
        <el-form-item label="回复状态：">
          <el-select v-model="searchQuery.isReply" placeholder="全部" clearable style="width: 150px;">
            <el-option label="全部" :value="-1" />
            <el-option label="已回复" :value="1" />
            <el-option label="未回复" :value="0" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
        </el-form-item>
      </el-form>
      <div style="margin-bottom: 15px;">
        <el-button type="danger" plain @click="handleBatchDelete">批量删除</el-button>
      </div>
      <el-table :data="tableData" style="width: 100%" v-loading="loading" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column prop="productId" label="商品ID" width="100" align="center" />
        <el-table-column prop="nickname" label="用户名称" width="120" align="center" />
        <el-table-column prop="replyScore" label="综合评分" width="150" align="center">
          <template #default="scope">
            <el-rate v-model="scope.row.replyScore" disabled show-score text-color="#ff9900" />
          </template>
        </el-table-column>
        <el-table-column prop="comment" label="评价内容" min-width="200" show-overflow-tooltip />
        <el-table-column prop="isReply" label="回复状态" width="100" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.isReply === 1 ? 'success' : 'info'">{{ scope.row.isReply === 1 ? '已回复' : '未回复' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="addTime" label="评价时间" width="160" align="center">
          <template #default="scope">
            {{ formatTime(scope.row.addTime) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" align="center" fixed="right">
          <template #default="scope">
            <el-button size="small" type="primary" link @click="handleDetail(scope.row)">回复</el-button>
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

    <el-dialog title="商品评论详情" v-model="detailVisible" width="500px">
      <el-descriptions border :column="1">
        <el-descriptions-item label="评价内容">{{ detailData.comment }}</el-descriptions-item>
        <el-descriptions-item label="商家回复">
          <el-input type="textarea" v-model="form.merchantReplyContent" placeholder="请输入商家回复内容" :rows="4"></el-input>
        </el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="detailVisible = false">取消</el-button>
          <el-button type="primary" @click="submitReply">确认回复</el-button>
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
  isReply: -1,
  page: 1,
  limit: 10
})

const form = reactive({
  id: null,
  merchantReplyContent: ''
})

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp * 1000)
  return date.toLocaleString('zh-CN', { hour12: false }).replace(/\//g, '-')
}

const fetchData = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/store/product/reply/list', { params: searchQuery })
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
  dialogTitle.value = '添加商品评论'
  form.id = null
  form.name = ''
  form.status = 1
  form.remark = ''
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑商品评论'
  form.id = row.id
  form.name = row.name
  form.status = row.status
  form.remark = row.remark || ''
  dialogVisible.value = true
}

const handleDetail = (row) => {
  detailData.value = { ...row }
  form.id = row.id
  form.merchantReplyContent = row.merchantReplyContent || ''
  detailVisible.value = true
}

const submitReply = async () => {
  if (!form.merchantReplyContent) return ElMessage.warning('回复内容不能为空')
  try {
    const res = await axios.post(`/api/admin/store/product/reply/set_reply`, form)
    if (res.data.code === 200) {
      ElMessage.success('回复成功')
      detailVisible.value = false
      fetchData()
    } else {
      ElMessage.error(res.data.msg || '回复失败')
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
      const res = await axios.post(`/api/admin/store/product/reply/delete`, { id: row.id })
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
      const res = await axios.post(`/api/admin/store/product/reply/delete`, { ids })
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
    const res = await axios.post(`/api/admin/store/product/reply/save`, form)
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
