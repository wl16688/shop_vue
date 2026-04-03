import re

router_content = """import { createRouter, createWebHistory } from 'vue-router'
import Layout from '../components/Layout.vue'

const routes = [
  { path: '/login', component: () => import('../components/Login.vue') },
  {
    path: '/',
    component: Layout,
    redirect: '/home',
    meta: { requiresAuth: true },
    children: [
      { path: 'home', name: 'Home', component: () => import('../components/Dashboard.vue') },
      { path: 'menu', name: 'MenuManagement', component: () => import('../components/MenuManagement.vue') },
      { path: 'config', name: 'ConfigManagement', component: () => import('../components/ConfigManagement.vue') },
      // __GENERATED_ROUTES__
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('admin_token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
"""

with open('/workspace/shop_vue/src/router/index.js', 'w') as f:
    f.write(router_content)

