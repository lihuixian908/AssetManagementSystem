<template>
  <div class="catalog-page">
    <!-- 搜索区 -->
    <el-card>
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="关键词">
          <el-input v-model="searchForm.keyword" placeholder="设备名称/资产编号" clearable style="width: 240px" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择" clearable style="width: 140px">
            <el-option label="在库" value="normal" />
            <el-option label="已借出" value="borrowed" />
            <el-option label="已报废" value="scrapped" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button type="success" @click="handleAdd">
            <el-icon><Plus /></el-icon> 新增设备
          </el-button>
          <el-button type="info" @click="handleExport">
            <el-icon><Download /></el-icon> Excel导出
          </el-button>
          <el-button type="warning" @click="handleDownloadTemplate">
            <el-icon><Document /></el-icon> 下载模板
          </el-button>
          <el-upload :show-file-list="false" :before-upload="handleUpload" accept=".xlsx,.xls" style="display:inline-block;margin-left:8px">
            <el-button type="success"><el-icon><Upload /></el-icon> Excel导入</el-button>
          </el-upload>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 分类标签 + 状态筛选 -->
    <el-card style="margin-top: 16px">
      <div class="filter-row">
        <span class="filter-label">分类：</span>
        <el-button :type="activeCategory === null ? 'primary' : 'default'" size="small" @click="filterByCategory(null)">全部</el-button>
        <el-button v-for="cat in categories" :key="cat.id" :type="activeCategory === cat.id ? 'primary' : 'default'" size="small" @click="filterByCategory(cat.id)">{{ cat.name }}</el-button>
      </div>
      <div class="filter-row" style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #f0f0f0">
        <span class="filter-label">状态：</span>
        <el-button :type="searchForm.status === '' ? 'primary' : 'default'" size="small" @click="filterByStatus('')">全部状态</el-button>
        <el-button :type="searchForm.status === 'normal' ? 'success' : 'default'" size="small" @click="filterByStatus('normal')">在库</el-button>
        <el-button :type="searchForm.status === 'borrowed' ? 'warning' : 'default'" size="small" @click="filterByStatus('borrowed')">已借出</el-button>
        <el-button :type="searchForm.status === 'scrapped' ? 'danger' : 'default'" size="small" @click="filterByStatus('scrapped')">已报废</el-button>
      </div>
    </el-card>

    <!-- 设备表格（PC/平板） -->
    <el-card style="margin-top: 16px" v-if="!isMobile">
      <div style="margin-bottom: 8px" v-if="selectedIds.length > 0">
        <el-button type="danger" @click="handleBatchDelete">批量删除（{{ selectedIds.length }}）</el-button>
      </div>
      <el-table :data="devices" v-loading="loading" border stripe @selection-change="onSelectionChange">
        <el-table-column type="selection" width="45" />
        <el-table-column prop="asset_code" label="资产编号" width="150" />
        <el-table-column label="公司编号" width="130"><template #default="{ row }">{{ row.company_code || '-' }}</template></el-table-column>
        <el-table-column label="SN号" width="130"><template #default="{ row }">{{ row.sn || '-' }}</template></el-table-column>
        <el-table-column prop="name" label="设备名称" min-width="160" />
        <el-table-column label="分类" width="120"><template #default="{ row }">{{ getCategoryName(row.category_id) }}</template></el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="负责人" width="100"><template #default="{ row }">{{ row.owner_name || row.user_id || '-' }}</template></el-table-column>
        <el-table-column prop="location" label="存放位置" width="130"><template #default="{ row }">{{ row.location || '-' }}</template></el-table-column>
        <el-table-column label="二维码" width="90" align="center">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="showQr(row)">查看</el-button>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="240" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleView(row)">查看</el-button>
            <el-button link type="success" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="danger" @click="handleScrap(row)" v-if="row.status !== 'scrapped'">报废</el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        v-model:current-page="pagination.page" v-model:page-size="pagination.page_size" :total="pagination.total"
        :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper"
        @current-change="fetchDevices" @size-change="fetchDevices" style="margin-top: 20px; justify-content: flex-end" />
    </el-card>

    <!-- 设备卡片（手机） -->
    <div v-else v-loading="loading" style="margin-top: 12px">
      <el-card v-for="d in devices" :key="d.id" style="margin-bottom: 10px">
        <div style="display: flex; justify-content: space-between; align-items: center">
          <strong>{{ d.name }}</strong>
          <el-tag :type="getStatusType(d.status)" size="small">{{ getStatusLabel(d.status) }}</el-tag>
        </div>
        <div style="margin-top: 6px; font-size: 13px; color: #606266">
          <p style="margin: 2px 0">编号: {{ d.asset_code }} | SN: {{ d.sn || '-' }}</p>
          <p style="margin: 2px 0">分类: {{ getCategoryName(d.category_id) }} | {{ d.owner_name || d.user_id || '无负责人' }}</p>
        </div>
        <div style="margin-top: 8px; display: flex; gap: 8px">
          <el-button size="small" @click="handleView(d)">查看</el-button>
          <el-button size="small" type="success" @click="handleEdit(d)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleScrap(d)" v-if="d.status !== 'scrapped'">报废</el-button>
        </div>
      </el-card>
      <el-pagination v-model:current-page="pagination.page" :total="pagination.total" :page-size="pagination.page_size" layout="prev, pager, next" @current-change="fetchDevices" size="small" style="justify-content: center; margin-top: 8px" />
    </div>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑设备' : '新增设备'" :width="isMobile ? '95%' : '750px'" @closed="resetForm">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="90px">
        <el-row :gutter="16">
          <el-col :xs="24" :md="12"><el-form-item label="资产编号" prop="asset_code"><el-input v-model="form.asset_code" /></el-form-item></el-col>
          <el-col :xs="24" :md="12"><el-form-item label="设备名称" prop="name"><el-input v-model="form.name" /></el-form-item></el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :xs="24" :md="12"><el-form-item label="公司编号"><el-input v-model="form.company_code" /></el-form-item></el-col>
          <el-col :xs="24" :md="12"><el-form-item label="SN号"><el-input v-model="form.sn" /></el-form-item></el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :xs="24" :md="12">
            <el-form-item label="分类"><el-select v-model="form.category_id" style="width: 100%"><el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" /></el-select></el-form-item>
          </el-col>
          <el-col :xs="24" :md="12">
            <el-form-item label="状态"><el-select v-model="form.status" style="width: 100%"><el-option label="在库" value="normal" /><el-option label="已借出" value="borrowed" /><el-option label="已报废" value="scrapped" /></el-select></el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :xs="24" :md="12"><el-form-item label="所属部门"><el-input v-model="form.department" /></el-form-item></el-col>
          <el-col :xs="24" :md="12"><el-form-item label="负责人"><el-select v-model="form.user_id" clearable style="width: 100%"><el-option v-for="u in userList" :key="u.id" :label="u.real_name" :value="u.id" /></el-select></el-form-item></el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :xs="24" :md="12"><el-form-item label="存放位置"><el-input v-model="form.location" /></el-form-item></el-col>
          <el-col :xs="24" :md="12"><el-form-item label="采购日期"><el-date-picker v-model="form.purchase_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" /></el-form-item></el-col>
        </el-row>
        <el-form-item label="备注"><el-input v-model="form.description" type="textarea" :rows="3" /></el-form-item>
      </el-form>
      <template #footer><el-button @click="dialogVisible = false">取消</el-button><el-button type="primary" @click="handleSubmit" :loading="submitting">提交</el-button></template>
    </el-dialog>

    <!-- 查看详情弹窗 -->
    <el-dialog v-model="detailVisible" title="设备详情" :width="isMobile ? '95%' : '700px'">
      <template v-if="currentDevice">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="资产编号">{{ currentDevice.asset_code }}</el-descriptions-item>
          <el-descriptions-item label="设备名称">{{ currentDevice.name }}</el-descriptions-item>
          <el-descriptions-item label="公司编号">{{ currentDevice.company_code || '-' }}</el-descriptions-item>
          <el-descriptions-item label="SN号">{{ currentDevice.sn || '-' }}</el-descriptions-item>
          <el-descriptions-item label="分类">{{ getCategoryName(currentDevice.category_id) }}</el-descriptions-item>
          <el-descriptions-item label="状态"><el-tag :type="getStatusType(currentDevice.status)">{{ getStatusLabel(currentDevice.status) }}</el-tag></el-descriptions-item>
          <el-descriptions-item label="所属部门">{{ currentDevice.department || '-' }}</el-descriptions-item>
          <el-descriptions-item label="负责人">{{ currentDevice.owner_name || currentDevice.user_id || '-' }}</el-descriptions-item>
          <el-descriptions-item label="存放位置">{{ currentDevice.location || '-' }}</el-descriptions-item>
          <el-descriptions-item label="采购日期">{{ currentDevice.purchase_date || '-' }}</el-descriptions-item>
          <el-descriptions-item label="备注" :span="2">{{ currentDevice.description || '-' }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ currentDevice.created_at }}</el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ currentDevice.updated_at }}</el-descriptions-item>
        </el-descriptions>
        <el-divider />
        <h4>操作记录</h4>
        <AssetTimeline :asset-id="currentDevice.id" />
      </template>
    </el-dialog>

    <!-- 二维码弹窗 -->
    <el-dialog v-model="qrVisible" title="设备二维码" width="360px" align-center>
      <div style="text-align: center">
        <el-image :src="qrUrl" style="width: 260px; height: 260px" fit="contain" />
        <p style="margin-top: 10px; color: #606266">{{ qrAsset?.name }} ({{ qrAsset?.asset_code }})</p>
        <el-button type="primary" size="small" @click="downloadQr">下载二维码</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { getAssets, getAsset, createAsset, updateAsset, deleteAsset, scrapAsset } from '@/api/asset'
