<template>
  <div class="scan-result">
    <el-card v-if="asset" v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>扫码结果</span>
          <div>
            <el-button @click="$router.push('/scan')">继续扫码</el-button>
            <el-button @click="$router.push('/categories')">返回列表</el-button>
          </div>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="资产编号">{{ asset.asset_code }}</el-descriptions-item>
        <el-descriptions-item label="设备名称">{{ asset.name }}</el-descriptions-item>
        <el-descriptions-item label="公司编号">{{ asset.company_code || '-' }}</el-descriptions-item>
        <el-descriptions-item label="SN号">{{ asset.sn || '-' }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="statusType">{{ statusLabel }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="所属部门">{{ asset.department || '-' }}</el-descriptions-item>
        <el-descriptions-item label="存放位置">{{ asset.location || '-' }}</el-descriptions-item>
        <el-descriptions-item label="负责人ID">{{ asset.user_id || '-' }}</el-descriptions-item>
      </el-descriptions>

      <div class="actions">
        <el-button type="warning" @click="handleBorrow" :disabled="asset.status !== 'normal'">出借</el-button>
        <el-button type="success" @click="handleReturn" :disabled="asset.status !== 'borrowed'">归还</el-button>
        <el-button type="danger" @click="handleScrap" :disabled="asset.status === 'scrapped'">报废</el-button>
        <el-button type="info" @click="handleChange">变动</el-button>
      </div>
    </el-card>

    <el-result v-else-if="!loading" icon="error" title="设备未找到" sub-title="请确认二维码是否正确">
      <template #extra>
        <el-button type="primary" @click="$router.push('/scan')">重新扫码</el-button>
      </template>
    </el-result>

    <BorrowDialog v-model="borrowVisible" :asset="asset" :users="userList" @success="onBorrowSuccess" />
    <ReturnDialog v-model="returnVisible" :asset="asset" @success="onReturnSuccess" />
    <ChangeDialog v-model="changeVisible" :asset="asset" :categories="categories" :users="userList" @success="onChangeSuccess" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getAsset, getAssets, scrapAsset } from '@/api/asset'
import request from '@/api/request'
import type { Asset, Category, User } from '@/types'
import BorrowDialog from '@/components/BorrowDialog.vue'
import ReturnDialog from '@/components/ReturnDialog.vue'
import ChangeDialog from '@/components/ChangeDialog.vue'

const route = useRoute()
const router = useRouter()

const asset = ref<Asset | null>(null)
const loading = ref(true)
const categories = ref<Category[]>([])
const userList = ref<User[]>([])

const borrowVisible = ref(false)
const returnVisible = ref(false)
const changeVisible = ref(false)

const statusLabel = computed(() => {
  const map: Record<string, string> = { normal: '在库', borrowed: '已借出', scrapped: '已报废' }
  return map[asset.value?.status || ''] || asset.value?.status || ''
})

const statusType = computed(() => {
  const map: Record<string, string> = { normal: 'success', borrowed: 'warning', scrapped: 'danger' }
  return map[asset.value?.status || ''] || 'info'
})

const fetchAsset = async () => {
  loading.value = true
  try {
    const code = route.params.id as string
    // 数字 ID 直接用 getAsset，否则按 asset_code 查
    if (/^\d+$/.test(code)) {
      const { data } = await getAsset(Number(code))
      asset.value = data.data
    } else {
      const { data: listData } = await getAssets({ keyword: code, page_size: 1 })
      if (listData.data.items.length > 0) {
        const { data } = await getAsset(listData.data.items[0].id)
        asset.value = data.data
      } else {
        asset.value = null
      }
    }
  } catch (e) {
    asset.value = null
  } finally {
    loading.value = false
  }
}

const fetchCategories = async () => {
  try {
    const { data } = await request.get('/categories', { params: { page: 1, page_size: 100 } })
    categories.value = data.data.items
  } catch (e) { /* ignore */ }
}

const requireLogin = (): boolean => {
  if (!localStorage.getItem('token')) {
    localStorage.setItem('redirect', route.fullPath)
    ElMessage.warning('请先登录')
    router.push('/login')
    return false
  }
  return true
}

const handleBorrow = () => {
  if (!requireLogin()) return
  borrowVisible.value = true
}

const handleReturn = () => { if (!requireLogin()) return; returnVisible.value = true }
const onReturnSuccess = () => { returnVisible.value = false; fetchAsset() }

const handleScrap = async () => {
  if (!requireLogin()) return
  if (!asset.value) return
  try {
    await ElMessageBox.confirm(`确认报废设备【${asset.value.name}】吗？`, '报废确认', { type: 'warning' })
    await scrapAsset(asset.value.id, '扫码报废')
    ElMessage.success('报废成功')
    fetchAsset()
  } catch (e: any) {
    if (e !== 'cancel' && e !== 'close') console.error(e)
  }
}

const handleChange = () => {
  if (!requireLogin()) return
  changeVisible.value = true
}

const onBorrowSuccess = () => {
  fetchAsset()
}

const onChangeSuccess = () => {
  fetchAsset()
}

const fetchUsers = async () => {
  try {
    const { data } = await request.get('/users', { params: { page: 1, page_size: 100 } })
    userList.value = data.data.items
  } catch (e) { /* ignore */ }
}

onMounted(() => {
  fetchAsset()
  fetchCategories()
  fetchUsers()
})
</script>

<style scoped>
.scan-result {
  max-width: 800px;
  margin: 20px auto;
  padding: 0 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.actions {
  margin-top: 24px;
  display: flex;
  gap: 12px;
  justify-content: center;
}
</style>
