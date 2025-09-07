import { auth } from '@clerk/nextjs/server'
import axios, { AxiosInstance, AxiosResponse } from 'axios'

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  async (config) => {
    // This is for server-side requests
    if (typeof window === 'undefined') {
      try {
        const { getToken } = await auth()
        const token = await getToken()
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
      } catch (error) {
        console.error('Error getting token on server:', error)
      }
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      if (typeof window !== 'undefined') {
        // Client-side: redirect to sign-in
        window.location.href = '/sign-in'
      }
    }
    return Promise.reject(error)
  }
)

export default api