import request from '@/api/request'
import type { Asset, Category, User } from '@/types'
import AssetTimeline from '@/components/AssetTimeline.vue'

const isMobile = ref(window.innerWidth < 768)
window.addEventListener('resize', () => { isMobile.value = window.innerWidth < 768 })

const selectedIds = ref<number[]>([])
const onSelectionChange = (rows: any[]) => { selectedIds.value = rows.map(r => r.id) }
const handleBatchDelete = async () => {
  try {
    await ElMessageBox.confirm(`确认删除选中的 ${selectedIds.value.length} 台设备吗？`, '批量删除', { type: 'warning' })
    await request.post('/assets/batch-delete', selectedIds.value)
    ElMessage.success('批量删除成功')
    selectedIds.value = []
    fetchDevices()
  } catch (e: any) { if (e !== 'cancel' && e !== 'close') console.error(e) }
}

const categories = ref<Category[]>([])
const userList = ref<User[]>([])
const devices = ref<Asset[]>([])
const loading = ref(false)
const pagination = reactive({ page: 1, page_size: 10, total: 0 })
const activeCategory = ref<number | null>(null)

const searchForm = reactive({ keyword: '', status: '' })

const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref<number | null>(null)
const submitting = ref(false)
const formRef = ref<FormInstance>()
const form = reactive({ asset_code: '', company_code: '', sn: '', name: '', category_id: 1, status: 'normal', department: '', user_id: null as number | null, location: '', purchase_date: '', description: '' })

