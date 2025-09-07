"use client"

import { ThemeToggle } from "@/components/theme/theme-toggle"
import { Button } from "@/components/ui/button"
import {
  SignedIn,
  SignedOut,
  SignInButton,
  SignUpButton,
  UserButton,
  useUser
} from "@clerk/nextjs"
import { Palette, Sparkles } from "lucide-react"
import Link from "next/link"
import { usePathname } from "next/navigation"

const navigation = [
  { name: "Create", href: "/create" },
  { name: "Browse", href: "/browse" },
  { name: "Learn", href: "/learn" },
  { name: "Pricing", href: "/pricing" },
]

export function Navbar() {
  const pathname = usePathname()
  const { user } = useUser()

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 max-w-screen-2xl items-center">
        {/* Logo */}
        <Link href="/" className="mr-6 flex items-center space-x-2">
          <Palette className="h-6 w-6 text-indigo-600" />
          <span className="font-bold text-xl">DEZ</span>
        </Link>

        {/* Navigation Links */}
        {/* <div className="mr-4 hidden md:flex">
          <nav className="flex items-center space-x-6 text-sm font-medium">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  "transition-colors hover:text-foreground/80",
                  pathname === item.href
                    ? "text-foreground"
                    : "text-foreground/60"
                )}
              >
                {item.name}
              </Link>
            ))}
          </nav>
        </div> */}

        {/* Right side */}
        <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
          {/* User-specific navigation */}
          <SignedIn>
            <div className="hidden md:flex items-center space-x-4">
              <Link href="/dashboard">
                <Button variant="ghost" size="sm">
                  Dashboard
                </Button>
              </Link>
              {user?.publicMetadata?.role === 'premium' && (
                <Sparkles className="h-4 w-4 text-yellow-500" />
              )}
            </div>
          </SignedIn>

          <div className="flex items-center space-x-4">
            <ThemeToggle />
            
            {/* Authentication Buttons */}
            <SignedOut>
              <SignInButton mode="modal">
                <Button variant="ghost" size="sm">
                  Sign in
                </Button>
              </SignInButton>
              <SignUpButton mode="modal">
                <Button size="sm">
                  Get started
                </Button>
              </SignUpButton>
            </SignedOut>

            <SignedIn>
              <UserButton
                appearance={{
                  elements: {
                    avatarBox: "h-8 w-8"
                  }
                }}
                userProfileMode="modal"
                afterSignOutUrl="/"
              />
            </SignedIn>
          </div>
        </div>
      </div>
    </nav>
  )
}