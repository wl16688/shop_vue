<template>
  <div class="order-container">
    <el-card shadow="never" class="table-card">
      <div class="search-wrapper">
        <el-form :inline="true" :model="searchQuery" class="advanced-search-form" size="default">
          <el-row :gutter="15">
            <el-col :span="6">
              <el-form-item label="订单搜索" style="width: 100%;">
                <el-input v-model="searchQuery.orderId" placeholder="订单号/流水号" clearable />
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item label="收货人" style="width: 100%;">
                <el-input v-model="searchQuery.realName" placeholder="姓名" clearable />
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item label="联系电话" style="width: 100%;">
                <el-input v-model="searchQuery.userPhone" placeholder="手机号" clearable />
              </el-form-item>
            </el-col>
            <el-col :span="10" class="text-right">
              <el-form-item style="margin-right: 0;">
                <el-button type="primary" @click="fetchOrders">搜索</el-button>
                <el-button @click="resetSearch">重置</el-button>
                <el-button type="primary" link @click="isExpandSearch = !isExpandSearch">
                  {{ isExpandSearch ? '收起' : '高级搜索' }}
                  <el-icon><ArrowDown v-if="!isExpandSearch" /><ArrowUp v-else /></el-icon>
                </el-button>
              </el-form-item>
            </el-col>
          </el-row>

          <!-- 高级搜索展开 -->
          <el-row :gutter="15" v-show="isExpandSearch" style="margin-top: 15px;">
            <el-col :span="4">
              <el-form-item label="订单类型" style="width: 100%;">
                <el-select v-model="searchQuery.type" placeholder="全部" clearable style="width: 100%;">
                  <el-option label="普通订单" :value="1" />
                  <el-option label="秒杀订单" :value="2" />
                  <el-option label="拼团订单" :value="3" />
                  <el-option label="砍价订单" :value="4" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item label="订单状态" style="width: 100%;">
                <el-select v-model="searchQuery.status" placeholder="全部" clearable style="width: 100%;">
                  <el-option label="待发货" :value="0" />
                  <el-option label="待收货" :value="1" />
                  <el-option label="已收货" :value="2" />
                  <el-option label="待评价" :value="3" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item label="退款状态" style="width: 100%;">
                <el-select v-model="searchQuery.refundStatus" placeholder="全部" clearable style="width: 100%;">
                  <el-option label="未退款" :value="0" />
                  <el-option label="申请中" :value="1" />
                  <el-option label="已退款" :value="2" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item label="支付方式" style="width: 100%;">
                <el-select v-model="searchQuery.payType" placeholder="全部" clearable style="width: 100%;">
                  <el-option label="微信支付" value="weixin" />
                  <el-option label="支付宝" value="alipay" />
                  <el-option label="余额支付" value="yue" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>

      <div class="action-bar" style="margin-bottom: 15px;">
        <el-button type="warning" @click="handleExport" plain>导出订单数据</el-button>
        <el-button type="info" plain>打印电子面单</el-button>
      </div>

      <el-table :data="orderList" v-loading="loading" style="width: 100%" border>
        <el-table-column prop="orderId" label="订单号" width="180" align="center" />
        <el-table-column prop="realName" label="收货人" width="100" align="center" />
        <el-table-column prop="userPhone" label="联系电话" width="120" align="center" />
        <el-table-column prop="totalPrice" label="订单总价" width="100" align="center" />
        <el-table-column prop="payPrice" label="实付金额" width="100" align="center">
          <template #default="scope">
            <span style="color: #f5222d; font-weight: bold;">¥{{ scope.row.payPrice }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="payType" label="支付方式" width="100" align="center" />
        <el-table-column prop="status" label="订单状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusName(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right" align="center">
          <template #default="{ row }">
            <el-button size="small" type="primary" link @click="handleEdit(row)">详情</el-button>
            <el-button v-if="row.status === 0" size="small" type="success" link @click="handleDeliver(row)">去发货</el-button>
            <el-button size="small" type="danger" link @click="handleDelete(row.id)">删除</el-button>
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
          @current-change="fetchOrders"
          @size-change="fetchOrders"
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
import { ref, reactive, onMounted, inject } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowDown, ArrowUp } from '@element-plus/icons-vue'

const axios = inject('axios')

const orderList = ref([])
const loading = ref(false)
const total = ref(0)
const isExpandSearch = ref(false)

const searchQuery = reactive({
  orderId: '',
  realName: '',
  userPhone: '',
  status: null,
  type: null,
  refundStatus: null,
  payType: null,
  page: 1,
  limit: 15
})

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
    '3': '待评价'
  }
  return statusMap[status] || '未知状态'
}

const getStatusType = (status) => {
  if (status === 0) return 'warning'
  if (status === 1) return 'primary'
  if (status === 2 || status === 3) return 'success'
  return ''
}

const fetchOrders = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/store/order/list', { params: searchQuery })
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

const resetSearch = () => {
  searchQuery.orderId = ''
  searchQuery.realName = ''
  searchQuery.userPhone = ''
  searchQuery.status = null
  searchQuery.type = null
  searchQuery.refundStatus = null
  searchQuery.payType = null
  searchQuery.page = 1
  fetchOrders()
}

const handleEdit = (row) => {
  ElMessageBox.alert(
    `<div>订单号：${row.orderId}</div>
     <div>收货人：${row.realName} (${row.userPhone || '暂无'})</div>
     <div>支付金额：￥${row.payPrice}</div>
     <div>支付方式：${row.payType || '未知'}</div>
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

const handleExport = () => {
  ElMessage.success('开始导出订单数据...')
}

onMounted(() => {
  fetchOrders()
})
</script>

<style scoped>
.order-container {
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
