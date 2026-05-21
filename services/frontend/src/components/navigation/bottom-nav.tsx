import { Link, useLocation } from "react-router-dom"
import { cn } from "@/lib/utils"

const navItems = [
  { href: "/", icon: "grid_view", label: "PLAY" },
  { href: "/stats", icon: "leaderboard", label: "STATS" },
  { href: "/ai", icon: "smart_toy", label: "AI" },
  { href: "/rank", icon: "workspace_premium", label: "RANK" },
]

export function BottomNav() {
  const { pathname } = useLocation()

  return (
    <nav className="fixed bottom-0 left-0 w-full z-50 flex justify-around items-center px-4 py-3 bg-secondary border-t-4 border-destructive rounded-t-2xl shadow-[0_-4px_0px_0px_var(--color-accent)]">
      {navItems.map((item) => {
        const isActive = pathname === item.href || 
          (item.href === "/" && pathname === "/game")
        
        return (
          <Link
            key={item.href}
            to={item.href}
            className={cn(
              "flex flex-col items-center justify-center transition-all",
              isActive
                ? "bg-accent text-secondary rounded-lg py-1 px-4 border-2 border-secondary shadow-[3px_3px_0px_0px_rgba(0,0,0,0.5)]"
                : "text-primary p-2 hover:text-white"
            )}
          >
            <span 
              className={cn(
                "material-symbols-outlined text-2xl",
                isActive && "fill"
              )}
              style={{ fontVariationSettings: isActive ? "'FILL' 1" : "'FILL' 0" }}
            >
              {item.icon}
            </span>
            <span className="mt-1 font-mono text-[10px] font-bold tracking-widest">
              {item.label}
            </span>
          </Link>
        )
      })}
    </nav>
  )
}
