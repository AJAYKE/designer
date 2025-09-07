import { Navbar } from '@/components/layout/navbar'
import { ToastProvider } from '@/components/providers/toastProvider'
import { ThemeProvider } from '@/components/theme/themeProvider'
import { ClerkProvider } from "@clerk/nextjs"
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'AI Design Platform',
  description: 'Create beautiful designs with AI-powered tools',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider
      publishableKey={process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY!}
      appearance={{
        baseTheme: undefined, 
        variables: {
          colorPrimary: "#6366f1", 
          colorBackground: "#ffffff",
          colorInputBackground: "#ffffff",
          colorInputText: "#1f2937",
        },
        elements: {
          formButtonPrimary: "bg-indigo-600 hover:bg-indigo-700 text-white",
          card: "shadow-lg border border-gray-200",
        }
      }}
    >
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <div className="min-h-screen bg-background text-foreground">
          <Navbar />
            {children}
          </div>
          <ToastProvider />
        </ThemeProvider>
      </body>
    </html>
    </ClerkProvider>
  )
}