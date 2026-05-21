import { Header, BottomNav } from "@/components/navigation"
import { cn } from "@/lib/utils"

const leaderboard = [
  { rank: 1, name: "SudokuMaster99", score: 125430, badge: "crown" },
  { rank: 2, name: "PuzzleQueen", score: 118250, badge: "military_tech" },
  { rank: 3, name: "GridWizard", score: 112890, badge: "emoji_events" },
  { rank: 4, name: "NumberNinja", score: 98450, badge: null },
  { rank: 5, name: "LogicLord", score: 95200, badge: null },
  { rank: 6, name: "BrainStorm", score: 92100, badge: null },
  { rank: 7, name: "You", score: 89500, badge: null, isCurrentUser: true },
  { rank: 8, name: "CellSolver", score: 87300, badge: null },
  { rank: 9, name: "MatrixMind", score: 85100, badge: null },
  { rank: 10, name: "PuzzlePro", score: 82900, badge: null },
]

export default function RankPage() {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header />
      
      <main className="flex-1 px-4 py-6 pb-24 max-w-lg mx-auto w-full">
        {/* Title */}
        <div className="mb-8 text-center">
          <h1 className="font-heading font-bold text-4xl text-primary uppercase">
            LEADERBOARD
          </h1>
          <p className="font-sans text-muted-foreground mt-2">
            Top Sudoku players worldwide
          </p>
        </div>

        {/* Leaderboard */}
        <div className="space-y-3">
          {leaderboard.map((player) => (
            <div
              key={player.rank}
              className={cn(
                "flex items-center gap-4 p-4 rounded-xl border-2 transition-all",
                player.isCurrentUser
                  ? "bg-accent/20 border-accent shadow-[4px_4px_0px_0px_var(--color-accent)]"
                  : player.rank <= 3
                    ? "bg-secondary/50 border-secondary shadow-[3px_3px_0px_0px_var(--color-secondary)]"
                    : "bg-card border-border"
              )}
            >
              {/* Rank */}
              <div className={cn(
                "w-10 h-10 flex items-center justify-center rounded-lg font-heading font-bold text-lg",
                player.rank === 1 ? "bg-primary text-secondary" :
                player.rank === 2 ? "bg-gray-300 text-gray-800" :
                player.rank === 3 ? "bg-amber-700 text-white" :
                "bg-muted text-muted-foreground"
              )}>
                {player.rank}
              </div>

              {/* Badge */}
              {player.badge && (
                <span 
                  className={cn(
                    "material-symbols-outlined text-2xl",
                    player.rank === 1 ? "text-primary" :
                    player.rank === 2 ? "text-gray-400" :
                    "text-amber-600"
                  )}
                  style={{ fontVariationSettings: "'FILL' 1" }}
                >
                  {player.badge}
                </span>
              )}

              {/* Name */}
              <div className="flex-1">
                <span className={cn(
                  "font-sans font-bold",
                  player.isCurrentUser ? "text-accent" : "text-foreground"
                )}>
                  {player.name}
                </span>
              </div>

              {/* Score */}
              <div className="text-right">
                <span className={cn(
                  "font-mono text-lg font-bold",
                  player.rank <= 3 ? "text-primary" : "text-muted-foreground"
                )}>
                  {player.score.toLocaleString()}
                </span>
              </div>
            </div>
          ))}
        </div>

        {/* Your Stats */}
        <div className="mt-8 bg-secondary p-6 rounded-xl border-2 border-accent shadow-[4px_4px_0px_0px_var(--color-accent)]">
          <div className="text-center">
            <span className="font-mono text-xs text-accent uppercase tracking-widest">
              Your Global Rank
            </span>
            <div className="font-heading font-bold text-5xl text-primary mt-2">
              #7
            </div>
            <p className="font-sans text-muted-foreground mt-2 text-sm">
              {"You're in the top 0.1% of players!"}
            </p>
          </div>
        </div>
      </main>

      <BottomNav />
    </div>
  )
}
