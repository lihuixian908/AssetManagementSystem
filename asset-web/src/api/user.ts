import request from './request'
import type { ApiResponse, User } from '@/types'

export const getUsers = (params?: any) => {
  return request.get<ApiResponse<{ items: User[]; total: number }>>('/users', { params })
}

export const createUser = (data: {
  username: string
  password: string
  real_name: string
  department?: string
  role?: string
}) => {
  return request.post<ApiResponse>('/users', data)
}

export const updateUser = (id: number, data: any) => {
  return request.put<ApiResponse>(`/users/${id}`, data)
}

export const deleteUser = (id: number) => {
  return request.delete<ApiResponse>(`/users/${id}`)
}

export const resetPassword = (id: number, new_password: string) => {
  return request.post<ApiResponse>(`/users/${id}/reset-password`, { new_password })
}
