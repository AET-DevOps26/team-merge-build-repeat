import { createContext, useContext, useState, useEffect, useMemo, useRef } from "react"
import type { ReactNode } from "react"
import { useAuth } from "@/src/auth/auth-context"

const storageKeyFor = (userId: string) => `activeGameId:${userId}`

interface GameContextValue {
  activeGameId: string | null
  setActiveGameId: (id: string | null) => void
}

const GameContext = createContext<GameContextValue | null>(null)

export function GameProvider({ children }: { children: ReactNode }) {
  const { session, loading } = useAuth()
  const userId = session?.user.id ?? null
  const previousUserId = useRef<string | null>(null)
  const [activeGameId, setActiveGameIdState] = useState<string | null>(null)
  const [hydratedUserId, setHydratedUserId] = useState<string | null>(null)

  useEffect(() => {
    if (loading) return

    if (previousUserId.current && previousUserId.current !== userId) {
      setActiveGameIdState(null)
    }

    previousUserId.current = userId
    setActiveGameIdState(userId ? localStorage.getItem(storageKeyFor(userId)) : null)
    setHydratedUserId(userId)
  }, [loading, userId])

  useEffect(() => {
    if (!userId || hydratedUserId !== userId) return
    const key = storageKeyFor(userId)
    if (activeGameId) localStorage.setItem(key, activeGameId)
    else localStorage.removeItem(key)
  }, [activeGameId, hydratedUserId, userId])

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
