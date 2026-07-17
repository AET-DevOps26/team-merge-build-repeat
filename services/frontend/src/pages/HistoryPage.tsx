import { useState, useEffect, useCallback } from "react"
import { useNavigate } from "react-router-dom"
import { Header, BottomNav } from "@/components/navigation"
import { useAuth } from "@/src/auth/auth-context"
import { useGame } from "@/src/game-context"

interface GameSummary {
  gameId: string
  templateId: string
  difficulty: string
  filledCells: number
  totalCells: number
}

const DIFFICULTY_COLORS: Record<string, string> = {
  easy: "text-green-400 border-green-500/50 bg-green-500/20",
  medium: "text-yellow-400 border-yellow-500/50 bg-yellow-500/20",
  hard: "text-red-400 border-red-500/50 bg-red-500/20",
}

export default function HistoryPage() {
  const navigate = useNavigate()
  const { user, accessToken } = useAuth()
  const { activeGameId, setActiveGameId } = useGame()
  const [games, setGames] = useState<GameSummary[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [deletingIds, setDeletingIds] = useState<Set<string>>(new Set())
  const [clearConfirm, setClearConfirm] = useState(false)

  const loadGames = useCallback(() => {
    if (!user?.id) return
    setLoading(true)
    fetch(`/application/v1/users/games`, {
      headers: { "Authorization": `Bearer ${accessToken}` },
    })
      .then(res => {
        if (!res.ok) throw new Error(`Failed to load history: ${res.status}`)
        return res.json()
      })
      .then((data: GameSummary[]) => setGames([...data].reverse()))
      .catch(e => setError(e instanceof Error ? e.message : "Failed to load history"))
      .finally(() => setLoading(false))
  }, [user?.id, accessToken])

  useEffect(() => { loadGames() }, [loadGames])

  const handlePlay = (gameId: string) => {
    setActiveGameId(gameId)
    navigate(`/game/${gameId}`)
  }

  const handleDelete = async (gameId: string) => {
    setDeletingIds(prev => new Set(prev).add(gameId))
    try {
      const res = await fetch(`/application/v1/games/${gameId}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${accessToken}` },
      })
      if (!res.ok) throw new Error(`Failed to delete: ${res.status}`)
      setGames(prev => prev.filter(g => g.gameId !== gameId))
      if (activeGameId === gameId) setActiveGameId(null)
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to delete game")
    } finally {
      setDeletingIds(prev => { const s = new Set(prev); s.delete(gameId); return s })
    }
  }

  const handleClearAll = async () => {
    if (!clearConfirm) { setClearConfirm(true); return }
    setClearConfirm(false)
    const ids = games.map(g => g.gameId)
    for (const id of ids) await handleDelete(id)
    setActiveGameId(null)
  }

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header />

      <main className="flex-1 flex flex-col items-center px-6 py-8 pb-24">
        <div className="w-full max-w-2xl">
          <div className="flex items-center justify-between mb-6">
            <h1 className="font-heading font-bold text-3xl text-white uppercase tracking-tight">
              Game History
            </h1>
            {games.length > 0 && (
              <button
                onClick={handleClearAll}
                className={`font-mono text-xs font-bold px-3 py-1.5 rounded-lg border-2 transition-all ${
                  clearConfirm
                    ? "bg-destructive/80 border-destructive text-white"
                    : "bg-destructive/20 border-destructive/50 text-destructive hover:bg-destructive/30"
                }`}
              >
                {clearConfirm ? "Confirm clear all" : "Clear all"}
              </button>
            )}
          </div>

          {clearConfirm && (
            <div className="flex items-center justify-between bg-destructive/10 border-2 border-destructive/50 rounded-lg px-4 py-2 mb-4">
              <p className="text-destructive font-mono text-xs">This will delete all {games.length} games permanently.</p>
              <button onClick={() => setClearConfirm(false)} className="text-foreground/50 hover:text-foreground font-mono text-xs ml-4">
                Cancel
              </button>
            </div>
          )}

          {loading && (
            <div className="flex items-center justify-center py-12">
              <span className="material-symbols-outlined text-accent text-3xl animate-spin">progress_activity</span>
            </div>
          )}

          {error && (
            <div className="bg-destructive/20 border-2 border-destructive text-destructive px-4 py-3 rounded-lg text-sm font-semibold mb-4">
              {error}
            </div>
          )}

          {!loading && !error && games.length === 0 && (
            <div className="text-center py-12">
              <span className="material-symbols-outlined text-accent/50 text-5xl mb-4 block">history</span>
              <p className="text-foreground/60 font-mono text-sm">No games played yet. Start a new game from the home screen!</p>
            </div>
          )}

          {!loading && games.length > 0 && (
            <div className="space-y-3">
              {games.map((game, idx) => {
                const progress = game.totalCells > 0
                  ? Math.round((game.filledCells / game.totalCells) * 100)
                  : 0
                const diffColor = DIFFICULTY_COLORS[game.difficulty.toLowerCase()] ?? "text-foreground border-accent/50 bg-accent/20"
                const isComplete = game.filledCells === game.totalCells && game.totalCells > 0
                const isDeleting = deletingIds.has(game.gameId)

                return (
                  <div
                    key={game.gameId}
                    className={`bg-card border-2 border-secondary rounded-xl p-5 flex items-center gap-4 transition-opacity ${isDeleting ? "opacity-40 pointer-events-none" : ""}`}
                  >
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-2 flex-wrap">
                        <span className={`font-mono text-xs font-bold px-2 py-0.5 rounded border ${diffColor} uppercase`}>
                          {game.difficulty}
                        </span>
                        {isComplete && (
                          <span className="font-mono text-xs font-bold px-2 py-0.5 rounded border text-green-400 border-green-500/50 bg-green-500/20 uppercase">
                            Solved
                          </span>
                        )}
                        <span className="text-foreground/40 font-mono text-xs">
                          #{games.length - idx}
                        </span>
                      </div>

                      <div className="w-full bg-white/10 rounded-full h-2 mb-1">
                        <div
                          className="h-2 rounded-full bg-accent transition-all"
                          style={{ width: `${progress}%` }}
                        />
                      </div>
                      <p className="text-foreground/60 font-mono text-xs">
                        {game.filledCells} / {game.totalCells} cells filled ({progress}%)
                      </p>
                    </div>

                    <div className="shrink-0 flex items-center gap-2">
                      <button
                        onClick={() => handlePlay(game.gameId)}
                        className="bg-accent/80 hover:bg-accent text-white font-heading font-bold text-sm py-2 px-4 rounded-lg border-2 border-primary shadow-[3px_3px_0px_0px_var(--color-primary)] hover:brightness-110 transition-all active:translate-y-0.5 active:translate-x-0.5 active:shadow-none"
                      >
                        {isComplete ? "Review" : "Continue"}
                      </button>
                      <button
                        onClick={() => handleDelete(game.gameId)}
                        disabled={isDeleting}
                        className="p-2 rounded-lg border-2 border-destructive/40 text-destructive/60 hover:bg-destructive/20 hover:text-destructive hover:border-destructive transition-all"
                        title="Delete game"
                      >
                        <span className="material-symbols-outlined text-xl">delete</span>
                      </button>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>
      </main>

      <BottomNav />
    </div>
  )
}
