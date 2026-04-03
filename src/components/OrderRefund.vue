<template>
  <div>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>退款单</span>
          <el-button type="primary" @click="dialogVisible = true">添加退款单</el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <el-form :inline="true" class="demo-form-inline">
        <el-form-item label="关键字">
          <el-input placeholder="请输入关键字搜索"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">搜索</el-button>
        </el-form-item>
      </el-form>

      <!-- 数据表格 -->
      <el-table :data="tableData" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-switch v-model="scope.row.status" :active-value="1" :inactive-value="0" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="dialogVisible = true">编辑</el-button>
            <el-button size="small" type="danger">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div style="margin-top: 20px; text-align: right;">
        <el-pagination background layout="prev, pager, next" :total="total" />
      </div>
    </el-card>

    <!-- 弹窗 -->
    <el-dialog title="退款单配置" v-model="dialogVisible" width="500px">
      <el-form label-width="100px">
        <el-form-item label="名称">
          <el-input placeholder="请输入名称"></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-switch :active-value="1" :inactive-value="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="dialogVisible = false">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const tableData = ref([])
const total = ref(0)
const loading = ref(false)
const dialogVisible = ref(false)

const fetchData = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/extend/order_refund/list')
    if (res.data.code === 200) {
      tableData.value = res.data.data.records || res.data.data
      total.value = res.data.data.total || res.data.data.length
    }
  } catch (error) {
    ElMessage.error('获取列表失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
