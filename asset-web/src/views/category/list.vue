<template>
  <div class="flow-management">
    <el-row :gutter="16">
      <!-- 左侧：设备列表 -->
      <el-col :xs="24" :sm="24" :md="14">
        <el-card>
          <template #header><span>设备列表</span></template>
          <el-input v-model="searchKeyword" placeholder="搜索设备名称/编号" clearable style="margin-bottom: 12px" @change="fetchDevices" />
          <div class="filter-row" style="margin-bottom: 12px">
            <el-button :type="statusFilter === '' ? 'primary' : 'default'" size="small" @click="filterByStatus('')">全部设备（{{ devices.length }}）</el-button>
            <el-button :type="statusFilter === 'normal' ? 'success' : 'default'" size="small" @click="filterByStatus('normal')">在库（{{ counts.normal }}）</el-button>
            <el-button :type="statusFilter === 'borrowed' ? 'warning' : 'default'" size="small" @click="filterByStatus('borrowed')">已借出（{{ counts.borrowed }}）</el-button>
            <el-button :type="statusFilter === 'scrapped' ? 'danger' : 'default'" size="small" @click="filterByStatus('scrapped')">已报废（{{ counts.scrapped }}）</el-button>
          </div>
          <el-table :data="filteredDevices" v-loading="loading" border stripe highlight-current-row @row-click="selectDevice" size="small" max-height="calc(100vh - 300px)">
            <el-table-column prop="asset_code" label="资产编号" width="140" />
            <el-table-column prop="name" label="设备名称" min-width="140" />
            <el-table-column label="分类" width="100">
              <template #default="{ row }">{{ getCategoryName(row.category_id) }}</template>
            </el-table-column>
            <el-table-column label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)" size="small">{{ getStatusLabel(row.status) }}</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <!-- 右侧：流转记录 + 操作 -->
      <el-col :xs="24" :sm="24" :md="10">
        <el-card v-if="!selectedDevice" style="height: 100%; display: flex; align-items: center; justify-content: center">
          <div style="text-align: center; color: #909399; padding: 80px 0">
            <el-icon :size="48"><Connection /></el-icon>
            <p style="margin-top: 16px">请从左侧选择设备</p>
            <p style="font-size: 12px">查看流转记录与执行操作</p>
          </div>
        </el-card>

        <template v-else>
          <!-- 设备信息 + 操作 -->
          <el-card style="margin-bottom: 16px">
            <template #header>
              <div class="card-header">
                <span>{{ selectedDevice.name }}</span>
                <el-tag :type="getStatusType(selectedDevice.status)" size="small">{{ getStatusLabel(selectedDevice.status) }}</el-tag>
              </div>
            </template>
            <el-descriptions :column="2" size="small" border>
              <el-descriptions-item label="资产编号">{{ selectedDevice.asset_code }}</el-descriptions-item>
              <el-descriptions-item label="分类">{{ getCategoryName(selectedDevice.category_id) }}</el-descriptions-item>
              <el-descriptions-item label="负责人">{{ selectedDevice.owner_name || selectedDevice.user_id || '-' }}</el-descriptions-item>
              <el-descriptions-item label="所属部门">{{ selectedDevice.department || '-' }}</el-descriptions-item>
              <el-descriptions-item label="存放位置">{{ selectedDevice.location || '-' }}</el-descriptions-item>
              <el-descriptions-item label="采购日期">{{ selectedDevice.purchase_date || '-' }}</el-descriptions-item>
            </el-descriptions>
            <div class="actions">
              <el-button type="warning" @click="handleBorrow" :disabled="selectedDevice.status !== 'normal'">
                <el-icon><Switch /></el-icon> 出借
              </el-button>
              <el-button type="success" @click="handleReturn" :disabled="selectedDevice.status !== 'borrowed'">
                <el-icon><CircleCheck /></el-icon> 归还
              </el-button>
              <el-button type="danger" @click="handleCancelBorrow" :disabled="selectedDevice.status !== 'borrowed'" plain>
                <el-icon><Close /></el-icon> 取消出借
              </el-button>
              <el-button type="info" @click="handleChange">
                <el-icon><Edit /></el-icon> 变动
              </el-button>
            </div>
          </el-card>

          <!-- 流转记录 -->
          <el-card>
            <template #header><span>流转记录</span></template>
            <el-tabs v-model="activeTab">
              <el-tab-pane label="全部" name="all" />
              <el-tab-pane label="出借/归还" name="borrow" />
              <el-tab-pane label="变动记录" name="change" />
            </el-tabs>
            <div v-if="activeTab === 'all' || activeTab === 'borrow'">
              <h4 style="margin-bottom: 8px; color: #606266">出借归还记录</h4>
              <el-timeline v-if="borrowRecords.length > 0">
                <el-timeline-item v-for="r in borrowRecords" :key="r.id" :timestamp="r.time" :color="r.status === 'borrowed' ? '#e6a23c' : '#67c23a'">
                  {{ r.title }} — {{ r.desc }}
                  <div v-if="r.photo_url || r.return_photo_url" style="margin-top: 6px">
                    <el-image v-if="r.photo_url" :src="r.photo_url" style="width:80px;height:80px;border-radius:6px;margin-right:6px" fit="cover" :preview-src-list="[r.photo_url]" />
                    <el-image v-if="r.return_photo_url" :src="r.return_photo_url" style="width:80px;height:80px;border-radius:6px" fit="cover" :preview-src-list="[r.return_photo_url]" />
                  </div>
                </el-timeline-item>
              </el-timeline>
              <p v-else style="color: #909399; padding: 12px">暂无记录</p>
            </div>
            <div v-if="activeTab === 'all' || activeTab === 'change'" style="margin-top: 16px">
              <h4 style="margin-bottom: 8px; color: #606266">变动记录</h4>
              <el-timeline v-if="changeRecords.length > 0">
                <el-timeline-item v-for="r in changeRecords" :key="r.id" :timestamp="r.time" :color="r.change_type === 'owner' ? '#9b59b6' : '#909399'">
                  {{ r.title }}: {{ r.desc }}
                </el-timeline-item>
              </el-timeline>
              <p v-else style="color: #909399; padding: 12px">暂无记录</p>
            </div>
          </el-card>
        </template>
      </el-col>
    </el-row>

    <!-- 出借弹窗 -->
    <BorrowDialog v-model="borrowVisible" :asset="selectedDevice" :users="userList" @success="onBorrowSuccess" />
    <!-- 归还弹窗 -->
    <ReturnDialog v-model="returnVisible" :asset="selectedDevice" @success="onReturnSuccess" />
    <!-- 变动弹窗 -->
    <ChangeDialog v-model="changeVisible" :asset="selectedDevice" :categories="categories" :users="userList" @success="onChangeSuccess" />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getAssets } from '@/api/asset'
