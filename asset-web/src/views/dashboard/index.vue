<template>
  <div class="dashboard">
    <!-- 统计卡片 -->
    <el-row :gutter="20">
      <el-col :xs="12" :sm="12" :md="6">
        <el-card class="stat-card"><div class="stat-content"><div class="stat-icon" style="background: #409eff"><el-icon :size="30"><Box /></el-icon></div><div class="stat-info"><div class="stat-value">{{ stats.total || 0 }}</div><div class="stat-label">资产总数</div></div></div></el-card>
      </el-col>
      <el-col :xs="12" :sm="12" :md="6">
        <el-card class="stat-card"><div class="stat-content"><div class="stat-icon" style="background: #67c23a"><el-icon :size="30"><CircleCheck /></el-icon></div><div class="stat-info"><div class="stat-value">{{ stats.by_status?.normal || 0 }}</div><div class="stat-label">在库</div></div></div></el-card>
      </el-col>
      <el-col :xs="12" :sm="12" :md="6">
        <el-card class="stat-card"><div class="stat-content"><div class="stat-icon" style="background: #e6a23c"><el-icon :size="30"><Switch /></el-icon></div><div class="stat-info"><div class="stat-value">{{ stats.by_status?.borrowed || 0 }}</div><div class="stat-label">已借出</div></div></div></el-card>
      </el-col>
      <el-col :xs="12" :sm="12" :md="6">
        <el-card class="stat-card"><div class="stat-content"><div class="stat-icon" style="background: #f56c6c"><el-icon :size="30"><CircleClose /></el-icon></div><div class="stat-info"><div class="stat-value">{{ stats.by_status?.scrapped || 0 }}</div><div class="stat-label">已报废</div></div></div></el-card>
      </el-col>
    </el-row>

    <!-- 逾期提醒 -->
    <el-row v-if="overdueList.length > 0" style="margin-top: 20px">
      <el-col :span="24">
        <el-card style="border-left: 4px solid #f56c6c">
          <template #header><span style="color:#f56c6c;font-weight:bold">⚠️ 逾期未归还提醒（{{ overdueList.length }}）</span></template>
          <el-table :data="overdueList" size="small" border stripe>
            <el-table-column prop="asset_name" label="设备名称" />
            <el-table-column prop="asset_code" label="资产编号" width="150" />
            <el-table-column prop="borrower" label="借用人" width="100" />
            <el-table-column prop="borrow_date" label="借出日期" width="120" />
            <el-table-column label="预计归还" width="120"><template #default="{ row }"><span style="color:#f56c6c;font-weight:bold">{{ row.expected_return_date }}</span></template></el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <!-- 资产状态分布 -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>资产状态分布</span>
          </template>
          <div class="status-bars">
            <div class="status-item">
              <div class="status-label">
                <span>在库</span>
                <span class="status-count">{{ stats.by_status?.normal || 0 }}</span>
              </div>
              <el-progress
                :percentage="getPercent(stats.by_status?.normal)"
                :color="'#67c23a'"
                :stroke-width="18"
                :show-text="false"
              />
            </div>
            <div class="status-item">
              <div class="status-label">
                <span>已借出</span>
                <span class="status-count">{{ stats.by_status?.borrowed || 0 }}</span>
              </div>
              <el-progress
                :percentage="getPercent(stats.by_status?.borrowed)"
                :color="'#e6a23c'"
                :stroke-width="18"
                :show-text="false"
              />
            </div>
            <div class="status-item">
              <div class="status-label">
                <span>已报废</span>
                <span class="status-count">{{ stats.by_status?.scrapped || 0 }}</span>
              </div>
              <el-progress
                :percentage="getPercent(stats.by_status?.scrapped)"
                :color="'#f56c6c'"
                :stroke-width="18"
                :show-text="false"
              />
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 近期操作记录 -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>近期操作记录</span>
          </template>
          <div class="recent-activities" v-if="activities.length > 0">
            <div v-for="(item, i) in activities" :key="i" class="activity-item">
              <div class="activity-dot" :style="{ background: getActivityColor(item.title) }"></div>
              <div class="activity-body">
                <div class="activity-title">
                  <el-tag size="small" :type="getActivityTag(item.title)">{{ item.title }}</el-tag>
                  <span class="activity-asset">{{ item.asset_name }}</span>
                </div>
                <div class="activity-desc">{{ item.description }}</div>
                <div class="activity-meta">
                  <span>{{ item.operator }}</span>
                  <span>{{ item.time?.slice(0, 16) }}</span>
                </div>
              </div>
            </div>
          </div>
          <p v-else class="empty-text">暂无操作记录</p>
        </el-card>
      </el-col>
    </el-row>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import request from '@/api/request'

const stats = ref<any>({ total: 0, by_status: {} })
const activities = ref<any[]>([])
const overdueList = ref<any[]>([])

const getPercent = (val: number | undefined) => {
  const total = stats.value.total || 1
  return Math.round(((val || 0) / total) * 100)
}

const getActivityTag = (title: string) => {
  if (title.includes('入库') || title.includes('归还') || title.includes('维修')) return 'success'
  if (title.includes('出借') || title.includes('领用')) return 'warning'
  if (title.includes('报废')) return 'danger'
  if (title.includes('负责人')) return ''
  if (title.includes('变更')) return 'info'
  return ''
}

const getActivityColor = (title: string) => {
  if (title.includes('入库') || title.includes('归还')) return '#67c23a'
  if (title.includes('出借') || title.includes('领用')) return '#e6a23c'
  if (title.includes('报废')) return '#f56c6c'
  if (title.includes('负责人')) return '#9b59b6'
  if (title.includes('变更')) return '#909399'
  return '#409eff'
}

onMounted(async () => {
  try {
    const { data } = await request.get('/reports/asset-stats')
    stats.value = data.data
  } catch (error) {
    console.error('获取统计数据失败', error)
  }

  try {
    const { data } = await request.get('/reports/overdue')
    overdueList.value = data.data
  } catch (e) { /* */ }

  try {
    const { data } = await request.get('/reports/recent-activities', { params: { limit: 10 } })
    activities.value = data.data
  } catch (error) {
    console.error('获取最近活动失败', error)
  }
})
</script>

<style scoped>
.stat-card {
  cursor: pointer;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

.status-bars {
  padding: 10px 0;
}

.status-item {
  margin-bottom: 20px;
}

.status-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
  font-size: 14px;
  color: #606266;
}

.status-count {
  font-weight: bold;
  color: #303133;
}

.recent-activities {
  max-height: 350px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-top: 6px;
  flex-shrink: 0;
}

.activity-body {
  flex: 1;
}

.activity-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.activity-asset {
  font-weight: 500;
  color: #303133;
}

.activity-desc {
  font-size: 13px;
  color: #606266;
  margin-bottom: 2px;
}

.activity-meta {
  font-size: 12px;
  color: #c0c4cc;
  display: flex;
  gap: 12px;
}

.empty-text {
  text-align: center;
  color: #909399;
  padding: 40px 0;
}

.chart-placeholder {
  min-height: 150px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #909399;
}

.chart-placeholder ul {
  list-style: none;
  padding: 0;
}

.chart-placeholder li {
  padding: 5px 0;
}
</style>