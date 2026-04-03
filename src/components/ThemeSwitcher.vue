<template>
  <component :is="currentLayout" />
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import LayoutV1 from './Layout.vue'
import LayoutV2 from './LayoutV2.vue'

const theme = ref('v1')

onMounted(() => {
  const storedTheme = localStorage.getItem('ui_theme')
  if (storedTheme) {
    theme.value = storedTheme
  }
})

const currentLayout = computed(() => {
  return theme.value === 'v2' ? LayoutV2 : LayoutV1
})
</script>