import { cancelBorrow, getBorrowHistory } from '@/api/borrow'
import { getChangeHistory } from '@/api/change'
import request from '@/api/request'
import type { Asset, Category, User } from '@/types'
import BorrowDialog from '@/components/BorrowDialog.vue'
import ChangeDialog from '@/components/ChangeDialog.vue'
import ReturnDialog from '@/components/ReturnDialog.vue'

const loading = ref(false)
const searchKeyword = ref('')
const statusFilter = ref('')
const activeTab = ref('all')

const devices = ref<Asset[]>([])
const categories = ref<Category[]>([])
const userList = ref<User[]>([])
const selectedDevice = ref<Asset | null>(null)

const counts = computed(() => ({
  normal: devices.value.filter(d => d.status === 'normal').length,
  borrowed: devices.value.filter(d => d.status === 'borrowed').length,
  scrapped: devices.value.filter(d => d.status === 'scrapped').length,
}))

const filterByStatus = (s: string) => { statusFilter.value = s }
const filteredDevices = computed(() => {
  if (!statusFilter.value) return devices.value
  return devices.value.filter(d => d.status === statusFilter.value)
})

const borrowRecords = ref<any[]>([])
const changeRecords = ref<any[]>([])

const borrowVisible = ref(false)
const returnVisible = ref(false)
const changeVisible = ref(false)

