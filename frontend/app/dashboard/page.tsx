import { DashboardContent } from "@/components/dashboard/dashboardContent"
import { auth } from "@clerk/nextjs/server"
import { redirect } from "next/navigation"

export default async function DashboardPage() {
  const { userId } = await auth()

  if (!userId) {
    redirect("/signin")
  }

  return <DashboardContent />
}