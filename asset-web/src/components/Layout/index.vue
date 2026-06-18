<template>
  <el-container class="layout-container">
    <!-- PC 侧边栏 -->
    <el-aside width="200px" class="pc-sidebar">
      <div class="logo">固定资产管理</div>
      <el-menu
        :default-active="activeMenu"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409eff"
        @select="handleMenuSelect"
      >
        <el-menu-item index="/dashboard"><el-icon><HomeFilled /></el-icon><span>主页</span></el-menu-item>
        <el-menu-item index="/catalog"><el-icon><Folder /></el-icon><span>资产目录</span></el-menu-item>
        <el-menu-item index="/categories"><el-icon><Connection /></el-icon><span>资产流动管理</span></el-menu-item>
        <el-menu-item index="/users"><el-icon><User /></el-icon><span>用户管理</span></el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 手机抽屉 -->
    <el-drawer v-model="mobileMenuVisible" direction="ltr" size="220px" :with-header="false">
      <div class="logo">固定资产管理</div>
      <el-menu :default-active="activeMenu" background-color="#304156" text-color="#bfcbd9" active-text-color="#409eff" @select="handleMobileSelect">
        <el-menu-item index="/dashboard"><el-icon><HomeFilled /></el-icon><span>主页</span></el-menu-item>
        <el-menu-item index="/catalog"><el-icon><Folder /></el-icon><span>资产目录</span></el-menu-item>
        <el-menu-item index="/categories"><el-icon><Connection /></el-icon><span>资产流动管理</span></el-menu-item>
        <el-menu-item index="/users"><el-icon><User /></el-icon><span>用户管理</span></el-menu-item>
      </el-menu>
    </el-drawer>

    <el-container>
      <el-header class="header">
        <div class="header-left">
          <el-button class="menu-toggle" link @click="mobileMenuVisible = true">
            <el-icon :size="22"><Menu /></el-icon>
          </el-button>
          <span class="page-title">{{ route.meta.title || '首页' }}</span>
        </div>
        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <span class="user-info">{{ userStore.user?.real_name || '用户' }}<el-icon><ArrowDown /></el-icon></span>
            <template #dropdown>
              <el-dropdown-menu><el-dropdown-item command="logout">退出登录</el-dropdown-item></el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="main-content">
        <router-view :key="$route.name" />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const activeMenu = computed(() => route.path)

onMounted(async () => {
  await userStore.fetchUser()
})

const handleCommand = (command: string) => {
  if (command === 'logout') {
    userStore.logout()
    router.push('/login')
  }
}

const mobileMenuVisible = ref(false)
const handleMenuSelect = (index: string) => {
  router.push(index)
}
const handleMobileSelect = (index: string) => {
  mobileMenuVisible.value = false
  router.push(index)
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.el-aside {
  background-color: #304156;
}

.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  background-color: #263445;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
  border-bottom: 1px solid #e6e6e6;
  padding: 0 20px;
}

.page-title {
  font-size: 18px;
  font-weight: 500;
  color: #303133;
}

.user-info {
  cursor: pointer;
  color: #606266;
  display: flex;
  align-items: center;
  gap: 5px;
}

.main-content {
  background: #f0f2f5;
  padding: 20px;
}

.menu-toggle { display: none; }

@media (max-width: 768px) {
  .pc-sidebar { display: none; }
  .menu-toggle { display: inline-flex; margin-right: 8px; }
  .main-content { padding: 12px; }
  .header { padding: 0 12px; }
}
</style>