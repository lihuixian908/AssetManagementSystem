<template>
  <div class="user-list">
    <el-card v-if="!isMobile">
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
          <div>
            <el-input v-model="keyword" placeholder="搜索用户" style="width: 200px" clearable @change="fetchUsers" />
            <el-button type="primary" style="margin-left: 12px" @click="handleAdd" v-if="isAdmin">
              <el-icon><Plus /></el-icon>
              新增用户
            </el-button>
          </div>
        </div>
      </template>

      <div style="margin-bottom: 8px" v-if="selectedUserIds.length > 0 && isAdmin">
        <el-button type="danger" @click="handleBatchDeleteUsers">批量删除（{{ selectedUserIds.length }}）</el-button>
      </div>
      <el-table :data="users" v-loading="loading" border stripe @selection-change="onUserSelectionChange">
        <el-table-column type="selection" width="45" v-if="isAdmin" />
        <el-table-column prop="username" label="用户名" width="130" />
        <el-table-column prop="real_name" label="真实姓名" width="120" />
        <el-table-column prop="department" label="所属部门" width="120"><template #default="{ row }">{{ row.department || '-' }}</template></el-table-column>
        <el-table-column label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="row.role === 'admin' ? 'danger' : row.role === 'asset_admin' ? 'warning' : ''">
              {{ row.role === 'admin' ? '系统管理员' : row.role === 'asset_admin' ? '资产管理员' : '普通员工' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'danger'">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="phone" label="手机号" width="140" />
        <el-table-column prop="email" label="邮箱" min-width="160" />
        <el-table-column label="操作" width="280" fixed="right" v-if="isAdmin">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="warning" @click="handleResetPwd(row)">重置密码</el-button>
            <el-button link :type="row.status === 1 ? 'danger' : 'success'" @click="handleToggleStatus(row)">
              {{ row.status === 1 ? '禁用' : '启用' }}
            </el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next"
        @current-change="fetchUsers"
        style="margin-top: 20px; justify-content: flex-end"
      />
    </el-card>

    <!-- 手机卡片 -->
    <div v-if="isMobile" v-loading="loading">
      <el-card v-for="u in users" :key="u.id" style="margin-bottom: 10px">
        <div style="display:flex;justify-content:space-between"><strong>{{ u.real_name }}</strong><el-tag :type="u.role==='admin'?'danger':''" size="small">{{ u.role==='admin'?'管理员':'普通用户' }}</el-tag></div>
        <p style="margin:4px 0;font-size:13px;color:#606266">@{{ u.username }} | {{ u.department || '无部门' }} | {{ u.status===1?'启用':'禁用' }}</p>
        <div style="display:flex;gap:6px" v-if="isAdmin"><el-button size="small" @click="handleEdit(u)">编辑</el-button><el-button size="small" type="warning" @click="handleResetPwd(u)">重置</el-button><el-button size="small" :type="u.status===1?'danger':'success'" @click="handleToggleStatus(u)">{{ u.status===1?'禁用':'启用' }}</el-button></div>
      </el-card>
    </div>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="formVisible" :title="isEdit ? '编辑用户' : '新增用户'" width="450px" @closed="resetForm">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="90px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" :disabled="isEdit" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="真实姓名" prop="real_name">
          <el-input v-model="form.real_name" placeholder="请输入真实姓名" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!isEdit">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item label="所属部门">
          <el-input v-model="form.department" placeholder="请输入所属部门" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role" style="width: 100%">
            <el-option label="系统管理员" value="admin" />
            <el-option label="资产管理员" value="asset_admin" />
            <el-option label="普通员工" value="user" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" v-if="isEdit">
          <el-switch v-model="form.status" active-text="启用" inactive-text="禁用" :active-value="1" :inactive-value="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="formVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">提交</el-button>
      </template>
    </el-dialog>

    <!-- 重置密码弹窗 -->
    <el-dialog v-model="pwdVisible" title="重置密码" width="380px" @closed="resetPwdForm">
      <el-form :model="pwdForm" :rules="pwdRules" ref="pwdFormRef" label-width="90px">
        <el-form-item label="新密码" prop="new_password">
          <el-input v-model="pwdForm.new_password" type="password" placeholder="请输入新密码" show-password />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirm_password">
          <el-input v-model="pwdForm.confirm_password" type="password" placeholder="请再次输入新密码" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="pwdVisible = false">取消</el-button>
        <el-button type="primary" @click="handleResetPwdSubmit" :loading="pwdSubmitting">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { getUsers, createUser, updateUser, deleteUser, resetPassword } from '@/api/user'
import request from '@/api/request'
import { useUserStore } from '@/stores/user'
import type { User } from '@/types'

const isMobile = ref(window.innerWidth < 768)
window.addEventListener('resize', () => { isMobile.value = window.innerWidth < 768 })
const userStore = useUserStore()
const isAdmin = computed(() => userStore.user?.role === 'admin')

const users = ref<User[]>([])
const loading = ref(false)
const keyword = ref('')
const selectedUserIds = ref<number[]>([])
const onUserSelectionChange = (rows: any[]) => { selectedUserIds.value = rows.map((r: any) => r.id) }
const handleBatchDeleteUsers = async () => {
  try {
    await ElMessageBox.confirm(`确认删除选中的 ${selectedUserIds.value.length} 名用户吗？`, '批量删除', { type: 'warning' })
    await request.post('/users/batch-delete', selectedUserIds.value)
    ElMessage.success('批量删除成功')
    selectedUserIds.value = []
    fetchUsers()
  } catch (e: any) { if (e !== 'cancel' && e !== 'close') console.error(e) }
}

const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

const fetchUsers = async () => {
  loading.value = true
  try {
    const { data } = await getUsers({ page: page.value, page_size: pageSize.value, keyword: keyword.value })
    users.value = data.data.items
    total.value = data.data.total
  } catch (e) {
    console.error('获取用户列表失败', e)
  } finally {
    loading.value = false
  }
}

// ========== 新增/编辑 ==========
const formVisible = ref(false)
const isEdit = ref(false)
const editId = ref<number | null>(null)
const submitting = ref(false)
const formRef = ref<FormInstance>()

const form = reactive({
  username: '',
  real_name: '',
  password: '',
  department: '',
  role: 'user' as string,
  status: 1,
})

const rules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名3~20位', trigger: 'blur' },
  ],
  real_name: [{ required: true, message: '请输入真实姓名', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, max: 20, message: '密码8~20位', trigger: 'blur' },
    { pattern: /^(?=.*[a-zA-Z])(?=.*\d)/, message: '密码需包含字母和数字', trigger: 'blur' },
  ],
}

