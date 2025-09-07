"use client"

import { AuthGuard } from '@/components/auth/authGuard'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { useAuth } from '@/hooks/useAuth'
import { useDesigns } from '@/hooks/useDesigns'
import { formatDistanceToNow } from 'date-fns'
import { Calendar, Loader2, Palette, Plus, User } from 'lucide-react'
import Link from 'next/link'
import { Badge } from '../ui/misc-components'

export function DashboardContent() {
  const { profile, isPremium } = useAuth()
  const { designs: designsResponse, loading } = useDesigns()

  // Extract designs array from response object
  const designs = Array.isArray(designsResponse) 
    ? designsResponse 
    : designsResponse?.designs || []

  return (
    <AuthGuard>
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold">Dashboard</h1>
            <p className="text-muted-foreground">
              Welcome back, {profile?.firstName || 'Designer'}!
            </p>
          </div>
          <div className="flex items-center gap-4">
            {isPremium && (
              <Badge variant="secondary" className="bg-yellow-100 text-yellow-800">
                Premium
              </Badge>
            )}
            <Link href="/">
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                New Design
              </Button>
            </Link>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Designs</CardTitle>
              <Palette className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{designs.length}</div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Published</CardTitle>
              <Calendar className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {designs.filter(d => d.status === 'published').length}
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Account Type</CardTitle>
              <User className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold capitalize">
                {profile?.role || 'User'}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Recent Designs */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Designs</CardTitle>
            <CardDescription>
              Your latest design projects
            </CardDescription>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="flex items-center justify-center py-8">
                <Loader2 className="h-6 w-6 animate-spin" />
              </div>
            ) : designs.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-muted-foreground mb-4">No designs yet</p>
                <Link href="/">
                  <Button>Create Your First Design</Button>
                </Link>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {designs.slice(0, 6).map((design) => (
                  <Card key={design.id} className="cursor-pointer hover:shadow-md transition-shadow">
                    <CardHeader>
                      <CardTitle className="text-lg">{design.title}</CardTitle>
                      <CardDescription>
                        {design.description || 'No description'}
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="flex items-center justify-between">
                        <Badge variant="outline">{design.status}</Badge>
                        <span className="text-xs text-muted-foreground">
                          {formatDistanceToNow(new Date(design.createdAt), { addSuffix: true })}
                        </span>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </AuthGuard>
  )
}