import { useState } from "react"
import { Link } from "react-router-dom"
import { Header, BottomNav } from "@/components/navigation"
import { cn } from "@/lib/utils"

type Difficulty = "easy" | "medium" | "hard"

const difficulties: { id: Difficulty; label: string; emoji: string; emojiColor: string }[] = [
  { id: "easy", label: "EASY", emoji: "sentiment_satisfied", emojiColor: "text-primary" },
  { id: "medium", label: "MEDIUM", emoji: "sentiment_neutral", emojiColor: "text-accent" },
  { id: "hard", label: "HARD", emoji: "sentiment_very_dissatisfied", emojiColor: "text-destructive" },
]

export default function HomePage() {
  const [selectedDifficulty, setSelectedDifficulty] = useState<Difficulty>("medium")

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
        <div className="w-full max-w-md space-y-4 mb-12">
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

        {/* Difficulty Selection */}
        <div className="w-full max-w-md">
          <div className="flex items-center gap-2 mb-4">
            <span className="w-4 h-1 bg-destructive rounded-full" />
            <span className="font-mono text-xs text-muted-foreground uppercase tracking-widest">
              Select Difficulty
            </span>
          </div>
          
          <div className="grid grid-cols-3 gap-3">
            {difficulties.map((diff) => (
              <button
                key={diff.id}
                onClick={() => setSelectedDifficulty(diff.id)}
                className={cn(
                  "flex flex-col items-center justify-center py-4 px-2 rounded-lg border-2 transition-all",
                  selectedDifficulty === diff.id
                    ? "bg-muted border-accent shadow-[3px_3px_0px_0px_var(--color-accent)]"
                    : "bg-card border-border hover:border-accent/50"
                )}
              >
                <span className="font-mono text-xs text-muted-foreground mb-2">
                  {diff.label}
                </span>
                <span 
                  className={cn("material-symbols-outlined text-3xl", diff.emojiColor)}
                  style={{ fontVariationSettings: "'FILL' 1" }}
                >
                  {diff.emoji}
                </span>
              </button>
            ))}
          </div>
        </div>
      </main>

      <BottomNav />
    </div>
  )
}