const getCategoryName = (id: number) => { const c = categories.value.find(x => x.id === id); return c?.name || String(id) }
const getStatusType = (s: string) => ({ normal: 'success', borrowed: 'warning', scrapped: 'danger' } as any)[s] || 'info'
const getStatusLabel = (s: string) => ({ normal: '在库', borrowed: '已借出', scrapped: '已报废' } as any)[s] || s

const fetchDevices = async () => {
  loading.value = true
  try {
    const p: any = { page: 1, page_size: 100 }
    if (searchKeyword.value) p.keyword = searchKeyword.value
    const { data } = await getAssets(p)
    devices.value = data.data.items
  } catch (e) { ElMessage.error('操作失败') } finally { loading.value = false }
}

const fetchCategories = async () => { try { const { data } = await request.get('/categories', { params: { page: 1, page_size: 100 } }); categories.value = data.data.items } catch (e) { ElMessage.error('操作失败') } }
const fetchUsers = async () => { try { const { data } = await request.get('/users', { params: { page: 1, page_size: 100 } }); userList.value = data.data.items } catch (e) { ElMessage.error('操作失败') } }

const selectDevice = async (d: Asset) => {
  selectedDevice.value = d
  // 查借还记录
  try { const { data } = await getBorrowHistory(d.id); borrowRecords.value = data.data.map((r: any) => ({ id: r.id, time: r.borrow_date || r.created_at, title: r.status === 'borrowed' ? '设备出借' : '设备归还', desc: `${r.borrower}${r.department ? ' (' + r.department + ')' : ''}${r.location ? ' @' + r.location : ''} ` + (r.status === 'borrowed' ? '借出' : '归还'), status: r.status, photo_url: r.photo_url, return_photo_url: r.return_photo_url })) } catch (e) { borrowRecords.value = [] }
  // 查变动记录
  try { const { data } = await getChangeHistory(d.id); changeRecords.value = data.data.map((r: any) => ({ id: r.id, time: r.created_at, title: r.change_type_label, desc: `${r.old_value || '无'} → ${r.new_value}`, change_type: r.change_type })) } catch (e) { changeRecords.value = [] }
}

const refreshDevice = async () => {
  await fetchDevices()
  if (selectedDevice.value) {
    const updated = devices.value.find(d => d.id === selectedDevice.value!.id)
    if (updated) await selectDevice(updated)
  }
}

const handleBorrow = () => { borrowVisible.value = true }
const onBorrowSuccess = () => { borrowVisible.value = false; refreshDevice() }

const handleReturn = () => { returnVisible.value = true }
const onReturnSuccess = () => { returnVisible.value = false; refreshDevice() }

const handleCancelBorrow = async () => {
  if (!selectedDevice.value) return
  const activeRecord = borrowRecords.value.find((r: any) => r.status === 'borrowed')
  if (!activeRecord) { ElMessage.warning('未找到进行中的出借记录'); return }
  try {
    await ElMessageBox.confirm(`确认取消设备【${selectedDevice.value.name}】的出借记录吗？`, '取消出借', { type: 'warning' })
    await cancelBorrow(activeRecord.id)
    ElMessage.success('出借已取消')
    refreshDevice()
  } catch (e: any) { if (e !== 'cancel' && e !== 'close') console.error(e) }
}

const handleChange = () => { changeVisible.value = true }
const onChangeSuccess = () => { changeVisible.value = false; refreshDevice() }

onMounted(async () => { await fetchCategories(); fetchUsers(); fetchDevices() })
</script>

<style scoped>
@media (max-width: 768px) {
  .el-col { margin-bottom: 12px; }
  .actions { flex-wrap: wrap; }
}
.group-title { display: flex; align-items: center; gap: 8px; width: 100% }
.group-count { font-size: 12px; color: #909399 }
.device-item { display: flex; align-items: center; gap: 12px; padding: 8px 12px; border-radius: 8px; cursor: pointer; transition: background .2s }
.device-item:hover { background: #f5f7fa }
.device-item.active { background: #ecf5ff; border-left: 3px solid #409eff }
.device-code { font-size: 13px; color: #909399; font-family: monospace }
.device-name { font-size: 14px; color: #303133; flex: 1 }
.card-header { display: flex; align-items: center; justify-content: space-between }
.actions { margin-top: 16px; display: flex; gap: 12px }
</style>
