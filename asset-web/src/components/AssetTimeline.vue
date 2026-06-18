<template>
  <div>
    <el-timeline v-if="events.length > 0">
      <el-timeline-item
        v-for="event in events"
        :key="event.id"
        :timestamp="event.time"
        placement="top"
        :color="event.color"
      >
        <el-card shadow="hover">
          <strong>{{ event.title }}</strong>
          <p style="margin: 4px 0; color: #606266">{{ event.description }}</p>
          <span style="font-size: 12px; color: #909399">{{ event.detail }}</span>
          <div v-if="event.photo" style="margin-top: 6px">
            <el-image :src="event.photo" style="width:80px;height:80px;border-radius:6px" fit="cover" :preview-src-list="[event.photo]" />
          </div>
        </el-card>
      </el-timeline-item>
    </el-timeline>
    <p v-else style="color: #909399; text-align: center; padding: 20px">暂无操作记录</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getAssetRecords } from '@/api/asset'
import { getBorrowHistory } from '@/api/borrow'
import { getChangeHistory } from '@/api/change'
import request from '@/api/request'

const props = defineProps<{
  assetId: number
}>()

interface TimelineEvent {
  id: string
  time: string
  title: string
  description: string
  detail: string
  color: string
  photo?: string | null
}

const events = ref<TimelineEvent[]>([])

const STATUS_LABELS: Record<string, string> = {
  normal: '在库',
  borrowed: '已借出',
  scrapped: '已报废',
}

const fetchTimeline = async () => {
  const list: TimelineEvent[] = []

  // 1. 操作记录
  try {
    const { data } = await getAssetRecords(props.assetId, { page: 1, page_size: 50 })
    for (const r of data.data.items) {
      list.push({
        id: `record-${r.id}`,
        time: r.created_at,
        title: r.type_name,
        description: r.description || '',
        detail: `操作人: ${r.operator}`,
        color: '#409eff',
      })
    }
  } catch (e) { /* ignore */ }

  // 2. 出借记录
  try {
    const { data } = await getBorrowHistory(props.assetId)
    for (const r of data.data) {
      const deptInfo = r.department ? ` (${r.department})` : ''
      const locInfo = r.location ? ` @${r.location}` : ''
      if (r.status === 'borrowed') {
        list.push({
          id: `borrow-${r.id}`,
          time: r.borrow_date || r.created_at,
          title: '设备出借',
          description: `${r.borrower}${deptInfo}${locInfo} 借出设备`,
          detail: [
            r.borrow_date ? `借出日期: ${r.borrow_date}` : '',
            r.expected_return_date ? `预计归还: ${r.expected_return_date}` : '',
          ].filter(Boolean).join(' | '),
          color: '#e6a23c',
          photo: r.photo_url || null,
        })
      } else {
        list.push({
          id: `return-${r.id}`,
          time: r.actual_return_date || r.created_at,
          title: '归还设备',
          description: `${r.borrower}${deptInfo}${locInfo} 归还设备`,
          detail: [
            r.borrow_date ? `借出日期: ${r.borrow_date}` : '',
            r.actual_return_date ? `实际归还: ${r.actual_return_date}` : '',
          ].filter(Boolean).join(' | '),
          color: '#67c23a',
          photo: r.return_photo_url || r.photo_url || null,
        })
      }
    }
  } catch (e) { /* ignore */ }

  // 3. 变动记录（含用户姓名映射）
  let userMap: Record<number, string> = {}
  try {
    const { data } = await request.get('/users', { params: { page: 1, page_size: 100 } })
    for (const u of data.data.items) userMap[u.id] = u.real_name
  } catch (e) { /* ignore */ }

  try {
    const { data } = await getChangeHistory(props.assetId)

    const formatVal = (type: string, val: string | null) => {
      if (!val) return '无'
      if (type === 'owner') return userMap[Number(val)] || val
      return val
    }

    for (const r of data.data) {
      list.push({
        id: `change-${r.id}`,
        time: r.created_at,
        title: r.change_type_label,
        description: `${formatVal(r.change_type, r.old_value)} → ${formatVal(r.change_type, r.new_value)}`,
        detail: `操作人: ${r.operator}` + (r.remark ? ` | 备注: ${r.remark}` : ''),
        color: r.change_type === 'owner' ? '#9b59b6' : '#909399',
      })
    }
  } catch (e) { /* ignore */ }

  list.sort((a, b) => new Date(b.time).getTime() - new Date(a.time).getTime())
  events.value = list
}

onMounted(() => {
  fetchTimeline()
})
</script>
