export interface User {
  id: number
  username: string
  real_name: string
  department: string | null
  role: string
  phone: string | null
  email: string | null
  status: number
}

export interface UserCreate {
  username: string
  password: string
  real_name: string
  role: string
}

export interface Asset {
  id: number
  asset_code: string
  company_code: string | null
  sn: string | null
  name: string
  category_id: number
  department: string | null
  user_id: number | null
  owner_name?: string | null
  location: string | null
  status: string
  price: number | null
  purchase_date: string | null
  description: string | null
  images: string[] | null
  qr_code_url: string | null
  created_at: string
  updated_at: string
}

export interface Category {
  id: number
  name: string
  code: string
  parent_id: number
  sort_order: number
  status: number
}

export interface AssetRecord {
  id: number
  asset_id: number
  user_id: number | null
  type: string
  type_name: string
  description: string | null
  operator: string
  created_at: string
}

export interface BorrowRecord {
  id: number
  asset_id: number
  borrower: string
  department: string | null
  borrow_date: string
  expected_return_date: string | null
  actual_return_date: string | null
  status: string
  remark: string | null
  created_at: string
}

export interface ChangeRecord {
  id: number
  asset_id: number
  change_type: string
  change_type_label: string
  old_value: string | null
  new_value: string
  operator: string
  remark: string | null
  created_at: string
}

export interface PaginationResult<T = any> {
  total: number
  page: number
  page_size: number
  items: T[]
}

export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}