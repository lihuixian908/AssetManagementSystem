<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    title="设备出借"
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
      <el-form-item label="借用人" prop="borrower">
        <el-select v-model="form.borrower" placeholder="请选择借用人" filterable style="width: 100%" @change="onBorrowerChange">
          <el-option v-for="u in users" :key="u.id" :label="u.real_name" :value="u.real_name" />
        </el-select>
      </el-form-item>
      <el-form-item label="所属部门">
        <el-input v-model="form.department" placeholder="自动填入或手动输入" />
      </el-form-item>
      <el-form-item label="使用地点" prop="location">
        <el-input v-model="form.location" placeholder="请输入设备使用地点" />
      </el-form-item>
      <el-form-item label="借出日期" prop="borrow_date">
        <el-date-picker v-model="form.borrow_date" type="date" placeholder="选择借出日期" value-format="YYYY-MM-DD" style="width: 100%" />
      </el-form-item>
      <el-form-item label="预计归还日期">
        <el-date-picker v-model="form.expected_return_date" type="date" placeholder="选择预计归还日期" value-format="YYYY-MM-DD" style="width: 100%" />
      </el-form-item>
      <el-form-item label="设备照片" prop="photo">
        <el-upload
          ref="uploadRef"
          :auto-upload="false"
          :limit="1"
          :on-change="onPhotoChange"
          :on-remove="onPhotoRemove"
          :before-upload="() => false"
          accept=".jpg,.jpeg,.png"
          list-type="picture"
        >
          <el-button type="primary" link><el-icon><Upload /></el-icon> 选择照片 (JPG/PNG)</el-button>
        </el-upload>
      </el-form-item>
      <el-form-item label="备注">
        <el-input v-model="form.remark" type="textarea" :rows="2" placeholder="备注信息" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="$emit('update:modelValue', false)">取消</el-button>
      <el-button type="primary" @click="handleSubmit" :loading="submitting">确认出借</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules, UploadInstance, UploadFile } from 'element-plus'
import { createBorrow } from '@/api/borrow'
import request from '@/api/request'
import type { Asset, User } from '@/types'

const props = defineProps<{
  modelValue: boolean
  asset: Asset | null
  users: User[]
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  success: []
}>()

const formRef = ref<FormInstance>()
const uploadRef = ref<UploadInstance>()
const submitting = ref(false)
const photoFile = ref<File | null>(null)

const form = reactive({
  borrower: '',
  department: '',
  location: '',
  borrow_date: '',
  expected_return_date: '',
  remark: '',
})

const rules: FormRules = {
  borrower: [{ required: true, message: '请选择借用人', trigger: 'change' }],
  location: [{ required: true, message: '请输入使用地点', trigger: 'blur' }],
  borrow_date: [{ required: true, message: '请选择借出日期', trigger: 'change' }],
  expected_return_date: [{
    validator: (_rule, value, callback) => {
      if (value && form.borrow_date && value < form.borrow_date) {
        callback(new Error('归还日期不能早于出借日期'))
      } else {
        callback()
      }
    },
    trigger: 'change',
  }],
}

const onBorrowerChange = (name: string) => {
  const user = props.users.find(u => u.real_name === name)
  if (user && user.department) {
    form.department = user.department
  }
}

const onPhotoChange = (file: UploadFile) => { photoFile.value = file.raw || null }
const onPhotoRemove = () => { photoFile.value = null }

const resetForm = () => {
  form.borrower = ''
  form.department = ''
  form.location = ''
  form.borrow_date = ''
  form.expected_return_date = ''
  form.remark = ''
  photoFile.value = null
  uploadRef.value?.clearFiles()
  formRef.value?.resetFields()
}

const handleSubmit = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid || !props.asset) return

  submitting.value = true
  try {
    let photo_url = undefined
    if (photoFile.value) {
      const fd = new FormData()
      fd.append('file', photoFile.value)
      const { data } = await request.post('/upload', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
      photo_url = data.data.url
    }

    await createBorrow({
      asset_id: props.asset.id,
      borrower: form.borrower,
      department: form.department || undefined,
      location: form.location || undefined,
      borrow_date: form.borrow_date || undefined,
      expected_return_date: form.expected_return_date || undefined,
      photo_url,
      remark: form.remark || undefined,
    })
    ElMessage.success('出借成功')
    emit('update:modelValue', false)
    emit('success')
  } catch (error) {
    console.error('出借失败', error)
  } finally {
    submitting.value = false
  }
}
</script>
