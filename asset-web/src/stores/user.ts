import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { User } from '@/types'
import { getCurrentUser } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string>(localStorage.getItem('token') || '')

  const setToken = (newToken: string) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  const fetchUser = async () => {
    try {
      const { data } = await getCurrentUser()
      user.value = data.data as User
    } catch (error) {
      user.value = null
    }
  }

  const logout = () => {
    user.value = null
    token.value = ''
    localStorage.removeItem('token')
  }

  return { user, token, setToken, fetchUser, logout }
})