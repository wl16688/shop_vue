<template>
  <div class="order-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>订单管理</span>
          <el-input
            v-model="orderId"
            placeholder="请输入订单号/流水号"
            style="width: 250px; margin-left: auto; margin-right: 10px;"
            clearable
            @clear="fetchOrders"
            @keyup.enter="fetchOrders"
          />
          <el-select v-model="status" placeholder="订单状态" style="width: 120px; margin-right: 10px;" clearable @change="fetchOrders">
            <el-option label="待发货" :value="0" />
            <el-option label="待收货" :value="1" />
            <el-option label="已收货" :value="2" />
            <el-option label="待评价" :value="3" />
            <el-option label="已退款" :value="-1" />
          </el-select>
          <el-button type="primary" @click="fetchOrders">搜索</el-button>
        </div>
      </template>

      <el-table :data="orderList" v-loading="loading" style="width: 100%">
        <el-table-column prop="orderId" label="订单号" width="180" />
        <el-table-column prop="realName" label="收货人" width="100" />
        <el-table-column prop="userPhone" label="联系电话" width="120" />
        <el-table-column prop="totalPrice" label="订单总价" width="100" />
        <el-table-column prop="payPrice" label="实付金额" width="100" />
        <el-table-column prop="payType" label="支付方式" width="100" />
        <el-table-column prop="paid" label="支付状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.paid === 1 ? 'success' : 'danger'">
              {{ row.paid === 1 ? '已支付' : '未支付' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="订单状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusName(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" text @click="handleEdit(row)">订单详情</el-button>
            <el-button v-if="row.status === 0" size="small" type="success" text @click="handleDeliver(row)">去发货</el-button>
            <el-button size="small" type="danger" text @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Pagination -->
      <div class="pagination-block">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="limit"
          :total="total"
          @current-change="fetchOrders"
          layout="total, prev, pager, next"
        />
      </div>
    </el-card>

    <!-- Delivery Dialog -->
    <el-dialog v-model="deliveryDialogVisible" title="订单发货" width="400px">
      <el-form :model="deliveryForm" label-width="100px">
        <el-form-item label="快递公司">
          <el-input v-model="deliveryForm.deliveryName" placeholder="请输入快递公司名称" />
        </el-form-item>
        <el-form-item label="快递单号">
          <el-input v-model="deliveryForm.deliveryId" placeholder="请输入快递单号" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deliveryDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitDelivery" :loading="submitting">确定发货</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

const orderList = ref([])
const loading = ref(false)
const orderId = ref('')
const status = ref(null)
const page = ref(1)
const limit = ref(15)
const total = ref(0)

const deliveryDialogVisible = ref(false)
const submitting = ref(false)
const deliveryForm = ref({
  id: null,
  deliveryName: '',
  deliveryId: ''
})

const getStatusName = (status) => {
  const statusMap = {
    '0': '待发货',
    '1': '待收货',
    '2': '已收货',
    '3': '待评价',
    '-1': '已退款'
  }
  return statusMap[status] || '未知状态'
}

const getStatusType = (status) => {
  if (status === 0) return 'warning'
  if (status === 1) return 'primary'
  if (status === 2 || status === 3) return 'success'
  if (status === -1) return 'info'
  return ''
}

const fetchOrders = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/store/order/list', {
      params: { page: page.value, limit: limit.value, orderId: orderId.value, status: status.value }
    })
    if (res.data.code === 200) {
      orderList.value = res.data.data.records
      total.value = res.data.data.total
    }
  } catch (error) {
    ElMessage.error('获取订单列表失败')
  } finally {
    loading.value = false
  }
}

const handleEdit = (row) => {
  ElMessageBox.alert(
    `<div>订单号：${row.orderId}</div>
     <div>收货人：${row.realName} (${row.userPhone})</div>
     <div>支付金额：￥${row.payPrice}</div>
     <div>支付方式：${row.payType}</div>
     <div>快递公司：${row.deliveryName || '暂无'}</div>
     <div>快递单号：${row.deliveryId || '暂无'}</div>`,
    '订单详情',
    { dangerouslyUseHTMLString: true }
  )
}

const handleDeliver = (row) => {
  deliveryForm.value = {
    id: row.id,
    deliveryName: '',
    deliveryId: ''
  }
  deliveryDialogVisible.value = true
}

const submitDelivery = async () => {
  if (!deliveryForm.value.deliveryName || !deliveryForm.value.deliveryId) {
    ElMessage.warning('请填写完整的快递信息')
    return
  }
  submitting.value = true
  try {
    const res = await axios.post(`/api/admin/store/order/deliver/${deliveryForm.value.id}`, {
      deliveryName: deliveryForm.value.deliveryName,
      deliveryId: deliveryForm.value.deliveryId
    })
    if (res.data.code === 200) {
      ElMessage.success('发货成功')
      deliveryDialogVisible.value = false
      fetchOrders()
    } else {
      ElMessage.error(res.data.msg || '发货失败')
    }
  } catch (error) {
    ElMessage.error('发货请求失败')
  } finally {
    submitting.value = false
  }
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定要删除此订单吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      const res = await axios.delete(`/api/admin/store/order/delete/${id}`)
      if (res.data.code === 200) {
        ElMessage.success('删除成功')
        fetchOrders()
      }
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

onMounted(() => {
  fetchOrders()
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
