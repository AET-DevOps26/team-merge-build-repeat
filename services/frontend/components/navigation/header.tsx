import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { useAuth } from "@/src/auth/auth-context"
import { useGame } from "@/src/game-context"
import { useTheme } from "@/src/theme-context"

interface HeaderProps {
  showBackButton?: boolean
  variant?: "default" | "chat"
}

export function Header({ showBackButton = false, variant = "default" }: HeaderProps) {
  const navigate = useNavigate()
  const { session, signOut } = useAuth()
  const { setActiveGameId } = useGame()
  const { theme, setTheme } = useTheme()
  const [signOutLoading, setSignOutLoading] = useState(false)
  const [signOutError, setSignOutError] = useState<string | null>(null)

  const handleAuthClick = async () => {
    if (!session) {
      navigate("/login")
      return
    }

    setSignOutLoading(true)
    setSignOutError(null)

    try {
      await signOut()
      localStorage.removeItem("activeGameId")
      setActiveGameId(null)
      navigate("/", { replace: true })
    } catch (err) {
      setSignOutError(err instanceof Error ? err.message : "Sign out failed.")
    } finally {
      setSignOutLoading(false)
    }
  }

  return (
    <header className="relative flex justify-between items-center w-full px-6 py-4 bg-primary border-b-4 border-secondary sticky top-0 z-40">
      <button
        onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
        className="text-secondary hover:bg-black/10 transition-colors p-2 rounded-full"
        aria-label="Toggle theme"
      >
        <span className="material-symbols-outlined text-3xl">
          {theme === "dark" ? "light_mode" : "dark_mode"}
        </span>
      </button>
      
      <Link to="/" className="text-2xl flex items-baseline">
        <span className="font-heading font-bold uppercase tracking-tighter text-secondary">
          PAULANA
        </span>
        <span className="font-heading font-bold text-white italic ml-1" style={{ textShadow: '2px 2px 0 #4834d4, -1px -1px 0 #4834d4' }}>
          ZUDOKYU
        </span>
      </Link>
      
      <button 
        onClick={handleAuthClick}
        disabled={signOutLoading}
        className="text-secondary hover:bg-black/10 transition-colors p-2 rounded-full"
        aria-label={session ? "Sign out" : "Sign in"}
      >
        <span className="material-symbols-outlined text-3xl">
          {signOutLoading ? "progress_activity" : session ? "logout" : variant === "chat" ? "more_vert" : "login"}
        </span>
      </button>
      {signOutError && (
        <p
          aria-live="polite"
          className="absolute right-6 top-full mt-2 max-w-[calc(100vw-3rem)] rounded border-2 border-secondary bg-card px-3 py-2 text-sm font-semibold text-destructive shadow-[3px_3px_0px_0px_var(--color-secondary)]"
        >
          {signOutError}
        </p>
      )}
    </header>
  )
}
