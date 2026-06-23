<template>
  <div class="flow-management">
    <el-row :gutter="16">
      <!-- 左侧：设备列表 -->
      <el-col :xs="24" :sm="24" :md="14">
        <el-card>
          <template #header>
            <div style="display:flex;justify-content:space-between;align-items:center">
              <span>设备列表</span>
              <div v-if="isAdmin">
                <el-button v-if="!inventoryActive" type="warning" size="small" @click="startInventory">开始盘点</el-button>
                <template v-else>
                  <span style="margin-right:8px;font-size:13px;color:#e6a23c">盘点中</span>
                  <el-button type="success" size="small" @click="endInventory">结束盘点</el-button>
                </template>
              </div>
            </div>
          </template>
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
            <el-table-column label="盘点" width="200">
              <template #default="{ row }">
                <template v-if="inventoryActive">
                  <el-upload :show-file-list="false" :before-upload="(f:any)=>(uploadInvPhoto(row,f),false)" accept=".jpg,.jpeg,.png" style="display:inline-block;margin-right:2px">
                    <el-button link size="small">📷</el-button>
                  </el-upload>
                  <el-button link size="small" @click.stop="markChecked(row)">确认</el-button>
                  <el-button link size="small" type="danger" @click.stop="markAbnormal(row)">异常</el-button>
                </template>
                <span v-if="getInvStatus(row) === '已盘点'"><el-tag type="success" size="small">已盘点</el-tag></span>
                <span v-else-if="getInvStatus(row) === '异常'"><el-tag type="danger" size="small">异常</el-tag></span>
                <span v-else><el-tag type="info" size="small">未盘点</el-tag></span>
                <el-image v-if="getInvImage(row)" :src="getInvImage(row)" style="width:36px;height:36px;border-radius:4px;vertical-align:middle;margin-left:4px" fit="cover" :preview-src-list="[getInvImage(row)]" preview-teleported />
              </template>
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
        <el-card v-if="!selectedDevice">
          <template #header v-if="isAdmin && pendingList.length > 0"><span style="color:#e6a23c">待审批出借（{{ pendingList.length }}）</span></template>
          <template v-if="isAdmin && pendingList.length > 0">
            <div v-for="p in pendingList" :key="p.id" style="padding:10px 0;border-bottom:1px solid #f0f0f0">
              <div style="display:flex;justify-content:space-between;align-items:center">
                <div><strong>{{ p.asset_name }}</strong><span style="font-size:12px;color:#909399;margin-left:8px">{{ p.asset_code }}</span></div>
                <div><el-button size="small" type="success" @click="doApprove(p.id)">批准</el-button><el-button size="small" type="danger" @click="doReject(p.id)">拒绝</el-button></div>
              </div>
              <div style="font-size:12px;color:#909399;margin-top:4px">{{ p.borrower }}{{ p.department ? ' ('+p.department+')' : '' }}{{ p.location ? ' @'+p.location : '' }}</div>
            </div>
          </template>
          <div v-else style="text-align:center;color:#909399;padding:40px 0">
            <el-icon :size="48"><Connection /></el-icon>
            <p style="margin-top:16px">请从左侧选择设备</p>
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
              <el-button type="success" @click="handleReturn" :disabled="selectedDevice.status !== 'borrowed' || !canReturn">
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
                <el-timeline-item v-for="r in borrowRecords" :key="r.id" :timestamp="r.time" :color="r.status === 'borrowed' ? '#e6a23c' : r.status === 'pending' ? '#909399' : r.status === 'rejected' ? '#f56c6c' : '#67c23a'">
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
import { useUserStore } from '@/stores/user'
import { getAssets } from '@/api/asset'
import { cancelBorrow, getBorrowHistory, getPendingBorrows, approveBorrow, rejectBorrow } from '@/api/borrow'
import { getChangeHistory } from '@/api/change'
import request from '@/api/request'
import type { Asset, Category, User } from '@/types'
import BorrowDialog from '@/components/BorrowDialog.vue'
import ChangeDialog from '@/components/ChangeDialog.vue'
import ReturnDialog from '@/components/ReturnDialog.vue'

const userStore = useUserStore()
const isAdmin = computed(() => userStore.user?.role === 'admin' || userStore.user?.role === 'asset_admin')
const canReturn = computed(() => {
  if (isAdmin.value) return true
  const active = borrowRecords.value.find((r: any) => r.status === 'borrowed')
  return active && userStore.user?.real_name === (active as any)._borrower
})
const inventoryActive = ref(false)

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
const pendingList = ref<any[]>([])

