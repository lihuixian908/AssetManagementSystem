import request from './request'
import type { ApiResponse, Asset, AssetRecord, PaginationResult } from '@/types'

export const getAssets = (params: any) => {
  return request.get<ApiResponse<PaginationResult<Asset>>>('/assets', { params })
}

export const getAsset = (id: number) => {
  return request.get<ApiResponse<Asset>>(`/assets/${id}`)
}

export const createAsset = (data: any) => {
  return request.post<ApiResponse<Asset>>('/assets', data)
}

export const updateAsset = (id: number, data: any) => {
  return request.put<ApiResponse<Asset>>(`/assets/${id}`, data)
}

export const deleteAsset = (id: number) => {
  return request.delete<ApiResponse>(`/assets/${id}`)
}

export const assignAsset = (id: number, user_id: number, description?: string) => {
  return request.post<ApiResponse>(`/assets/${id}/assign`, null, { params: { user_id, description } })
}

export const returnAsset = (id: number, description?: string) => {
  return request.post<ApiResponse>(`/assets/${id}/return`, null, { params: { description } })
}

export const transferAsset = (id: number, department: string, user_id?: number, description?: string) => {
  return request.post<ApiResponse>(`/assets/${id}/transfer`, null, { params: { department, user_id, description } })
}

export const maintenanceAsset = (id: number, description?: string) => {
  return request.post<ApiResponse>(`/assets/${id}/maintenance`, null, { params: { description } })
}

export const scrapAsset = (id: number, description?: string) => {
  return request.post<ApiResponse>(`/assets/${id}/scrap`, null, { params: { description } })
}

export const scanAsset = (id: number) => {
  return request.post<ApiResponse>(`/assets/${id}/scan`)
}

export const getAssetRecords = (id: number, params?: any) => {
  return request.get<ApiResponse<PaginationResult<AssetRecord>>>(`/assets/${id}/records`, { params })
}

export const importAssets = (data: FormData) => {
  return request.post<ApiResponse>('/assets/import', data)
}