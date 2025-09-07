"use client"

import { useAuth } from '@clerk/nextjs'
import axios from 'axios'

let _apiClient: ReturnType<typeof axios.create> | null = null

export function useApiClient() {
  const { getToken } = useAuth()

  if (_apiClient) return _apiClient

  const baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  const apiClient = axios.create({
    baseURL,
    timeout: 30000,
    headers: { 'Content-Type': 'application/json' },
  })

  apiClient.interceptors.request.use(
    async (config) => {
      try {
        // Get the session token (which is actually a JWT in Clerk)
        const token = await getToken({ skipCache: true })
        
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
          // Optional: Log token type for debugging
          console.log('Token acquired, length:', token.length)
        } else {
          console.warn('No token available - user may not be signed in')
        }
      } catch (err) {
        console.error('Error getting token:', err)
      }
      return config
    },
    (error) => Promise.reject(error)
  )

  apiClient.interceptors.response.use(
    (res) => res,
    async (error) => {
      if (error.response?.status === 401) {
        console.error('Authentication failed:', error.response.data)
        // Avoid redirect loops
        if (typeof window !== 'undefined' && window.location.pathname !== '/signin') {
          window.location.href = '/signin'
        }
      }
      return Promise.reject(error)
    }
  )

  _apiClient = apiClient
  return apiClient
}

// Your existing API service
export const apiService = {
  generateDesign: (config: any) => useApiClient().post('/api/v1/generate', config),
  getUserData: () => useApiClient().get('/api/v1/auth/me'),
  saveDesign: (designData: any) => useApiClient().post('/api/v1/designs', designData),
  getDesigns: () => useApiClient().get('/api/v1/designs'),
  deleteDesign: (designId: string) => useApiClient().delete(`/api/v1/designs/${designId}`),
}