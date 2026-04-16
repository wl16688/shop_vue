<template>
  <div class="product-category-container">
    <el-card shadow="never" class="table-card">
      <div class="search-wrapper">
        <el-form :inline="true" :model="searchQuery" class="advanced-search-form" size="default">
          <el-row :gutter="15">
            <el-col :span="6">
              <el-form-item label="分类名称" style="width: 100%;">
                <el-input v-model="searchQuery.keyword" placeholder="请输入分类名称" clearable />
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item label="状态" style="width: 100%;">
                <el-select v-model="searchQuery.isShow" placeholder="全部" clearable style="width: 100%;">
                  <el-option label="显示" :value="1"></el-option>
                  <el-option label="隐藏" :value="0"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="14" class="text-right">
              <el-form-item style="margin-right: 0;">
                <el-button type="primary" @click="fetchData">搜索</el-button>
                <el-button @click="resetSearch">重置</el-button>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>

      <div class="action-bar" style="margin-bottom: 15px;">
        <el-button type="primary" @click="handleAdd(0)">添加一级分类</el-button>
      </div>

      <el-table :data="tableTree" style="width: 100%" v-loading="loading" row-key="id" :tree-props="{children: 'children', hasChildren: 'hasChildren'}" border>
        <el-table-column prop="cateName" label="分类名称" min-width="180" />
        <el-table-column prop="id" label="ID" width="100" align="center" />
        <el-table-column prop="pic" label="分类图标" width="100" align="center">
          <template #default="scope">
            <el-image v-if="scope.row.pic" style="width: 40px; height: 40px; border-radius: 4px;" :src="scope.row.pic" fit="contain" />
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="sort" label="排序" width="100" align="center" />
        <el-table-column prop="isShow" label="状态" width="100" align="center">
          <template #default="scope">
            <el-switch v-model="scope.row.isShow" :active-value="1" :inactive-value="0" @change="handleStatusChange(scope.row)" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" align="center" fixed="right">
          <template #default="scope">
            <el-button size="small" type="success" link @click="handleAdd(scope.row.id)" v-if="scope.row.level < 2">添加子分类</el-button>
            <el-button size="small" type="primary" link @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" link @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px">
      <el-form label-width="100px" :model="form" ref="formRef">
        <el-form-item label="父级分类">
          <el-tree-select
            v-model="form.pid"
            :data="parentOptions"
            :props="{ label: 'cateName', value: 'id', children: 'children' }"
            check-strictly
            placeholder="请选择父级分类 (不选则为一级分类)"
            clearable
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="分类名称" required>
          <el-input v-model="form.cateName" placeholder="请输入分类名称"></el-input>
        </el-form-item>
        <el-form-item label="分类图标(PC)">
          <UploadImage v-model="form.pic" />
        </el-form-item>
        <el-form-item label="分类大图(移动)">
          <UploadImage v-model="form.bigPic" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.sort" :min="0"></el-input-number>
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="form.isShow" :active-value="1" :inactive-value="0" active-text="显示" inactive-text="隐藏" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, inject, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import UploadImage from '../UploadImage.vue'

const axios = inject('axios')
const tableData = ref([])
const loading = ref(false)

const dialogVisible = ref(false)
const dialogTitle = ref('新增分类')

const searchQuery = reactive({
  keyword: '',
  isShow: null
})

const form = reactive({
  id: null,
  pid: 0,
  cateName: '',
  pic: '',
  bigPic: '',
  sort: 0,
  isShow: 1
})

// 将平铺数据转换为树形结构
const tableTree = computed(() => {
  const data = JSON.parse(JSON.stringify(tableData.value))
  const result = []
  const map = {}
  data.forEach(item => {
    map[item.id] = item
  })
  data.forEach(item => {
    const parent = map[item.pid]
    if (parent) {
      (parent.children || (parent.children = [])).push(item)
    } else {
      result.push(item)
    }
  })
  return result
})

const parentOptions = computed(() => {
  // 过滤出1级和2级分类作为父级选项 (防止超过3级)
  const filterOptions = (nodes, currentLevel = 1) => {
    if (currentLevel >= 3) return null
    return nodes.map(node => {
      const newNode = { ...node }
      if (newNode.children && newNode.children.length > 0) {
        const filteredChildren = filterOptions(newNode.children, currentLevel + 1)
        if (filteredChildren) {
          newNode.children = filteredChildren
        } else {
          delete newNode.children
        }
      }
      return newNode
    })
  }
  
  const options = filterOptions(tableTree.value) || []
  return [{ id: 0, cateName: '顶级分类 (不选默认为此)' }, ...options]
})

const fetchData = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/store/productCategory/list', { params: searchQuery })
    if (res.data.code === 200) {
      tableData.value = res.data.data
    } else {
      ElMessage.error(res.data.msg || '获取数据失败')
    }
  } catch (error) {
    ElMessage.error('获取列表失败')
  } finally {
    loading.value = false
  }
}

const resetSearch = () => {
  searchQuery.keyword = ''
  searchQuery.isShow = null
  fetchData()
}

const handleAdd = (pid = 0) => {
  dialogTitle.value = pid === 0 ? '添加一级分类' : '添加子分类'
  form.id = null
  form.pid = pid
  form.cateName = ''
  form.pic = ''
  form.bigPic = ''
  form.sort = 0
  form.isShow = 1
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑分类'
  form.id = row.id
  form.pid = row.pid
  form.cateName = row.cateName
  form.pic = row.pic || ''
  form.bigPic = row.bigPic || ''
  form.sort = row.sort
  form.isShow = row.isShow
  dialogVisible.value = true
}

const handleStatusChange = async (row) => {
  try {
    const res = await axios.post(`/api/admin/store/productCategory/save`, row)
    if (res.data.code === 200) {
      ElMessage.success('状态修改成功')
    } else {
      ElMessage.error(res.data.msg || '状态修改失败')
      row.isShow = row.isShow === 1 ? 0 : 1
    }
  } catch(e) {
    ElMessage.error('网络错误')
    row.isShow = row.isShow === 1 ? 0 : 1
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除该分类吗? 如果存在子分类建议先删除子分类。', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    try {
      const res = await axios.delete(`/api/admin/store/productCategory/delete/${row.id}`)
      if (res.data.code === 200) {
        ElMessage.success('删除成功')
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
  if (!form.cateName) return ElMessage.warning('请输入分类名称')
  try {
    const res = await axios.post(`/api/admin/store/productCategory/save`, form)
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
  fetchData()
})
</script>

<style scoped>
.product-category-container {
  background-color: #f0f2f5;
  min-height: 100%;
}
.table-card {
  border-radius: 4px;
  border: none;
}
.search-wrapper {
  background-color: #f8f8f9;
  padding: 15px 15px 0;
  margin-bottom: 15px;
  border-radius: 4px;
}
.text-right {
  text-align: right;
}
</style>
