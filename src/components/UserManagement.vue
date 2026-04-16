<template>
  <div class="user-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户列表管理</span>
          <el-input
            v-model="keyword"
            placeholder="请输入昵称或手机号搜索"
            style="width: 200px; margin-left: auto; margin-right: 10px;"
            clearable
            @clear="fetchUsers"
            @keyup.enter="fetchUsers"
          />
          <el-button type="primary" @click="fetchUsers">搜索</el-button>
        </div>
      </template>

      <el-table :data="userList" v-loading="loading" style="width: 100%">
        <el-table-column prop="uid" label="UID" width="80" />
        <el-table-column prop="avatar" label="头像" width="80">
          <template #default="{ row }">
            <el-avatar :size="40" :src="row.avatar" />
          </template>
        </el-table-column>
        <el-table-column prop="nickname" label="昵称" />
        <el-table-column prop="phone" label="手机号码" width="120" />
        <el-table-column prop="nowMoney" label="余额" width="100" />
        <el-table-column prop="integral" label="积分" width="100" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-switch v-model="row.status" :active-value="1" :inactive-value="0" @change="handleStatusChange(row)" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="handleEdit(row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Pagination -->
      <div class="pagination-block">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="limit"
          :total="total"
          @current-change="fetchUsers"
          layout="total, prev, pager, next"
        />
      </div>
    </el-card>

    <!-- User Detail Dialog -->
    <el-dialog v-model="detailVisible" title="用户详情" width="500px">
      <div v-if="currentUser" class="user-detail">
        <div class="detail-item"><strong>UID:</strong> {{ currentUser.uid }}</div>
        <div class="detail-item"><strong>账号:</strong> {{ currentUser.account || '暂无' }}</div>
        <div class="detail-item"><strong>昵称:</strong> {{ currentUser.nickname }}</div>
        <div class="detail-item"><strong>手机号:</strong> {{ currentUser.phone || '暂无' }}</div>
        <div class="detail-item"><strong>真实姓名:</strong> {{ currentUser.realName || '暂无' }}</div>
        <div class="detail-item"><strong>当前余额:</strong> {{ currentUser.nowMoney }}</div>
        <div class="detail-item"><strong>积分:</strong> {{ currentUser.integral }}</div>
        <div class="detail-item"><strong>等级:</strong> {{ currentUser.level === 0 ? '普通用户' : 'VIP' }}</div>
        <div class="detail-item"><strong>注册时间:</strong> {{ formatTime(currentUser.addTime) }}</div>
        <div class="detail-item"><strong>最后登录:</strong> {{ formatTime(currentUser.lastTime) }}</div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="detailVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const userList = ref([])
const loading = ref(false)
const keyword = ref('')
const page = ref(1)
const limit = ref(15)
const total = ref(0)

const detailVisible = ref(false)
const currentUser = ref(null)

const formatTime = (timestamp) => {
  if (!timestamp) return '暂无'
  const date = new Date(timestamp * 1000)
  return date.toLocaleString()
}

const fetchUsers = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/user/list', {
      params: { page: page.value, limit: limit.value, keyword: keyword.value }
    })
    if (res.data.code === 200) {
      userList.value = res.data.data.records
      total.value = res.data.data.total
    }
  } catch (error) {
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

const handleEdit = (row) => {
  currentUser.value = row
  detailVisible.value = true
}

const handleStatusChange = async (row) => {
  try {
    await axios.post('/api/admin/user/save', row)
    ElMessage.success('用户状态更新成功')
  } catch (error) {
    row.status = row.status === 1 ? 0 : 1
    ElMessage.error('状态更新失败')
  }
}

onMounted(() => {
  fetchUsers()
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
.user-detail .detail-item {
  margin-bottom: 12px;
  font-size: 14px;
}
</style>
