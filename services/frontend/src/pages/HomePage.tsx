import { Link } from "react-router-dom"
import { Header, BottomNav } from "@/components/navigation"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header />
      
      <main className="flex-1 flex flex-col items-center justify-center px-6 py-8 pb-24">
        {/* Logo */}
        <div className="text-center mb-12">
          <h1 className="font-heading font-bold text-4xl sm:text-5xl text-secondary uppercase tracking-tight">
            PAULANA
          </h1>
          <h2 
            className="font-heading font-bold text-5xl sm:text-7xl text-white uppercase tracking-tighter" 
            style={{ textShadow: '3px 3px 0 #4834d4' }}
          >
            ZUDOKYU
          </h2>
        </div>

        {/* Buttons */}
        <div className="w-full max-w-md space-y-4">
          <Link
            to="/game"
            className="flex items-center justify-center gap-3 w-full bg-accent text-white font-heading font-bold text-xl py-4 px-8 rounded-xl border-2 border-primary shadow-[4px_4px_0px_0px_var(--color-primary)] hover:brightness-110 transition-all active:translate-y-1 active:translate-x-1 active:shadow-none"
          >
            <span className="material-symbols-outlined text-2xl">play_circle</span>
            NEW GAME
          </Link>
          
          <Link
            to="/game"
            className="flex items-center justify-center gap-3 w-full bg-accent/80 text-white font-heading font-bold text-xl py-4 px-8 rounded-xl border-2 border-primary shadow-[4px_4px_0px_0px_var(--color-primary)] hover:brightness-110 transition-all active:translate-y-1 active:translate-x-1 active:shadow-none"
          >
            <span className="material-symbols-outlined text-2xl">fast_forward</span>
            CONTINUE
          </Link>
        </div>
      </main>

      <BottomNav />
    </div>
  )
}
