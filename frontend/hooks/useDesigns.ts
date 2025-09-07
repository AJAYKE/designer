"use client"

import { useApiClient } from '@/lib/apiClient'
import { useEffect, useState } from 'react'

export interface Design {
  id: string
  title: string
  description?: string
  promptConfig: Record<string, any>
  htmlCode?: string
  cssClasses?: string
  javascript?: string
  images: any[]
  status: string
  isPublic: boolean
  tags: string[]
  createdAt: string
  updatedAt?: string
}

export function useDesigns() {
  const [designs, setDesigns] = useState<Design[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const apiClient = useApiClient()

  const fetchDesigns = async () => {
    try {
      setLoading(true)
      const response = await apiClient.get('/api/v1/designs')
      setDesigns(response.data)
      setError(null)
    } catch (err) {
      setError('Failed to fetch designs')
      console.error('Error fetching designs:', err)
    } finally {
      setLoading(false)
    }
  }

  const createDesign = async (designData: Partial<Design>) => {
    try {
      const response = await apiClient.post('/api/v1/designs', designData)
      setDesigns(prev => [response.data, ...prev])
      return response.data
    } catch (err) {
      console.error('Error creating design:', err)
      throw err
    }
  }

  const updateDesign = async (id: string, updates: Partial<Design>) => {
    try {
      const response = await apiClient.put(`/api/v1/designs/${id}`, updates)
      setDesigns(prev => 
        prev.map(design => design.id === id ? response.data : design)
      )
      return response.data
    } catch (err) {
      console.error('Error updating design:', err)
      throw err
    }
  }

  const deleteDesign = async (id: string) => {
    try {
      await apiClient.delete(`/api/v1/designs/${id}`)
      setDesigns(prev => prev.filter(design => design.id !== id))
    } catch (err) {
      console.error('Error deleting design:', err)
      throw err
    }
  }

  useEffect(() => {
    fetchDesigns()
  }, [])

  return {
    designs,
    loading,
    error,
    fetchDesigns,
    createDesign,
    updateDesign,
    deleteDesign
  }
}
