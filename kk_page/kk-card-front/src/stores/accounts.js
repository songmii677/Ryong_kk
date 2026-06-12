import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000'

export const useAccountStore = defineStore('accounts', () => {
  const token = ref(localStorage.getItem('token') || '')
  const username = ref(localStorage.getItem('username') || '')

  const isLogin = computed(() => {
    return !!token.value
  })

  function saveAuthData(newToken, newUsername) {
    token.value = newToken
    username.value = newUsername

    localStorage.setItem('token', newToken)
    localStorage.setItem('username', newUsername)
  }

  function clearAuthData() {
    token.value = ''
    username.value = ''

    localStorage.removeItem('token')
    localStorage.removeItem('username')
  }

  async function signup(payload) {
    const response = await axios.post(`${API_URL}/accounts/signup/`, {
      username: payload.username,
      password1: payload.password1,
      password2: payload.password2,
    })

    saveAuthData(response.data.key, payload.username)

    return response.data
  }

  async function login(payload) {
    const response = await axios.post(`${API_URL}/accounts/login/`, {
      username: payload.username,
      password: payload.password,
    })

    saveAuthData(response.data.key, payload.username)

    return response.data
  }

  async function logout() {
    try {
      if (token.value) {
        await axios.post(
          `${API_URL}/accounts/logout/`,
          {},
          {
            headers: {
              Authorization: `Token ${token.value}`,
            },
          }
        )
      }
    } catch (error) {
      console.error('로그아웃 요청 실패:', error)
    } finally {
      clearAuthData()
    }
  }

  return {
    token,
    username,
    isLogin,
    signup,
    login,
    logout,
    clearAuthData,
  }
})