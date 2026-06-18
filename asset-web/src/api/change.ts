import request from './request'
import type { ApiResponse } from '@/types'

export const createChange = (data: {
  asset_id: number
  change_type: string
  new_value: string
  remark?: string
}) => {
  return request.post<ApiResponse>('/change', data)
}

export const getChangeHistory = (asset_id: number) => {
  return request.get<ApiResponse>('/change/history/' + asset_id)
}
