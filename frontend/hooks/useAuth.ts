"use client"

import { useApiClient } from '@/lib/apiClient'
import { useAuth as useClerkAuth, useUser } from '@clerk/nextjs'
import { useEffect, useState } from 'react'

export interface UserProfile {
  id: string
  email: string
  firstName?: string
  lastName?: string
  imageUrl?: string
  role: string
  metadata: Record<string, any>
  createdAt: string
}

export function useAuth() {
  const { user, isLoaded, isSignedIn } = useUser()
  const { getToken } = useClerkAuth()
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [loading, setLoading] = useState(true)
  const apiClient = useApiClient()

  useEffect(() => {
    if (isLoaded && isSignedIn && user) {
      // Fetch user profile from our backend
      fetchUserProfile()
    } else if (isLoaded) {
      setLoading(false)
    }
  }, [isLoaded, isSignedIn, user])

  const fetchUserProfile = async () => {
    try {
      const response = await apiClient.get('/api/v1/auth/me')
      setProfile(response.data)
    } catch (error) {
      console.error('Failed to fetch user profile:', error)
    } finally {
      setLoading(false)
    }
  }

  const updateProfile = async (updates: Partial<UserProfile>) => {
    try {
      const response = await apiClient.put('/api/v1/auth/me', updates)
      setProfile(response.data)
      return response.data
    } catch (error) {
      console.error('Failed to update profile:', error)
      throw error
    }
  }

  const isPremium = profile?.role === 'premium' || profile?.role === 'admin'
  const isAdmin = profile?.role === 'admin'

  return {
    user,
    profile,
    isLoaded,
    isSignedIn,
    loading,
    isPremium,
    isAdmin,
    getToken,
    updateProfile,
    refetchProfile: fetchUserProfile
  }
}



