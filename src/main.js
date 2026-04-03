import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import router from './router'
import axios from 'axios'
import { ElMessage } from 'element-plus'

// 配置 axios 拦截器
axios.interceptors.request.use(
  config => {
    const token = localStorage.getItem('admin_token')
    if (token) {
      config.headers['Authorization'] = 'Bearer ' + token
      // 兼容原 PHP 后端使用的奇特请求头 Authori-zation
      config.headers['Authori-zation'] = 'Bearer ' + token
      // 如果后端使用的是 token 头
      config.headers['token'] = token
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

axios.interceptors.response.use(
  response => {
    return response
  },
  error => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('admin_token')
      router.push('/login')
      ElMessage.error('登录已过期，请重新登录')
    }
    return Promise.reject(error)
  }
)

// 将 axios 挂载到全局，这样在生成的组件里哪怕重新 import axios 也可以拦截到吗？
// 生成的组件直接 import axios from 'axios'，使用的是默认实例。
// 所以拦截器配置是生效的，因为 axios 是单例模式。

const app = createApp(App)

// Provide axios globally just in case
app.provide('axios', axios)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(ElementPlus)
app.use(router)
app.mount('#app')
