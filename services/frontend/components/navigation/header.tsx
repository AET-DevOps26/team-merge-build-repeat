import { Link, useNavigate } from "react-router-dom"
import { useAuth } from "@/src/auth/auth-context"

interface HeaderProps {
  showBackButton?: boolean
  variant?: "default" | "chat"
}

export function Header({ showBackButton = false, variant = "default" }: HeaderProps) {
  const navigate = useNavigate()
  const { session, signOut } = useAuth()

  return (
    <header className="flex justify-between items-center w-full px-6 py-4 bg-primary border-b-4 border-secondary sticky top-0 z-40">
      <button 
        onClick={showBackButton ? () => navigate(-1) : undefined}
        className="text-secondary hover:bg-black/10 transition-colors p-2 rounded-full"
        aria-label={showBackButton ? "Go back" : "Menu"}
      >
        <span className="material-symbols-outlined text-3xl">
          {showBackButton ? "arrow_back" : "menu"}
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
        onClick={session ? signOut : () => navigate("/login")}
        className="text-secondary hover:bg-black/10 transition-colors p-2 rounded-full"
        aria-label={session ? "Sign out" : "Sign in"}
      >
        <span className="material-symbols-outlined text-3xl">
          {session ? "logout" : variant === "chat" ? "more_vert" : "login"}
        </span>
      </button>
    </header>
  )
}
