import { SignIn } from "@clerk/nextjs"

export default function SignInPage() {
  return (
    <div className="flex min-h-[80vh] items-center justify-center">
      <SignIn 
        appearance={{
          elements: {
            formButtonPrimary: "bg-indigo-600 hover:bg-indigo-700 text-white",
            card: "shadow-xl border-0",
            headerTitle: "text-2xl font-bold",
            headerSubtitle: "text-muted-foreground",
          }
        }}
      />
    </div>
  )
}