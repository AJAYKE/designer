"use client"

import { useAuth } from '@/hooks/useAuth'
import { Loader2 } from 'lucide-react'

interface AuthGuardProps {
  children: React.ReactNode
  fallback?: React.ReactNode
  requirePremium?: boolean
  requireAdmin?: boolean
}

export function AuthGuard({ 
  children, 
  fallback, 
  requirePremium = false, 
  requireAdmin = false 
}: AuthGuardProps) {
  const { isLoaded, isSignedIn, loading, isPremium, isAdmin } = useAuth()

  if (!isLoaded || loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    )
  }

  if (!isSignedIn) {
    return fallback || (
      <div className="text-center py-8">
        <p className="text-muted-foreground">Please sign in to access this content.</p>
      </div>
    )
  }

  if (requireAdmin && !isAdmin) {
    return (
      <div className="text-center py-8">
        <p className="text-muted-foreground">Admin access required.</p>
      </div>
    )
  }

  if (requirePremium && !isPremium) {
    return (
      <div className="text-center py-8">
        <p className="text-muted-foreground">Premium subscription required.</p>
      </div>
    )
  }

  return <>{children}</>
}
