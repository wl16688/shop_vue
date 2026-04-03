<template>
  <div class="dashboard-container">
    <div class="header-banner">
      <h2>工作台</h2>
      <p>欢迎来到商城后台管理系统</p>
    </div>

    <!-- 首页统计数据 -->
    <el-row :gutter="20" class="stat-row">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card blue">
          <div class="stat-icon"><el-icon><User /></el-icon></div>
          <div class="stat-info">
            <div class="stat-title">总用户数</div>
            <div class="stat-value">1,205</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card green">
          <div class="stat-icon"><el-icon><List /></el-icon></div>
          <div class="stat-info">
            <div class="stat-title">总订单数</div>
            <div class="stat-value">3,456</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card orange">
          <div class="stat-icon"><el-icon><Money /></el-icon></div>
          <div class="stat-info">
            <div class="stat-title">总交易额</div>
            <div class="stat-value">¥ 45,230.00</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card purple">
          <div class="stat-icon"><el-icon><Goods /></el-icon></div>
          <div class="stat-info">
            <div class="stat-title">商品总数</div>
            <div class="stat-value">128</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="chart-row">
      <!-- 首页订单图表 -->
      <el-col :span="12">
        <el-card shadow="never" class="chart-card">
          <template #header>
            <div class="card-header">
              <span>订单量趋势 (近30天)</span>
            </div>
          </template>
          <div class="chart-box" ref="orderChartRef"></div>
        </el-card>
      </el-col>
      <!-- 首页用户图表 -->
      <el-col :span="12">
        <el-card shadow="never" class="chart-card">
          <template #header>
            <div class="card-header">
              <span>新增用户趋势 (近30天)</span>
            </div>
          </template>
          <div class="chart-box" ref="userChartRef"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="chart-row">
      <!-- 首页商品图表 -->
      <el-col :span="8">
        <el-card shadow="never" class="chart-card">
          <template #header>
            <div class="card-header">
              <span>商品数据占比</span>
            </div>
          </template>
          <div class="chart-box" ref="productChartRef"></div>
        </el-card>
      </el-col>
      
      <!-- 首页用户数据详情 -->
      <el-col :span="8">
        <el-card shadow="never" class="chart-card">
          <template #header>
            <div class="card-header">
              <span>用户数据详情 (Top 5)</span>
            </div>
          </template>
          <el-table :data="userTableData" style="width: 100%" size="small">
            <el-table-column prop="rank" label="排名" width="60" />
            <el-table-column prop="name" label="用户名称" />
            <el-table-column prop="consume" label="累计消费" width="100" />
          </el-table>
        </el-card>
      </el-col>

      <!-- 首页商品数据详情 -->
      <el-col :span="8">
        <el-card shadow="never" class="chart-card">
          <template #header>
            <div class="card-header">
              <span>商品销量排行 (Top 5)</span>
            </div>
          </template>
          <el-table :data="productTableData" style="width: 100%" size="small">
            <el-table-column prop="rank" label="排名" width="60" />
            <el-table-column prop="name" label="商品名称" show-overflow-tooltip />
            <el-table-column prop="sales" label="销量" width="80" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { User, List, Money, Goods } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

const orderChartRef = ref(null)
const userChartRef = ref(null)
const productChartRef = ref(null)

let orderChart = null
let userChart = null
let productChart = null

// Mock Data for Tables
const userTableData = ref([
  { rank: 1, name: '用户_A8x9', consume: '¥ 12,300' },
  { rank: 2, name: '用户_B2y1', consume: '¥ 8,450' },
  { rank: 3, name: '用户_C7z3', consume: '¥ 6,200' },
  { rank: 4, name: '用户_D4w5', consume: '¥ 4,100' },
  { rank: 5, name: '用户_E1v7', consume: '¥ 3,800' }
])

const productTableData = ref([
  { rank: 1, name: 'Apple iPhone 15 Pro', sales: '345' },
  { rank: 2, name: '华为 Mate 60 Pro', sales: '298' },
  { rank: 3, name: '小米 14 Ultra', sales: '256' },
  { rank: 4, name: 'DJI 大疆无人机', sales: '189' },
  { rank: 5, name: 'Sony 降轴耳机', sales: '150' }
])

