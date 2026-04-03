<template>
  <div class="category-params-container">
    <el-card class="box-card" :body-style="{ padding: '0px', height: 'calc(100vh - 150px)' }">
      <el-container style="height: 100%;">
        <el-aside width="200px" style="border-right: 1px solid #e6e6e6; background-color: #fff;">
          <el-menu
            :default-active="activeMenu"
            class="el-menu-vertical-demo"
            @select="handleSelect"
            style="border-right: none;"
          >
            <el-menu-item index="brand">
              <span>商品品牌</span>
            </el-menu-item>
            <el-menu-item index="unit">
              <span>商品单位</span>
            </el-menu-item>
            <el-menu-item index="specs">
              <span>商品参数</span>
            </el-menu-item>
            <el-menu-item index="ensure">
              <span>保障服务</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main style="padding: 20px; background-color: #f5f7f9;">
          <ProductProductBrand v-if="activeMenu === 'brand'" />
          <ProductUnitlist v-if="activeMenu === 'unit'" />
          <ProductSpecs v-if="activeMenu === 'specs'" />
          <ProductEnsureCreate v-if="activeMenu === 'ensure'" />
        </el-main>
      </el-container>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ProductProductBrand from './ProductProductBrand.vue'
import ProductUnitlist from './ProductUnitlist.vue'
import ProductSpecs from './ProductSpecs.vue'
import ProductEnsureCreate from './ProductEnsureCreate.vue'

const activeMenu = ref('brand')

const handleSelect = (key) => {
  activeMenu.value = key
}
</script>

<style scoped>
.category-params-container {
  padding: 0;
}
:deep(.el-main .el-card) {
  border: none;
  box-shadow: none;
}
</style>
