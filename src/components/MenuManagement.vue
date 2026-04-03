<template>
  <div class="menu-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>菜单权限管理</span>
          <el-button type="primary" @click="handleAdd(null)">添加顶级菜单</el-button>
        </div>
      </template>

      <el-table
        :data="menuTree"
        row-key="id"
        border
        v-loading="loading"
        default-expand-all
        :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
      >
        <el-table-column prop="menuName" label="菜单名称" width="200" />
        <el-table-column prop="icon" label="图标" width="80">
          <template #default="{ row }">
            <i :class="row.icon"></i>
          </template>
        </el-table-column>
        <el-table-column prop="path" label="路由/路径" />
        <el-table-column prop="authType" label="类型" width="100">
          <template #default="{ row }">
            <el-tag :type="row.authType === 1 ? 'primary' : 'info'">
              {{ row.authType === 1 ? '菜单' : '功能/按钮' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="isShow" label="可见状态" width="100">
          <template #default="{ row }">
            <el-switch v-model="row.isShow" :active-value="1" :inactive-value="0" @change="handleStatusChange(row)" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250">
          <template #default="{ row }">
            <el-button size="small" type="primary" text @click="handleAdd(row)">新增子菜单</el-button>
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Menu Form Dialog -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px">
      <el-form :model="form" ref="formRef" :rules="rules" label-width="100px">
        <el-form-item label="上级菜单">
          <el-tree-select
            v-model="form.pid"
            :data="menuTreeOptions"
            :props="{ label: 'menuName', value: 'id', children: 'children' }"
            check-strictly
            placeholder="请选择上级菜单"
            style="width: 100%"
            clearable
          />
        </el-form-item>
        <el-form-item label="菜单类型" prop="authType">
          <el-radio-group v-model="form.authType">
            <el-radio :label="1">菜单</el-radio>
            <el-radio :label="2">按钮/功能</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="菜单名称" prop="menuName">
          <el-input v-model="form.menuName" placeholder="请输入菜单名称"></el-input>
        </el-form-item>
        <el-form-item label="图标" v-if="form.authType === 1">
          <el-input v-model="form.icon" placeholder="请输入Element Plus图标名称，如：Setting"></el-input>
        </el-form-item>
        <el-form-item label="路由路径" prop="path" v-if="form.authType === 1">
          <el-input v-model="form.path" placeholder="请输入路由路径，如：/system"></el-input>
        </el-form-item>
        <el-form-item label="权限标识" v-if="form.authType === 2">
          <el-input v-model="form.api_url" placeholder="请输入后端接口权限标识，如：/api/admin/user/add"></el-input>
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.sort" :min="0" :max="9999" controls-position="right"></el-input-number>
        </el-form-item>
        <el-form-item label="是否显示" v-if="form.authType === 1">
          <el-switch v-model="form.isShow" :active-value="1" :inactive-value="0"></el-switch>
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
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

const menuTree = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref(null)

const form = ref({
  id: null,
  pid: 0,
  authType: 1,
  menuName: '',
  icon: '',
  path: '',
  api_url: '',
  sort: 0,
  isShow: 1
})

const rules = {
  menuName: [{ required: true, message: '请输入菜单名称', trigger: 'blur' }],
  path: [{ required: true, message: '请输入路由路径', trigger: 'blur' }]
}

const menuTreeOptions = computed(() => {
  return [{ id: 0, menuName: '顶级菜单' }, ...menuTree.value]
})

const buildTree = (data, pid = 0) => {
  const tree = []
  data.forEach(item => {
    if (item.pid === pid) {
      const children = buildTree(data, item.id)
      if (children.length > 0) {
        item.children = children
      }
      tree.push(item)
    }
  })
  return tree
}

const fetchMenus = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/system/menus/list')
    if (res.data.code === 200) {
      // Assuming flat list returned, build tree on frontend
      menuTree.value = buildTree(res.data.data, 0)
    }
  } catch (error) {
    ElMessage.error('获取菜单列表失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = (parent) => {
  form.value = {
    id: null,
    pid: parent ? parent.id : 0,
    authType: 1,
    menuName: '',
    icon: '',
    path: '',
    api_url: '',
    sort: 0,
    isShow: 1
  }
  dialogTitle.value = parent ? '新增子菜单' : '添加顶级菜单'
  dialogVisible.value = true
}

const handleEdit = (row) => {
  form.value = { ...row }
  dialogTitle.value = '编辑菜单'
  dialogVisible.value = true
}

const submitForm = () => {
  formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const res = await axios.post('/api/admin/system/menus/save', form.value)
        if (res.data.code === 200) {
          ElMessage.success('保存成功')
          dialogVisible.value = false
          fetchMenus()
        }
      } catch (error) {
        ElMessage.error('保存失败')
      }
    }
  })
}

const handleStatusChange = async (row) => {
  try {
    await axios.post('/api/admin/system/menus/save', row)
    ElMessage.success('状态更新成功')
  } catch (error) {
    row.isShow = row.isShow === 1 ? 0 : 1
    ElMessage.error('状态更新失败')
  }
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定要删除此菜单吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      const res = await axios.delete(`/api/admin/system/menus/delete/${id}`)
      if (res.data.code === 200) {
        ElMessage.success('删除成功')
        fetchMenus()
      }
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

onMounted(() => {
  fetchMenus()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
