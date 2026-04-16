<template>
  <div class="coupon-container">
    <el-card shadow="never" class="table-card">
      <div class="search-wrapper">
        <el-form :inline="true" :model="searchQuery" class="advanced-search-form" size="default">
          <el-row :gutter="15">
            <el-col :span="6">
              <el-form-item label="优惠券名称" style="width: 100%;">
                <el-input v-model="searchQuery.keyword" placeholder="请输入优惠券名称" clearable />
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item label="状态" style="width: 100%;">
                <el-select v-model="searchQuery.status" placeholder="全部状态" clearable style="width: 100%;">
                  <el-option label="正常" :value="1" />
                  <el-option label="无效" :value="0" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item label="发放类型" style="width: 100%;">
                <el-select v-model="searchQuery.type" placeholder="全部" clearable style="width: 100%;">
                  <el-option label="通用券" :value="0" />
                  <el-option label="品类券" :value="1" />
                  <el-option label="商品券" :value="2" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="10" class="text-right">
              <el-form-item style="margin-right: 0;">
                <el-button type="primary" @click="fetchCoupons">搜索</el-button>
                <el-button @click="resetSearch">重置</el-button>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>

      <div class="action-bar" style="margin-bottom: 15px;">
        <el-button type="success" @click="handleAdd">发布优惠券</el-button>
      </div>

      <el-table :data="couponList" v-loading="loading" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column prop="couponTitle" label="优惠券名称" min-width="150" />
        <el-table-column prop="couponType" label="优惠券类型" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.couponType === 1 ? 'danger' : 'warning'" size="small">
              {{ row.couponType === 1 ? '满减券' : '折扣券' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="type" label="适用范围" width="100" align="center">
          <template #default="{ row }">
            {{ row.type === 0 ? '通用券' : row.type === 1 ? '品类券' : '商品券' }}
          </template>
        </el-table-column>
        <el-table-column prop="couponPrice" label="面值/折扣" width="100" align="center">
          <template #default="{ row }">
             <span style="color: #f5222d; font-weight: bold;">
               {{ row.couponType === 1 ? '¥' + row.couponPrice : row.couponPrice + '折' }}
             </span>
          </template>
        </el-table-column>
        <el-table-column prop="useMinPrice" label="最低消费" width="100" align="center" />
        <el-table-column prop="totalCount" label="发行总量" width="100" align="center">
          <template #default="{ row }">
            {{ row.totalCount === 0 ? '不限量' : row.totalCount }}
          </template>
        </el-table-column>
        <el-table-column prop="remainCount" label="剩余数量" width="100" align="center">
           <template #default="{ row }">
            {{ row.totalCount === 0 ? '充足' : row.remainCount }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-switch v-model="row.status" :active-value="1" :inactive-value="0" @change="handleStatusChange(row)" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right" align="center">
          <template #default="{ row }">
            <el-button size="small" type="primary" link @click="handleEdit(row)">编辑</el-button>
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
          @current-change="fetchCoupons"
          @size-change="fetchCoupons"
        />
      </div>
    </el-card>

    <!-- Dialog -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px">
      <el-form label-width="120px" :model="form" ref="formRef">
        <el-form-item label="优惠券名称" required>
          <el-input v-model="form.couponTitle" placeholder="请输入优惠券名称"></el-input>
        </el-form-item>
        <el-row>
          <el-col :span="12">
            <el-form-item label="优惠券类型">
              <el-select v-model="form.couponType" style="width: 100%;">
                <el-option label="满减券" :value="1" />
                <el-option label="折扣券" :value="2" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="适用范围">
              <el-select v-model="form.type" style="width: 100%;">
                <el-option label="通用券" :value="0" />
                <el-option label="品类券" :value="1" />
                <el-option label="商品券" :value="2" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="面值/折扣" required>
              <el-input-number v-model="form.couponPrice" :min="0" style="width: 100%;" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="最低消费" required>
              <el-input-number v-model="form.useMinPrice" :min="0" style="width: 100%;" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="发行总量">
              <el-input-number v-model="form.totalCount" :min="0" placeholder="0为不限量" style="width: 100%;" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态">
              <el-switch v-model="form.status" :active-value="1" :inactive-value="0" active-text="开启" inactive-text="关闭" />
            </el-form-item>
          </el-col>
        </el-row>
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
import { ref, reactive, onMounted, inject } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const axios = inject('axios')

const couponList = ref([])
const loading = ref(false)
const total = ref(0)

const dialogVisible = ref(false)
const dialogTitle = ref('发布优惠券')

const searchQuery = reactive({
  keyword: '',
  status: null,
  type: null,
  page: 1,
  limit: 15
})

const form = reactive({
  id: null,
  couponTitle: '',
  couponType: 1,
  type: 0,
  couponPrice: 0,
  useMinPrice: 0,
  totalCount: 0,
  status: 1
})

const fetchCoupons = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/store/coupon/list', { params: searchQuery })
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

const resetSearch = () => {
  searchQuery.keyword = ''
  searchQuery.status = null
  searchQuery.type = null
  searchQuery.page = 1
  fetchCoupons()
}

const handleAdd = () => {
  dialogTitle.value = '发布优惠券'
  form.id = null
  form.couponTitle = ''
  form.couponType = 1
  form.type = 0
  form.couponPrice = 0
  form.useMinPrice = 0
  form.totalCount = 0
  form.status = 1
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑优惠券'
  Object.assign(form, row)
  dialogVisible.value = true
}

const handleStatusChange = async (row) => {
  try {
    const res = await axios.post('/api/admin/store/coupon/save', row)
    if (res.data.code === 200) {
      ElMessage.success('状态更新成功')
    } else {
      row.status = row.status === 1 ? 0 : 1
      ElMessage.error(res.data.msg || '状态更新失败')
    }
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
      } else {
        ElMessage.error(res.data.msg || '删除失败')
      }
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

const submitForm = async () => {
  if (!form.couponTitle) return ElMessage.warning('请输入优惠券名称')
  try {
    const res = await axios.post(`/api/admin/store/coupon/save`, form)
    if (res.data.code === 200) {
      ElMessage.success(form.id ? '编辑成功' : '发布成功')
      dialogVisible.value = false
      fetchCoupons()
    } else {
      ElMessage.error(res.data.msg || '保存失败')
    }
  } catch(e) {
    ElMessage.error('网络错误')
  }
}

onMounted(() => {
  fetchCoupons()
})
</script>

<style scoped>
.coupon-container {
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
