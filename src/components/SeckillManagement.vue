<template>
  <div class="seckill-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>秒杀活动管理</span>
          <el-input
            v-model="title"
            placeholder="请输入秒杀活动名称"
            style="width: 250px; margin-left: auto; margin-right: 10px;"
            clearable
            @clear="fetchSeckills"
            @keyup.enter="fetchSeckills"
          />
          <el-button type="primary" @click="fetchSeckills">搜索</el-button>
          <el-button type="success" @click="handleAdd">添加秒杀商品</el-button>
        </div>
      </template>

      <el-table :data="seckillList" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="image" label="商品图片" width="100">
          <template #default="{ row }">
            <el-avatar shape="square" :size="50" :src="row.image" />
          </template>
        </el-table-column>
        <el-table-column prop="title" label="秒杀标题" min-width="150" show-overflow-tooltip />
        <el-table-column prop="price" label="秒杀价" width="100" />
        <el-table-column prop="otPrice" label="原价" width="100" />
        <el-table-column prop="stock" label="秒杀库存" width="100" />
        <el-table-column prop="sales" label="已售" width="100" />
        <el-table-column prop="status" label="活动状态" width="100">
          <template #default="{ row }">
            <el-switch v-model="row.status" :active-value="1" :inactive-value="0" @change="handleStatusChange(row)" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Pagination -->
      <div class="pagination-block">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="limit"
          :total="total"
          @current-change="fetchSeckills"
          layout="total, prev, pager, next"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

const seckillList = ref([])
const loading = ref(false)
const title = ref('')
const page = ref(1)
const limit = ref(15)
const total = ref(0)

const fetchSeckills = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/store/seckill/list', {
      params: { page: page.value, limit: limit.value, title: title.value }
    })
    if (res.data.code === 200) {
      seckillList.value = res.data.data.records
      total.value = res.data.data.total
    }
  } catch (error) {
    ElMessage.error('获取秒杀列表失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  ElMessage.info('暂未实现表单弹窗')
}

const handleEdit = (row) => {
  ElMessage.info('暂未实现表单弹窗')
}

const handleStatusChange = async (row) => {
  try {
    await axios.post('/api/admin/store/seckill/save', row)
    ElMessage.success('状态更新成功')
  } catch (error) {
    row.status = row.status === 1 ? 0 : 1
    ElMessage.error('状态更新失败')
  }
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定要删除此秒杀活动吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      const res = await axios.delete(`/api/admin/store/seckill/delete/${id}`)
      if (res.data.code === 200) {
        ElMessage.success('删除成功')
        fetchSeckills()
      }
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

onMounted(() => {
  fetchSeckills()
})
</script>

<style scoped>
.card-header {
  display: flex;
  align-items: center;
}
.pagination-block {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>
