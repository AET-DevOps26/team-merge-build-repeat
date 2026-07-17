import { FormEvent, useState } from "react"
import { Navigate, useLocation, useNavigate } from "react-router-dom"
import { Header } from "@/components/navigation"
import { useAuth } from "@/src/auth/auth-context"

export default function LoginPage() {
  const { session, signInWithPassword, signUpWithPassword } = useAuth()
  const [mode, setMode] = useState<"sign-in" | "sign-up">("sign-in")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()
  const location = useLocation()
  const from = (location.state as { from?: { pathname?: string } } | null)?.from?.pathname ?? "/"

  if (session) {
    return <Navigate to={from} replace />
  }

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setLoading(true)
    setError(null)
    setMessage(null)

    try {
      if (mode === "sign-in") {
        await signInWithPassword(email, password)
        navigate("/", { replace: true })
      } else {
        await signUpWithPassword(email, password)
        setMessage("Account created. Check your inbox if email confirmation is enabled.")
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Authentication failed.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header />

      <main className="flex-1 flex items-center justify-center px-6 py-8">
        <form
          onSubmit={handleSubmit}
          className="w-full max-w-sm bg-card border-2 border-secondary rounded p-5 flex flex-col gap-4"
        >
          <div>
            <h1 className="font-heading font-bold text-3xl text-primary uppercase">
              {mode === "sign-in" ? "Sign in" : "Create account"}
            </h1>
            <p className="text-muted-foreground text-sm mt-1">
              {mode === "sign-in" ? "Use your Sudoku account." : "Start with a new account."}
            </p>
          </div>

          <label className="flex flex-col gap-2 text-sm font-bold">
            Email
            <input
              type="email"
              value={email}
              onChange={event => setEmail(event.target.value)}
              required
              autoComplete="email"
              className="bg-white/10 border-[1.5px] border-accent/50 text-foreground p-3 h-12 rounded font-sans focus:outline-none focus:border-primary"
            />
          </label>

          <label className="flex flex-col gap-2 text-sm font-bold">
            Password
            <input
              type="password"
              value={password}
              onChange={event => setPassword(event.target.value)}
              required
              minLength={6}
              autoComplete={mode === "sign-in" ? "current-password" : "new-password"}
              className="bg-white/10 border-[1.5px] border-accent/50 text-foreground p-3 h-12 rounded font-sans focus:outline-none focus:border-primary"
            />
          </label>

          {error && <p className="text-destructive font-semibold text-sm">{error}</p>}
          {message && <p className="text-primary font-semibold text-sm">{message}</p>}

          <button
            type="submit"
            disabled={loading}
            className="bg-accent text-white font-heading font-bold text-lg py-3 px-6 rounded border-2 border-primary shadow-[3px_3px_0px_0px_var(--color-primary)] hover:brightness-110 transition-all disabled:opacity-50"
          >
            {loading ? "Please wait" : mode === "sign-in" ? "Sign in" : "Create account"}
          </button>

          <button
            type="button"
            onClick={() => {
              setMode(mode === "sign-in" ? "sign-up" : "sign-in")
              setError(null)
              setMessage(null)
            }}
            className="text-primary text-sm font-bold hover:text-white transition-colors"
          >
            {mode === "sign-in" ? "Need an account?" : "Already have an account?"}
          </button>
        </form>
      </main>
    </div>
  )
}
