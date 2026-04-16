<template>
  <div>
    <el-card>
      <el-form :inline="true" class="demo-form-inline" size="default">
        <el-form-item label="模板名称：">
          <el-input v-model="searchQuery.keyword" placeholder="请输入模板名称" clearable style="width: 200px;" @keyup.enter="fetchData"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">搜索</el-button>
        </el-form-item>
      </el-form>
      <div style="margin-bottom: 15px;">
        <el-button type="primary" @click="handleAdd">添加参数模板</el-button>
      </div>
      <el-table :data="tableData" style="width: 100%" v-loading="loading" @selection-change="handleSelectionChange">
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column prop="ruleName" label="模板名称" min-width="120" align="center" />
        <el-table-column prop="ruleValue" label="商品参数" min-width="200" align="left">
          <template #default="scope">
            <div v-if="scope.row.ruleValue">
              <el-tag v-for="(spec, index) in parseSpecs(scope.row.ruleValue)" :key="index" size="small" style="margin-right: 5px; margin-bottom: 5px;">
                {{ spec.value }}
              </el-tag>
            </div>
            <span v-else>无参数</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" align="center" fixed="right">
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
        <el-form-item label="模板名称" required>
          <el-input v-model="form.ruleName" placeholder="请输入模板名称"></el-input>
        </el-form-item>
        <el-form-item label="规格参数">
          <div v-for="(spec, index) in parsedSpecs" :key="index" style="margin-bottom: 10px;">
            <el-input v-model="spec.value" placeholder="规格名称 (如: 颜色)" style="width: 150px; margin-right: 10px;"></el-input>
            <el-input v-model="spec.detailStr" placeholder="规格值 (多个用逗号隔开)" style="width: 250px;"></el-input>
            <el-button type="danger" link @click="removeSpec(index)">删除</el-button>
          </div>
          <el-button type="primary" link @click="addSpec">添加规格</el-button>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog title="商品参数详情" v-model="detailVisible" width="500px">
      <el-descriptions border :column="1">
        <el-descriptions-item label="ID">{{ detailData.id }}</el-descriptions-item>
        <el-descriptions-item label="模板名称">{{ detailData.ruleName }}</el-descriptions-item>
        <el-descriptions-item label="商品参数">
          <div v-if="detailData.ruleValue">
            <el-tag v-for="(spec, index) in parseSpecs(detailData.ruleValue)" :key="index" size="small" style="margin-right: 5px; margin-bottom: 5px;">
              {{ spec.value }}: {{ (spec.detail || []).join(', ') }}
            </el-tag>
          </div>
          <span v-else>无参数</span>
        </el-descriptions-item>
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
  ruleName: '',
  ruleValue: ''
})

const parsedSpecs = ref([])

const parseSpecs = (ruleValueStr) => {
  if (!ruleValueStr) return []
  try {
    return JSON.parse(ruleValueStr)
  } catch (e) {
    return []
  }
}

const addSpec = () => {
  parsedSpecs.value.push({ value: '', detailStr: '' })
}

const removeSpec = (index) => {
  parsedSpecs.value.splice(index, 1)
}

const fetchData = async () => {
  loading.value = true
  try {
    const res = await axios.post('/api/admin/store/product/rule/list', searchQuery)
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
  dialogTitle.value = '添加商品参数'
  form.id = null
  form.ruleName = ''
  form.ruleValue = ''
  parsedSpecs.value = [{ value: '', detailStr: '' }]
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑商品参数'
  form.id = row.id
  form.ruleName = row.ruleName
  form.ruleValue = row.ruleValue
  
  const specs = parseSpecs(row.ruleValue)
  parsedSpecs.value = specs.map(s => ({
    value: s.value,
    detailStr: (s.detail || []).join(',')
  }))
  if (parsedSpecs.value.length === 0) {
    parsedSpecs.value.push({ value: '', detailStr: '' })
  }
  dialogVisible.value = true
}

const handleDetail = async (row) => {
  try {
    const res = await axios.get(`/api/admin/store/product/rule/detail?id=${row.id}`)
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
    const res = await axios.post(`/api/admin/store/product/rule/save`, row)
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
      const res = await axios.post(`/api/admin/store/product/rule/delete`, { id: row.id })
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
      const res = await axios.post(`/api/admin/store/product/rule/delete`, { ids })
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
    const res = await axios.get(`/api/admin/extend/product_specs/export`, { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', '商品参数_export.csv')
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch(e) {
    ElMessage.error('导出失败')
  }
}

const submitForm = async () => {
  try {
    const specsData = parsedSpecs.value.filter(s => s.value.trim()).map(s => ({
      value: s.value,
      detail: s.detailStr.split(',').map(d => d.trim()).filter(d => d)
    }))
    form.ruleValue = JSON.stringify(specsData)
    
    const res = await axios.post(`/api/admin/store/product/rule/save`, form)
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
