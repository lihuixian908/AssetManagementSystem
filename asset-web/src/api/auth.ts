import request from './request'
import type { ApiResponse, User } from '@/types'

export const login = (username: string, password: string) => {
  return request.post<ApiResponse, ApiResponse>('/auth/login', { username, password })
}

export const logout = () => {
  return request.post<ApiResponse>('/auth/logout')
}

export const getCurrentUser = () => {
  return request.get<ApiResponse<User>>('/auth/me')
}

export const changePassword = (old_password: string, new_password: string) => {
  return request.put<ApiResponse>('/auth/password', { old_password, new_password })
}