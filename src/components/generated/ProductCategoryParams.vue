<template>
  <div class="category-params-container">
    <el-card shadow="never" class="box-card" :body-style="{ padding: '0' }">
      <div class="tabs-header">
        <el-tabs v-model="activeTab" class="custom-tabs" @tab-click="handleTabClick">
          <el-tab-pane label="商品品牌" name="brand"></el-tab-pane>
          <el-tab-pane label="商品单位" name="unit"></el-tab-pane>
          <el-tab-pane label="商品参数" name="specs"></el-tab-pane>
          <el-tab-pane label="保障服务" name="ensure"></el-tab-pane>
        </el-tabs>
      </div>
      <div class="tabs-content">
        <ProductProductBrand v-if="activeTab === 'brand'" />
        <ProductUnitlist v-if="activeTab === 'unit'" />
        <ProductSpecs v-if="activeTab === 'specs'" />
        <ProductEnsureCreate v-if="activeTab === 'ensure'" />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ProductProductBrand from './ProductProductBrand.vue'
import ProductUnitlist from './ProductUnitlist.vue'
import ProductSpecs from './ProductSpecs.vue'
import ProductEnsureCreate from './ProductEnsureCreate.vue'

const activeTab = ref('brand')

const handleTabClick = (tab) => {
  // 
}
</script>

<style scoped>
.category-params-container {
  padding: 10px;
}
.box-card {
  min-height: calc(100vh - 120px);
}
.tabs-header {
  padding: 0 20px;
  border-bottom: 1px solid #e4e7ed;
  background: #fff;
}
:deep(.el-tabs__header) {
  margin: 0;
  border-bottom: none;
}
.tabs-content {
  padding: 0px;
}
/* Hide the inner card headers of the embedded components since we have tabs now */
:deep(.el-card__header) {
  display: none !important;
}
:deep(.el-card) {
  border: none !important;
  box-shadow: none !important;
}
</style>
