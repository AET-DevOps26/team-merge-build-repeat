import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { Header, BottomNav } from "@/components/navigation"
import { useAuth } from "@/src/auth/auth-context"

type Difficulty = "easy" | "medium" | "hard"

const UUID_REGEX = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i

function formatUUID(chars: string[]): string {
  const value = chars.join('')
  return [value.slice(0, 8), value.slice(8, 12), value.slice(12, 16), value.slice(16, 20), value.slice(20, 32)]
    .filter(Boolean)
    .join('-')
}

function isValidUUID(chars: string[]): boolean {
  if (chars.some(c => c === '')) return false
  return UUID_REGEX.test(formatUUID(chars))
}

export default function HomePage() {
  const navigate = useNavigate()
  const { user, accessToken } = useAuth()
  const [loading, setLoading] = useState(false)
  const [uuidChars, setUuidChars] = useState<string[]>(Array(32).fill(''))
  const [error, setError] = useState<string | null>(null)

  const handleNewGame = async (difficulty: Difficulty) => {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch(`/application/v1/games/random?difficulty=${difficulty}`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${accessToken}`,
        },
      })
      if (!res.ok) throw new Error(`Failed to create game: ${res.status}`)
      const data = await res.json()
      navigate(`/game/${data.gameId}`, { state: { templateId: data.templateId } })
    } catch (e) {
      const msg = e instanceof Error ? e.message : "Failed to create game"
      setError(msg)
      setLoading(false)
    }
  }

  const handleTemplateGame = async () => {
    const templateId = formatUUID(uuidChars)

    if (!isValidUUID(uuidChars)) {
      setError("Please enter a valid template ID")
      return
    }
    setLoading(true)
    setError(null)
    try {
      const res = await fetch(`/application/v1/templates/${templateId}/new-game`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${accessToken}`,
        },
      })
      if (!res.ok) throw new Error(`Failed to create game from template: ${res.status}`)
      const data = await res.json()
      navigate(`/game/${data.gameId}`, { state: { templateId: data.templateId } })
    } catch (e) {
      const msg = e instanceof Error ? e.message : "Failed to create game from template"
      setError(msg)
      setLoading(false)
    }
  }

  const handleTemplateIdChange = (value: string) => {
    const chars = value.replace(/[^0-9a-f]/gi, '').slice(0, 32).toLowerCase().split('')
    setUuidChars([...chars, ...Array(32 - chars.length).fill('')])
  }

  const handleContinue = async () => {
    if (!user?.id) {
      setError("Not logged in")
      return
    }
    setLoading(true)
    setError(null)
    try {
      const res = await fetch(`/application/v1/users/latest-game`, {
        headers: {
          "Authorization": `Bearer ${accessToken}`,
        },
      })
      if (!res.ok) throw new Error(`Failed to fetch latest game: ${res.status}`)
      const gameId = await res.text()
      navigate(`/game/${gameId.replace(/"/g, '')}`)
    } catch (e) {
      const msg = e instanceof Error ? e.message : "Failed to load latest game"
      setError(msg)
      setLoading(false)
    }
  }

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

        {/* Main Buttons */}
        <div className="w-full max-w-2xl space-y-6">
          {/* Error Message */}
          {error && (
            <div className="bg-destructive/20 border-2 border-destructive text-destructive px-4 py-3 rounded-lg text-sm font-semibold">
              {error}
            </div>
          )}

          {/* Game Creation Bubble */}
          <div className="bg-card border-2 border-secondary rounded-xl p-8">
            <h3 className="text-foreground font-heading font-bold text-lg mb-6 uppercase tracking-tight">New Game</h3>

            <div className="space-y-6">
              {/* Difficulty Buttons */}
              <div className="grid grid-cols-3 gap-4">
                <button
                  onClick={() => handleNewGame("easy")}
                  disabled={loading}
                  className="w-full bg-green-500/30 hover:bg-green-500/40 text-white font-bold py-3 px-4 rounded-lg border-2 border-green-500/50 hover:border-green-500 transition-all active:translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  😊 Easy
                </button>
                <button
                  onClick={() => handleNewGame("medium")}
                  disabled={loading}
                  className="w-full bg-yellow-500/30 hover:bg-yellow-500/40 text-white font-bold py-3 px-4 rounded-lg border-2 border-yellow-500/50 hover:border-yellow-500 transition-all active:translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  🎯 Medium
                </button>
                <button
                  onClick={() => handleNewGame("hard")}
                  disabled={loading}
                  className="w-full bg-red-500/30 hover:bg-red-500/40 text-white font-bold py-3 px-4 rounded-lg border-2 border-red-500/50 hover:border-red-500 transition-all active:translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  🔥 Hard
                </button>
              </div>

              {/* With ID Section */}
              <div className="flex flex-col">
                <label htmlFor="template-id" className="text-foreground font-heading font-bold text-sm mb-3 uppercase tracking-tight">or load by template id</label>
                <div className="mb-3">
                  <input
                    id="template-id"
                    type="text"
                    value={formatUUID(uuidChars)}
                    onChange={(e) => handleTemplateIdChange(e.target.value)}
                    disabled={loading}
                    inputMode="text"
                    autoComplete="off"
                    spellCheck={false}
                    placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
                    aria-describedby="template-id-help"
                    className="w-full bg-white/10 border-2 border-accent/50 text-foreground rounded px-3 py-3 focus:outline-none focus:border-accent focus:ring-2 focus:ring-accent/50 disabled:opacity-50 transition-all font-mono font-bold"
                  />
                  <p id="template-id-help" className="mt-2 text-xs text-foreground/70">Paste or enter a template UUID.</p>
                </div>
                <button
                  onClick={handleTemplateGame}
                  disabled={loading || !isValidUUID(uuidChars)}
                  className="w-full bg-accent/30 hover:bg-accent/40 text-white font-bold py-3 px-4 rounded-lg border-2 border-accent/50 hover:border-accent transition-all active:translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  📋 Load
                </button>
              </div>
            </div>
          </div>

          {/* Continue Button */}
          <button
            onClick={handleContinue}
            disabled={loading}
            className="w-full bg-accent/80 hover:bg-accent text-white font-heading font-bold text-xl py-4 px-8 rounded-xl border-2 border-primary shadow-[4px_4px_0px_0px_var(--color-primary)] hover:brightness-110 transition-all active:translate-y-1 active:translate-x-1 active:shadow-none disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span className="flex items-center justify-center gap-3">
              <span className="material-symbols-outlined text-2xl">fast_forward</span>
              CONTINUE
            </span>
          </button>

          {loading && (
            <div className="flex items-center justify-center py-4">
              <span className="material-symbols-outlined text-accent text-3xl animate-spin">progress_activity</span>
            </div>
          )}
        </div>
      </main>

      <BottomNav />
    </div>
  )
}