const initCharts = () => {
  // 1. Order Chart
  if (orderChartRef.value) {
    orderChart = echarts.init(orderChartRef.value)
    orderChart.setOption({
      tooltip: { trigger: 'axis' },
      grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
      xAxis: { type: 'category', boundaryGap: false, data: ['1日', '5日', '10日', '15日', '20日', '25日', '30日'] },
      yAxis: { type: 'value' },
      series: [{
        name: '订单量',
        type: 'line',
        smooth: true,
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(82, 196, 26, 0.5)' },
            { offset: 1, color: 'rgba(82, 196, 26, 0.1)' }
          ])
        },
        itemStyle: { color: '#52c41a' },
        data: [120, 132, 101, 134, 90, 230, 210]
      }]
    })
  }

  // 2. User Chart
  if (userChartRef.value) {
    userChart = echarts.init(userChartRef.value)
    userChart.setOption({
      tooltip: { trigger: 'axis' },
      grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
      xAxis: { type: 'category', data: ['1日', '5日', '10日', '15日', '20日', '25日', '30日'] },
      yAxis: { type: 'value' },
      series: [{
        name: '新增用户',
        type: 'bar',
        barWidth: '40%',
        itemStyle: { color: '#1890ff', borderRadius: [4, 4, 0, 0] },
        data: [10, 52, 200, 334, 390, 330, 220]
      }]
    })
  }

  // 3. Product Chart
  if (productChartRef.value) {
    productChart = echarts.init(productChartRef.value)
    productChart.setOption({
      tooltip: { trigger: 'item' },
      legend: { bottom: '0%', left: 'center' },
      series: [{
        name: '商品状态',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: { show: false, position: 'center' },
        emphasis: {
          label: { show: true, fontSize: 20, fontWeight: 'bold' }
        },
        labelLine: { show: false },
        data: [
          { value: 1048, name: '出售中' },
          { value: 735, name: '仓库中' },
          { value: 580, name: '已售罄' },
          { value: 484, name: '回收站' },
          { value: 300, name: '库存预警' }
        ]
      }]
    })
  }
}

const handleResize = () => {
  orderChart?.resize()
  userChart?.resize()
  productChart?.resize()
}

onMounted(() => {
  setTimeout(() => {
    initCharts()
    window.addEventListener('resize', handleResize)
  }, 100)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  orderChart?.dispose()
  userChart?.dispose()
  productChart?.dispose()
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  background-color: #f0f2f5;
  min-height: 100%;
}
.header-banner {
  background-color: #fff;
  padding: 20px;
  border-radius: 4px;
  margin-bottom: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.header-banner h2 {
  margin: 0 0 10px 0;
  font-size: 20px;
  color: #333;
}
.header-banner p {
  margin: 0;
  color: #666;
  font-size: 14px;
}
.stat-row, .chart-row {
  margin-bottom: 20px;
}
.stat-card {
  border: none;
  border-radius: 4px;
}
:deep(.stat-card .el-card__body) {
  display: flex;
  align-items: center;
  padding: 20px;
}
.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 30px;
  margin-right: 15px;
}
.stat-info {
  flex: 1;
}
.stat-title {
  color: #909399;
  font-size: 14px;
  margin-bottom: 8px;
}
.stat-value {
  color: #303133;
  font-size: 24px;
  font-weight: bold;
}

/* Colors */
.blue .stat-icon { background: rgba(24, 144, 255, 0.1); color: #1890ff; }
.green .stat-icon { background: rgba(82, 196, 26, 0.1); color: #52c41a; }
.orange .stat-icon { background: rgba(250, 140, 22, 0.1); color: #fa8c16; }
.purple .stat-icon { background: rgba(114, 46, 209, 0.1); color: #722ed1; }

.chart-card {
  border: none;
  border-radius: 4px;
  height: 380px;
}
.card-header {
  font-weight: bold;
}
.chart-box {
  height: 280px;
  width: 100%;
}
</style>