const fetchPending = async () => {
  if (!isAdmin.value) return
  try { const { data } = await getPendingBorrows(); pendingList.value = data.data } catch (e) { }
}
const doApprove = async (id: number) => { await approveBorrow(id); ElMessage.success('已批准'); fetchPending(); fetchDevices() }
const doReject = async (id: number) => { await rejectBorrow(id); ElMessage.success('已拒绝'); fetchPending() }
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
  try { const { data } = await getBorrowHistory(d.id); borrowRecords.value = data.data.map((r: any) => {
  let title, desc, status = r.status
  if (r.status === 'borrowed') { title = '设备出借'; desc = `${r.borrower}${r.department ? ' (' + r.department + ')' : ''}${r.location ? ' @' + r.location : ''} 借出` }
  else if (r.status === 'pending') { title = '待审批'; desc = `${r.borrower} 申请出借，等待审批` }
  else if (r.status === 'rejected') { title = '已拒绝'; desc = `${r.borrower} 的出借申请被拒绝` }
  else { title = '设备归还'; desc = `${r.borrower} 归还设备` }
  if (r.remark) desc += ` | 备注: ${r.remark}`
  return { id: r.id, time: r.borrow_date || r.created_at, title, desc, status, photo_url: r.photo_url, return_photo_url: r.return_photo_url, _borrower: r.borrower }
}) } catch (e) { borrowRecords.value = [] }
  // 查变动记录
  try { const { data } = await getChangeHistory(d.id); changeRecords.value = data.data.map((r: any) => ({ id: r.id, time: r.created_at, title: r.change_type_label, desc: `${r.change_type === 'owner' ? (userList.value.find(u => String(u.id) === r.old_value)?.real_name || r.old_value || '无') : (r.old_value || '无')} → ${r.change_type === 'owner' ? (userList.value.find(u => String(u.id) === r.new_value)?.real_name || r.new_value) : r.new_value}` + (r.remark ? ` | 备注: ${r.remark}` : ''), change_type: r.change_type })) } catch (e) { changeRecords.value = [] }
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

// ========== 盘点 ==========
// 盘点：前端暂存修改，结束时批量提交
const inventoryChanges = ref<Map<number, { status: string; image: string | null }>>(new Map())
const getInvStatus = (row: any) => inventoryChanges.value.has(row.id) ? inventoryChanges.value.get(row.id)!.status : row.inventory_status || '未盘点'
const getInvImage = (row: any) => inventoryChanges.value.has(row.id) ? inventoryChanges.value.get(row.id)!.image : row.inventory_image

const startInventory = () => { inventoryActive.value = true; inventoryChanges.value = new Map() }
const endInventory = async () => {
  try {
    await ElMessageBox.confirm('本次盘点结果将保存，是否继续？', '结束盘点', { type: 'info' })
    const items: any[] = []
    inventoryChanges.value.forEach((v, id) => items.push({ id, inventory_status: v.status, inventory_image: v.image }))
    if (items.length > 0) await request.post('/assets/inventory/save', items)
    inventoryActive.value = false; inventoryChanges.value = new Map(); fetchDevices()
    ElMessage.success('盘点完成')
  } catch (e: any) { if (e !== 'cancel' && e !== 'close') console.error(e) }
}

const uploadInvPhoto = async (row: any, file: File) => {
  const fd = new FormData(); fd.append('file', file)
  const { data } = await request.post('/upload', fd)
  const cur = inventoryChanges.value.get(row.id) || { status: getInvStatus(row), image: getInvImage(row) }
  cur.image = data.data.url; inventoryChanges.value.set(row.id, cur)
  return false
}
const markChecked = async (row: any) => {
  try { await ElMessageBox.confirm(`确认设备【${row.name}】盘点正常？`, '盘点确认', { type: 'success' }); const cur = inventoryChanges.value.get(row.id) || { status: getInvStatus(row), image: getInvImage(row) }; cur.status = '已盘点'; inventoryChanges.value.set(row.id, cur); ElMessage.success('已标记为已盘点') } catch (e) { }
}
const markAbnormal = async (row: any) => {
  try { await ElMessageBox.confirm(`确认设备【${row.name}】为异常？`, '异常确认', { type: 'warning' }); const cur = inventoryChanges.value.get(row.id) || { status: getInvStatus(row), image: getInvImage(row) }; cur.status = '异常'; inventoryChanges.value.set(row.id, cur); ElMessage.success('已标记为异常') } catch (e) { }
}
const onChangeSuccess = () => { changeVisible.value = false; refreshDevice() }

onMounted(async () => { await fetchCategories(); fetchUsers(); fetchDevices(); fetchPending() })
</script>

<style scoped>
@media (max-width: 768px) {
  .el-col { margin-bottom: 12px; }
  .actions { flex-wrap: wrap; }
:deep(.el-image-viewer__wrapper) { z-index: 9999 !important; }
:deep(.el-image-viewer__mask) { z-index: 9998 !important; }
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