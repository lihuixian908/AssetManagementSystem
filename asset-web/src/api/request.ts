import axios from 'axios'
import { ElMessage } from 'element-plus'
import type { ApiResponse } from '@/types'

const request = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
})

let lastMsg = ''
let lastTime = 0
const showError = (msg: string) => {
  const now = Date.now()
  if (msg !== lastMsg || now - lastTime > 2000) {
    lastMsg = msg; lastTime = now
    showError(msg)
  }
}

request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

request.interceptors.response.use(
  (response) => {
    // blob 响应（如 Excel 导出）跳过 JSON 格式校验
    if (response.config.responseType === 'blob') return response
    const data = response.data as ApiResponse
    if (data.code !== 200) {
      showError(data.message || '请求失败')
      return Promise.reject(new Error(data.message))
    }
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    } else {
      showError(error.response?.data?.detail || '网络错误')
    }
    return Promise.reject(error)
  }
)

export default request
