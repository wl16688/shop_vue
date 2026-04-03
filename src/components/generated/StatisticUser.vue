<template>
  <div class="user-statistic-container">
    <!-- Header -->
    <div class="header-section">
      <h2 class="page-title">用户概况</h2>
      <el-button type="primary" plain icon="Download" @click="handleExport">导出数据</el-button>
    </div>

    <!-- Basic Info Cards -->
    <el-row :gutter="20" class="basic-info-row">
      <el-col :span="4">
        <el-card shadow="hover" class="info-card">
          <div class="info-title">用户总数</div>
          <div class="info-value">{{ basicData.totalUser || 0 }}</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="hover" class="info-card">
          <div class="info-title">今日新增用户</div>
          <div class="info-value">{{ basicData.todayNew || 0 }}</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="hover" class="info-card">
          <div class="info-title">昨日新增用户</div>
          <div class="info-value">{{ basicData.yesterdayNew || 0 }}</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="hover" class="info-card">
          <div class="info-title">本月新增用户</div>
          <div class="info-value">{{ basicData.monthNew || 0 }}</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="hover" class="info-card">
          <div class="info-title">付费会员总数</div>
          <div class="info-value">{{ basicData.totalVip || 0 }}</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="hover" class="info-card">
          <div class="info-title">总访问量</div>
          <div class="info-value">{{ basicData.totalVisitor || 0 }}</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Trend Chart -->
    <el-card shadow="hover" class="chart-card">
      <template #header>
        <div class="card-header">
          <span>用户趋势</span>
          <el-radio-group v-model="trendDays" size="small" @change="fetchTrend">
            <el-radio-button :label="7">7天</el-radio-button>
            <el-radio-button :label="15">15天</el-radio-button>
            <el-radio-button :label="30">30天</el-radio-button>
          </el-radio-group>
        </div>
      </template>
      <div ref="trendChartRef" style="height: 350px; width: 100%;"></div>
    </el-card>

    <!-- Region & Gender -->
    <el-row :gutter="20" class="bottom-row">
      <el-col :span="12">
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="card-header">
              <span>用户地区排行 (Top 10)</span>
            </div>
          </template>
          <el-table :data="regionData" style="width: 100%" max-height="350">
            <el-table-column type="index" label="排名" width="80" align="center">
              <template #default="scope">
                <span :class="['rank-badge', `rank-${scope.$index + 1}`]">{{ scope.$index + 1 }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="name" label="省份/地区" />
            <el-table-column prop="value" label="用户数" width="120" />
            <el-table-column prop="percent" label="占比" width="100">
              <template #default="scope">
                <el-progress :percentage="parseFloat(scope.row.percent)" :show-text="false" color="#3e75f5" />
                <span class="progress-text">{{ scope.row.percent }}</span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="card-header">
              <span>用户性别比例</span>
            </div>
          </template>
          <div ref="sexChartRef" style="height: 350px; width: 100%;"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, inject, nextTick, markRaw } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'

const axios = inject('axios')

// State
const basicData = ref({})
const trendDays = ref(30)
const regionData = ref([])

// Chart Refs
const trendChartRef = ref(null)
const sexChartRef = ref(null)

let trendChartInstance = null
let sexChartInstance = null

const fetchBasic = async () => {
  try {
    const res = await axios.get('/api/admin/statistic/user/get_basic')
    if (res.data.code === 200) {
      basicData.value = res.data.data
    }
  } catch (error) {
    console.error('Failed to fetch basic data', error)
  }
}

const fetchTrend = async () => {
  try {
    const res = await axios.get(`/api/admin/statistic/user/get_trend?days=${trendDays.value}`)
    if (res.data.code === 200) {
      renderTrendChart(res.data.data)
    }
  } catch (error) {
    console.error('Failed to fetch trend data', error)
  }
}

const fetchRegion = async () => {
  try {
    const res = await axios.get('/api/admin/statistic/user/get_region')
    if (res.data.code === 200) {
      regionData.value = res.data.data
    }
  } catch (error) {
    console.error('Failed to fetch region data', error)
  }
}

