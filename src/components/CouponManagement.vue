<template>
  <div class="coupon-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>优惠券管理</span>
          <el-input
            v-model="title"
            placeholder="请输入优惠券名称搜索"
            style="width: 250px; margin-left: auto; margin-right: 10px;"
            clearable
            @clear="fetchCoupons"
            @keyup.enter="fetchCoupons"
          />
          <el-button type="primary" @click="fetchCoupons">搜索</el-button>
          <el-button type="success" @click="handleAdd">发布优惠券</el-button>
        </div>
      </template>

      <el-table :data="couponList" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="couponTitle" label="优惠券名称" min-width="150" />
        <el-table-column prop="couponType" label="类型" width="100">
          <template #default="{ row }">
            <el-tag :type="row.couponType === 1 ? 'danger' : 'warning'">
              {{ row.couponType === 1 ? '满减券' : '折扣券' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="couponPrice" label="面值/折扣" width="100" />
        <el-table-column prop="useMinPrice" label="最低消费门槛" width="120" />
        <el-table-column prop="totalCount" label="发行总量" width="100" />
        <el-table-column prop="remainCount" label="剩余数量" width="100" />
        <el-table-column prop="status" label="状态" width="100">
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
          @current-change="fetchCoupons"
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

const couponList = ref([])
const loading = ref(false)
const title = ref('')
const page = ref(1)
const limit = ref(15)
const total = ref(0)

const fetchCoupons = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/store/coupon/list', {
      params: { page: page.value, limit: limit.value, title: title.value }
    })
    if (res.data.code === 200) {
      couponList.value = res.data.data.records
      total.value = res.data.data.total
    }
  } catch (error) {
    ElMessage.error('获取优惠券列表失败')
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
    await axios.post('/api/admin/store/coupon/save', row)
    ElMessage.success('状态更新成功')
  } catch (error) {
    row.status = row.status === 1 ? 0 : 1
    ElMessage.error('状态更新失败')
  }
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定要删除此优惠券吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      const res = await axios.delete(`/api/admin/store/coupon/delete/${id}`)
      if (res.data.code === 200) {
        ElMessage.success('删除成功')
        fetchCoupons()
      }
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

onMounted(() => {
  fetchCoupons()
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
