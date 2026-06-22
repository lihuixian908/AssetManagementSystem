import request from './request'
import type { ApiResponse } from '@/types'

export const createBorrow = (data: {
  asset_id: number
  borrower: string
  department?: string
  location?: string
  borrow_date?: string
  expected_return_date?: string
  remark?: string
}) => {
  return request.post<ApiResponse>('/borrow', data)
}

export const returnBorrow = (asset_id: number) => {
  return request.post<ApiResponse>('/borrow/return', null, { params: { asset_id } })
}

export const cancelBorrow = (record_id: number) => {
  return request.delete<ApiResponse>('/borrow/' + record_id)
}

export const getPendingBorrows = () => {
  return request.get<ApiResponse>('/borrow/pending')
}

export const approveBorrow = (id: number) => {
  return request.post<ApiResponse>(`/borrow/${id}/approve`)
}

export const rejectBorrow = (id: number) => {
  return request.post<ApiResponse>(`/borrow/${id}/reject`)
}

export const getBorrowHistory = (asset_id: number) => {
  return request.get<ApiResponse>('/borrow/history/' + asset_id)
}
