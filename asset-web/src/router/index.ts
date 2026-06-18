import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue'),
  },
  {
    path: '/scan',
    name: 'Scan',
    component: () => import('@/views/scan/index.vue'),
    meta: { title: '扫码识别' },
  },
  {
    path: '/scan/result/:id',
    name: 'ScanResult',
    component: () => import('@/views/scan/result.vue'),
    meta: { title: '扫码结果' },
  },
  {
    path: '/',
    component: () => import('@/components/Layout/index.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '主页' },
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('@/views/user/list.vue'),
        meta: { title: '用户管理' },
      },
      {
        path: 'catalog',
        name: 'Catalog',
        component: () => import('@/views/asset-catalog/index.vue'),
        meta: { title: '资产目录' },
      },
      {
        path: 'categories',
        name: 'Categories',
        component: () => import('@/views/category/list.vue'),
        meta: { title: '资产流动管理' },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token')
  const isPublic = to.path === '/login' || to.path.startsWith('/scan/result/')
  if (!isPublic && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/')
  } else {
    next()
  }
})

export default router