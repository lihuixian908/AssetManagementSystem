<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    title="设备归还"
    width="420px"
    @closed="resetForm"
  >
    <el-form label-width="90px">
      <el-form-item label="设备名称"><span>{{ asset?.name }}</span></el-form-item>
      <el-form-item label="归还照片">
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
    </el-form>
    <template #footer>
      <el-button @click="$emit('update:modelValue', false)">取消</el-button>
      <el-button type="primary" @click="handleConfirm" :loading="submitting">确认归还</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import type { UploadInstance, UploadFile } from 'element-plus'
import { returnBorrow } from '@/api/borrow'
import request from '@/api/request'
import type { Asset } from '@/types'

const props = defineProps<{ modelValue: boolean; asset: Asset | null }>()
const emit = defineEmits<{ 'update:modelValue': [boolean]; success: [] }>()

const uploadRef = ref<UploadInstance>()
const submitting = ref(false)
const photoFile = ref<File | null>(null)

const onPhotoChange = (file: UploadFile) => { photoFile.value = file.raw || null }
const onPhotoRemove = () => { photoFile.value = null }

const resetForm = () => { photoFile.value = null; uploadRef.value?.clearFiles() }

const handleConfirm = async () => {
  if (!props.asset) return
  submitting.value = true
  try {
    let return_photo_url = undefined
    if (photoFile.value) {
      const fd = new FormData()
      fd.append('file', photoFile.value)
      const { data } = await request.post('/upload', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
      return_photo_url = data.data.url
    }
    await request.post('/borrow/return', null, { params: { asset_id: props.asset.id, return_photo_url } })
    ElMessage.success('归还成功')
    emit('update:modelValue', false)
    emit('success')
  } catch (e) { /* */ } finally { submitting.value = false }
}
</script>
