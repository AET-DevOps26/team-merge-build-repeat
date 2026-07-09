import { Navigate, Outlet, useLocation } from "react-router-dom"
import { useAuth } from "./auth-context"

export function RequireAuth() {
  const { loading, session } = useAuth()
  const location = useLocation()

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <span className="material-symbols-outlined text-accent text-5xl animate-spin">
          progress_activity
        </span>
      </div>
    )
  }

  if (!session) {
    return <Navigate to="/login" replace state={{ from: location }} />
  }

  return <Outlet />
}
