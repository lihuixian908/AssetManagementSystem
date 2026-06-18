<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    title="设备变动"
    width="480px"
    @closed="resetForm"
  >
    <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
      <el-form-item label="设备名称">
        <span>{{ asset?.name }}</span>
      </el-form-item>
      <el-form-item label="资产编号">
        <span>{{ asset?.asset_code }}</span>
      </el-form-item>
      <el-form-item label="变动类型" prop="change_type">
        <el-select v-model="form.change_type" placeholder="请选择变动类型" style="width: 100%">
          <el-option label="负责人变更" value="owner" />
          <el-option label="部门变更" value="dept" />
          <el-option label="位置变更" value="location" />
          <el-option label="分类变更" value="category" />
        </el-select>
      </el-form-item>
      <el-form-item label="当前值" v-if="form.change_type">
        <span>{{ currentValue }}</span>
      </el-form-item>
      <el-form-item label="新值" prop="new_value">
        <el-select
          v-if="form.change_type === 'owner'"
          v-model="form.new_value"
          placeholder="请选择新负责人"
          style="width: 100%"
        >
          <el-option
            v-for="u in users"
            :key="u.id"
            :label="u.real_name"
            :value="String(u.id)"
          />
        </el-select>
        <el-select
          v-else-if="form.change_type === 'category'"
          v-model="form.new_value"
          placeholder="请选择新分类"
          style="width: 100%"
        >
          <el-option
            v-for="cat in categories"
            :key="cat.id"
            :label="cat.name"
            :value="String(cat.id)"
          />
        </el-select>
        <el-input
          v-else
          v-model="form.new_value"
          placeholder="请输入新值"
        />
      </el-form-item>
      <el-form-item label="备注">
        <el-input v-model="form.remark" type="textarea" :rows="2" placeholder="备注信息" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="$emit('update:modelValue', false)">取消</el-button>
      <el-button type="primary" @click="handleSubmit" :loading="submitting">确认变动</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { createChange } from '@/api/change'
import type { Asset, Category, User } from '@/types'

const props = defineProps<{
  modelValue: boolean
  asset: Asset | null
  categories: Category[]
  users: User[]
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  success: []
}>()

const formRef = ref<FormInstance>()
const submitting = ref(false)

const form = reactive({
  change_type: '' as string,
  new_value: '',
  remark: '',
})

const rules: FormRules = {
  change_type: [{ required: true, message: '请选择变动类型', trigger: 'change' }],
  new_value: [{ required: true, message: '请输入新值', trigger: 'blur' }],
}

const CHANGE_LABEL: Record<string, string> = {
  owner: '负责人',
  dept: '部门',
  location: '位置',
  category: '分类',
}

const currentValue = computed(() => {
  if (!props.asset || !form.change_type) return ''
  const type = form.change_type
  if (type === 'owner') return props.asset.owner_name || (props.asset.user_id ? String(props.asset.user_id) : '无')
  if (type === 'dept') return props.asset.department || '无'
  if (type === 'location') return props.asset.location || '无'
  if (type === 'category') {
    const cat = props.categories.find(c => c.id === props.asset?.category_id)
    return cat ? cat.name : String(props.asset.category_id)
  }
  return ''
})

const resetForm = () => {
  form.change_type = ''
  form.new_value = ''
  form.remark = ''
  formRef.value?.resetFields()
}

const handleSubmit = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid || !props.asset) return

  submitting.value = true
  try {
    await createChange({
      asset_id: props.asset.id,
      change_type: form.change_type,
      new_value: form.new_value,
      remark: form.remark || undefined,
    })
    ElMessage.success('变动成功')
    emit('update:modelValue', false)
    emit('success')
  } catch (error) {
    console.error('变动失败', error)
  } finally {
    submitting.value = false
  }
}
</script>