const resetForm = () => {
  form.username = ''
  form.real_name = ''
  form.password = ''
  form.department = ''
  form.role = 'user'
  form.status = 1
  isEdit.value = false
  editId.value = null
  formRef.value?.resetFields()
}

const handleAdd = () => {
  resetForm()
  formVisible.value = true
}

const handleEdit = (row: User) => {
  resetForm()
  isEdit.value = true
  editId.value = row.id
  form.username = row.username
  form.real_name = row.real_name
  form.department = row.department || ''
  form.role = row.role
  form.status = row.status
  formVisible.value = true
}

const handleSubmit = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    if (isEdit.value && editId.value) {
      await updateUser(editId.value, {
        real_name: form.real_name,
        department: form.department,
        role: form.role,
        status: form.status,
      })
      ElMessage.success('编辑成功')
    } else {
      await createUser({
        username: form.username,
        password: form.password,
        real_name: form.real_name,
        department: form.department,
        role: form.role,
      })
      ElMessage.success('新增成功')
    }
    formVisible.value = false
    fetchUsers()
  } catch (e) {
    console.error('提交失败', e)
  } finally {
    submitting.value = false
  }
}

// ========== 删除 ==========
const handleDelete = async (row: User) => {
  try {
    await ElMessageBox.confirm(`确认删除用户【${row.real_name}】吗？`, '提示', { type: 'warning' })
    await deleteUser(row.id)
    ElMessage.success('删除成功')
    fetchUsers()
  } catch (e: any) {
    if (e !== 'cancel' && e !== 'close') console.error(e)
  }
}

// ========== 重置密码 ==========
const pwdVisible = ref(false)
const pwdSubmitting = ref(false)
const pwdFormRef = ref<FormInstance>()
const pwdUserId = ref<number | null>(null)

const pwdForm = reactive({
  new_password: '',
  confirm_password: '',
})

const validateConfirmPwd = (_rule: any, value: string, callback: any) => {
  if (value !== pwdForm.new_password) {
    callback(new Error('两次密码不一致'))
  } else {
    callback()
  }
}

const pwdRules: FormRules = {
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 8, max: 20, message: '密码8~20位', trigger: 'blur' },
    { pattern: /^(?=.*[a-zA-Z])(?=.*\d)/, message: '密码需包含字母和数字', trigger: 'blur' },
  ],
  confirm_password: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirmPwd, trigger: 'blur' },
  ],
}

const resetPwdForm = () => {
  pwdForm.new_password = ''
  pwdForm.confirm_password = ''
  pwdUserId.value = null
  pwdFormRef.value?.resetFields()
}

const handleResetPwd = (row: User) => {
  resetPwdForm()
  pwdUserId.value = row.id
  pwdVisible.value = true
}

const handleResetPwdSubmit = async () => {
  const valid = await pwdFormRef.value?.validate().catch(() => false)
  if (!valid || !pwdUserId.value) return

  pwdSubmitting.value = true
  try {
    await resetPassword(pwdUserId.value, pwdForm.new_password)
    ElMessage.success('密码重置成功')
    pwdVisible.value = false
  } catch (e) {
    console.error('重置密码失败', e)
  } finally {
    pwdSubmitting.value = false
  }
}

// ========== 启用/禁用 ==========
const handleToggleStatus = async (row: User) => {
  const newStatus = row.status === 1 ? 0 : 1
  const label = newStatus === 0 ? '禁用' : '启用'
  try {
    await ElMessageBox.confirm(`确认${label}用户【${row.real_name}】吗？`, '提示', { type: 'warning' })
    await updateUser(row.id, { status: newStatus })
    ElMessage.success(`${label}成功`)
    fetchUsers()
  } catch (e: any) {
    if (e !== 'cancel' && e !== 'close') console.error(e)
  }
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>