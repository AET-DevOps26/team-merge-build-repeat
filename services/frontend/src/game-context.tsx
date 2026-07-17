import { createContext, useContext, useState, useEffect, useMemo } from "react"
import type { ReactNode } from "react"
import { useAuth } from "@/src/auth/auth-context"

const STORAGE_KEY = "activeGameId"

interface GameContextValue {
  activeGameId: string | null
  setActiveGameId: (id: string | null) => void
}

const GameContext = createContext<GameContextValue | null>(null)

export function GameProvider({ children }: { children: ReactNode }) {
  const { session } = useAuth()
  const [activeGameId, setActiveGameIdState] = useState<string | null>(
    () => localStorage.getItem(STORAGE_KEY)
  )

  useEffect(() => {
    if (activeGameId) {
      localStorage.setItem(STORAGE_KEY, activeGameId)
    } else {
      localStorage.removeItem(STORAGE_KEY)
    }
  }, [activeGameId])

  useEffect(() => {
    if (!session) {
      setActiveGameIdState(null)
      localStorage.removeItem(STORAGE_KEY)
    }
  }, [session])

  const value = useMemo<GameContextValue>(() => ({
    activeGameId,
    setActiveGameId: setActiveGameIdState,
  }), [activeGameId])

  return <GameContext.Provider value={value}>{children}</GameContext.Provider>
}

export function useGame() {
  const context = useContext(GameContext)
  if (!context) throw new Error("useGame must be used inside GameProvider.")
  return context
}