const rules: FormRules = {
  asset_code: [{ required: true, message: '请输入资产编号', trigger: 'blur' }],
  name: [{ required: true, message: '请输入设备名称', trigger: 'blur' }],
}

const detailVisible = ref(false)
const currentDevice = ref<Asset | null>(null)

const getCategoryName = (id: number) => { const c = categories.value.find(x => x.id === id); return c?.name || String(id) }
const getStatusType = (s: string) => ({ normal: 'success', borrowed: 'warning', scrapped: 'danger' } as any)[s] || 'info'
const getStatusLabel = (s: string) => ({ normal: '在库', borrowed: '已借出', scrapped: '已报废' } as any)[s] || s

const fetchCategories = async () => { try { const { data } = await request.get('/categories', { params: { page: 1, page_size: 100 } }); categories.value = data.data.items } catch (e) { ElMessage.error('操作失败') } }
const fetchUsers = async () => { try { const { data } = await request.get('/users', { params: { page: 1, page_size: 100 } }); userList.value = data.data.items } catch (e) { ElMessage.error('操作失败') } }

const fetchDevices = async () => {
  loading.value = true
  try {
    const p: any = { page: pagination.page, page_size: pagination.page_size }
    if (searchForm.keyword) p.keyword = searchForm.keyword
    if (searchForm.status) p.status_filter = searchForm.status
    if (activeCategory.value !== null) p.category_id = activeCategory.value
    const { data } = await getAssets(p)
    devices.value = data.data.items; pagination.total = data.data.total
  } catch (e) { ElMessage.error('操作失败') } finally { loading.value = false }
}

const handleSearch = () => { pagination.page = 1; fetchDevices() }
const handleReset = () => { searchForm.keyword = ''; searchForm.status = ''; activeCategory.value = null; pagination.page = 1; fetchDevices() }
const filterByCategory = (id: number | null) => { activeCategory.value = id; pagination.page = 1; fetchDevices() }
const filterByStatus = (s: string) => { searchForm.status = s; pagination.page = 1; fetchDevices() }