const fetchSex = async () => {
  try {
    const res = await axios.get('/api/admin/statistic/user/get_sex')
    if (res.data.code === 200) {
      renderSexChart(res.data.data)
    }
  } catch (error) {
    console.error('Failed to fetch sex data', error)
  }
}

const renderTrendChart = (data) => {
  if (!trendChartRef.value) return
  if (!trendChartInstance) {
    trendChartInstance = markRaw(echarts.init(trendChartRef.value))
  }
  
  const option = {
    tooltip: { trigger: 'axis' },
    legend: { data: ['新增用户', '活跃用户'], bottom: 0 },
    grid: { left: '3%', right: '4%', bottom: '10%', containLabel: true },
    xAxis: { type: 'category', boundaryGap: false, data: data.dates },
    yAxis: { type: 'value' },
    series: [
      {
        name: '新增用户',
        type: 'line',
        smooth: true,
        data: data.newUsers,
        itemStyle: { color: '#3e75f5' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(62,117,245,0.3)' },
            { offset: 1, color: 'rgba(62,117,245,0)' }
          ])
        }
      },
      {
        name: '活跃用户',
        type: 'line',
        smooth: true,
        data: data.activeUsers,
        itemStyle: { color: '#19be6b' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(25,190,107,0.3)' },
            { offset: 1, color: 'rgba(25,190,107,0)' }
          ])
        }
      }
    ]
  }
  trendChartInstance.setOption(option)
}

const renderSexChart = (data) => {
  if (!sexChartRef.value) return
  if (!sexChartInstance) {
    sexChartInstance = markRaw(echarts.init(sexChartRef.value))
  }
  
  const option = {
    tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
    legend: { bottom: '0', left: 'center' },
    series: [
      {
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
          label: { show: true, fontSize: '20', fontWeight: 'bold' }
        },
        labelLine: { show: false },
        data: data.map(item => ({
          value: item.value,
          name: item.name,
          itemStyle: {
            color: item.name === '男' ? '#3e75f5' : item.name === '女' ? '#ff9900' : '#c8c9cc'
          }
        }))
      }
    ]
  }
  sexChartInstance.setOption(option)
}

const handleExport = async () => {
  ElMessage.success('导出任务已提交')
  try {
    await axios.get('/api/admin/statistic/user/get_excel')
  } catch (e) {
    // mock success
  }
}

const resizeCharts = () => {
  if (trendChartInstance) trendChartInstance.resize()
  if (sexChartInstance) sexChartInstance.resize()
}

onMounted(() => {
  fetchBasic()
  fetchTrend()
  fetchRegion()
  fetchSex()
  window.addEventListener('resize', resizeCharts)
})

onUnmounted(() => {
  window.removeEventListener('resize', resizeCharts)
  if (trendChartInstance) trendChartInstance.dispose()
  if (sexChartInstance) sexChartInstance.dispose()
})
</script>

<style scoped>
.user-statistic-container {
  padding: 10px;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.basic-info-row {
  margin-bottom: 20px;
}

.info-card {
  text-align: center;
  padding: 10px 0;
}

.info-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 10px;
}

.info-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.chart-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.rank-badge {
  display: inline-block;
  width: 24px;
  height: 24px;
  line-height: 24px;
  border-radius: 50%;
  background-color: #f4f4f5;
  color: #909399;
  font-weight: bold;
}

.rank-1 { background-color: #f56c6c; color: #fff; }
.rank-2 { background-color: #e6a23c; color: #fff; }
.rank-3 { background-color: #3e75f5; color: #fff; }

.progress-text {
  font-size: 12px;
  color: #606266;
  margin-left: 5px;
}

:deep(.el-progress) {
  width: 100%;
  display: inline-block;
  vertical-align: middle;
}

:deep(.el-progress-bar) {
  padding-right: 0;
  width: 60%;
}
</style>
