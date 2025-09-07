import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'

// Protected routes
const isProtectedRoute = createRouteMatcher([
  '/dashboard(.*)',
  '/create(.*)',
  '/browse(.*)',
  '/api/v1(.*)',
])

// Public routes
const isPublicRoute = createRouteMatcher([
  '/',
  // Support both /signin and /sign-in patterns
  '/signin(.*)',
  '/sign-in(.*)',
  '/signup(.*)',
  '/sign-up(.*)',
  '/api/public(.*)',
  '/health',
])

export default clerkMiddleware(async (auth, req) => {
  // Allow public routes through
  if (isPublicRoute(req)) return

  // Protect everything else
  if (isProtectedRoute(req)) {
    await auth.protect()
    return
  }
})

export const config = {
  matcher: [
    // Skip Next.js internals and static assets
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    // Always run for API routes
    '/(api|trpc)(.*)',
  ],
}
