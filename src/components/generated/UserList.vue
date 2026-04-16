<template>
  <div class="user-list-container">
    <el-card shadow="never" class="table-card">
      <div class="search-wrapper">
        <el-form :inline="true" :model="searchQuery" class="advanced-search-form" size="default">
          <el-row :gutter="15">
            <el-col :span="6">
              <el-form-item label="用户搜索" style="width: 100%;">
                <el-input v-model="searchQuery.keyword" placeholder="请输入昵称或手机号" clearable />
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item label="用户等级" style="width: 100%;">
                <el-select v-model="searchQuery.level" placeholder="全部等级" clearable style="width: 100%;">
                  <el-option label="普通用户" :value="0" />
                  <el-option label="VIP会员" :value="1" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item label="用户分组" style="width: 100%;">
                <el-select v-model="searchQuery.groupId" placeholder="全部分组" clearable style="width: 100%;">
                  <el-option label="默认分组" :value="0" />
                  <el-option label="高潜用户" :value="1" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="10" class="text-right">
              <el-form-item style="margin-right: 0;">
                <el-button type="primary" @click="fetchUsers">搜索</el-button>
                <el-button @click="resetSearch">重置</el-button>
                <el-button type="primary" link @click="isExpandSearch = !isExpandSearch">
                  {{ isExpandSearch ? '收起' : '高级搜索' }}
                  <el-icon><ArrowDown v-if="!isExpandSearch" /><ArrowUp v-else /></el-icon>
                </el-button>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row :gutter="15" v-show="isExpandSearch" style="margin-top: 15px;">
            <el-col :span="4">
              <el-form-item label="用户状态" style="width: 100%;">
                <el-select v-model="searchQuery.status" placeholder="全部" clearable style="width: 100%;">
                  <el-option label="正常" :value="1" />
                  <el-option label="禁用" :value="0" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>

      <div class="action-bar" style="margin-bottom: 15px;">
        <el-button type="info" @click="handleExport" plain>导出用户数据</el-button>
      </div>

      <el-table :data="userList" v-loading="loading" style="width: 100%" border>
        <el-table-column prop="uid" label="UID" width="80" align="center" />
        <el-table-column prop="avatar" label="头像" width="80" align="center">
          <template #default="{ row }">
            <el-avatar :size="40" :src="row.avatar" />
          </template>
        </el-table-column>
        <el-table-column prop="nickname" label="昵称" min-width="150" />
        <el-table-column prop="phone" label="手机号码" width="120" align="center" />
        <el-table-column prop="nowMoney" label="余额" width="100" align="center">
          <template #default="scope">
            <span style="color: #f5222d; font-weight: bold;">¥{{ scope.row.nowMoney }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="integral" label="积分" width="100" align="center" />
        <el-table-column prop="level" label="等级" width="100" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.level === 0 ? 'info' : 'warning'" size="small">
              {{ scope.row.level === 0 ? '普通' : 'VIP' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-switch v-model="row.status" :active-value="1" :inactive-value="0" @change="handleStatusChange(row)" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right" align="center">
          <template #default="{ row }">
            <el-button size="small" type="primary" link @click="handleEdit(row)">用户详情</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Pagination -->
      <div style="margin-top: 20px; display: flex; justify-content: flex-end;">
        <el-pagination
          background
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          :page-sizes="[15, 30, 50, 100]"
          v-model:current-page="searchQuery.page"
          v-model:page-size="searchQuery.limit"
          @current-change="fetchUsers"
          @size-change="fetchUsers"
        />
      </div>
    </el-card>

    <!-- User Detail Dialog -->
    <el-dialog v-model="detailVisible" title="用户详情" width="500px">
      <div v-if="currentUser" class="user-detail">
        <el-descriptions border :column="1">
          <el-descriptions-item label="UID">{{ currentUser.uid }}</el-descriptions-item>
          <el-descriptions-item label="账号">{{ currentUser.account || '暂无' }}</el-descriptions-item>
          <el-descriptions-item label="昵称">{{ currentUser.nickname }}</el-descriptions-item>
          <el-descriptions-item label="手机号">{{ currentUser.phone || '暂无' }}</el-descriptions-item>
          <el-descriptions-item label="真实姓名">{{ currentUser.realName || '暂无' }}</el-descriptions-item>
          <el-descriptions-item label="当前余额">¥{{ currentUser.nowMoney }}</el-descriptions-item>
          <el-descriptions-item label="积分">{{ currentUser.integral }}</el-descriptions-item>
          <el-descriptions-item label="等级">
            <el-tag :type="currentUser.level === 0 ? 'info' : 'warning'">{{ currentUser.level === 0 ? '普通用户' : 'VIP' }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="注册时间">{{ formatTime(currentUser.addTime) }}</el-descriptions-item>
          <el-descriptions-item label="最后登录">{{ formatTime(currentUser.lastTime) }}</el-descriptions-item>
        </el-descriptions>
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
import { ref, reactive, onMounted, inject } from 'vue'
import { ElMessage } from 'element-plus'
import { ArrowDown, ArrowUp } from '@element-plus/icons-vue'

const axios = inject('axios')

const userList = ref([])
const loading = ref(false)
const total = ref(0)
const isExpandSearch = ref(false)

const detailVisible = ref(false)
const currentUser = ref(null)

const searchQuery = reactive({
  keyword: '',
  level: null,
  groupId: null,
  status: null,
  page: 1,
  limit: 15
})

const formatTime = (timestamp) => {
  if (!timestamp) return '暂无'
  const date = new Date(timestamp * 1000)
  return date.toLocaleString()
}

const fetchUsers = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/user/list', { params: searchQuery })
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

const resetSearch = () => {
  searchQuery.keyword = ''
  searchQuery.level = null
  searchQuery.groupId = null
  searchQuery.status = null
  searchQuery.page = 1
  fetchUsers()
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

const handleExport = () => {
  ElMessage.success('开始导出用户数据...')
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.user-list-container {
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