const resetForm = () => { form.asset_code = ''; form.company_code = ''; form.sn = ''; form.name = ''; form.category_id = 1; form.status = 'normal'; form.department = ''; form.user_id = null; form.location = ''; form.purchase_date = ''; form.description = ''; isEdit.value = false; editId.value = null; formRef.value?.resetFields() }
const handleAdd = () => { resetForm(); dialogVisible.value = true }
const handleEdit = (row: Asset) => { resetForm(); isEdit.value = true; editId.value = row.id; form.asset_code = row.asset_code; form.company_code = row.company_code || ''; form.sn = row.sn || ''; form.name = row.name; form.category_id = row.category_id; form.status = row.status; form.department = row.department || ''; form.user_id = row.user_id; form.location = row.location || ''; form.purchase_date = row.purchase_date || ''; form.description = row.description || ''; dialogVisible.value = true }

const handleSubmit = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  submitting.value = true
  try {
    const payload: any = { asset_code: form.asset_code, name: form.name, category_id: form.category_id, status: form.status, department: form.department || undefined, user_id: form.user_id, location: form.location || undefined, purchase_date: form.purchase_date || undefined, description: form.description || undefined, company_code: form.company_code || undefined, sn: form.sn || undefined }
    if (isEdit.value && editId.value) { await updateAsset(editId.value, payload); ElMessage.success('编辑成功') }
    else { await createAsset(payload); ElMessage.success('新增成功') }
    dialogVisible.value = false; fetchDevices()
  } catch (e) { ElMessage.error('操作失败') } finally { submitting.value = false }
}

const handleDelete = async (row: Asset) => {
  try { await ElMessageBox.confirm(`确认删除设备【${row.name}】吗？`, '提示', { type: 'warning' }); await deleteAsset(row.id); ElMessage.success('删除成功'); fetchDevices() } catch (e: any) { if (e !== 'cancel' && e !== 'close') console.error(e) }
}

const handleScrap = async (row: Asset) => {
  try { await ElMessageBox.confirm(`确认报废设备【${row.name}】吗？`, '报废确认', { type: 'warning' }); await scrapAsset(row.id, '设备报废'); ElMessage.success('报废成功'); fetchDevices() } catch (e: any) { if (e !== 'cancel' && e !== 'close') console.error(e) }
}

const handleView = async (row: Asset) => { detailVisible.value = true; try { const { data } = await getAsset(row.id); currentDevice.value = data.data } catch (e) { ElMessage.error('操作失败') } }

const handleExport = async () => {
  try {
    const { data } = await request.get('/assets/export', { responseType: 'blob' })
    const url = URL.createObjectURL(data)
    const a = document.createElement('a'); a.href = url; a.download = '资产列表.xlsx'; a.click()
    URL.revokeObjectURL(url); ElMessage.success('导出成功')
  } catch (e) { ElMessage.error('操作失败') }
}

const handleDownloadTemplate = () => {
  request.get('/assets/export', { responseType: 'blob' }).then(({ data }: any) => {
    const url = URL.createObjectURL(data)
    const a = document.createElement('a'); a.href = url; a.download = '资产导入模板.xlsx'; a.click()
    URL.revokeObjectURL(url)
  })
}

const handleUpload = async (file: File) => {
  try {
    const fd = new FormData()
    fd.append('file', file)
    await request.post('/assets/import', fd)
    ElMessage.success('导入成功')
    await fetchCategories()
    fetchDevices()
  } catch (e) { ElMessage.error('操作失败') }
  return false
}

// ========== 二维码 ==========
const qrVisible = ref(false)
const qrAsset = ref<Asset | null>(null)
const qrUrl = ref('')

const showQr = (row: Asset) => {
  qrAsset.value = row
  qrUrl.value = `/api/v1/qrcode/${row.id}`
  qrVisible.value = true
}

const downloadQr = () => {
  if (!qrAsset.value) return
  const link = document.createElement('a')
  link.href = qrUrl.value
  link.download = `QR_${qrAsset.value.asset_code}.png`
  link.click()
}

onMounted(async () => { await fetchCategories(); fetchUsers(); fetchDevices() })
</script>

<style scoped>
.filter-row { display: flex; align-items: center; gap: 8px; flex-wrap: wrap }
.filter-label { font-size: 13px; color: #909399; margin-right: 4px }
</style>
