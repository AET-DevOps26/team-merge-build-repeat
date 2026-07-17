import { createContext, useContext, useState, useEffect, useMemo, ReactNode } from "react"

type Theme = "dark" | "light"

interface ThemeContextValue {
  theme: Theme
  setTheme: (theme: Theme) => void
}

const ThemeContext = createContext<ThemeContextValue | null>(null)
const STORAGE_KEY = "theme"

const LIGHT_COLORS = {
  background: "#ffffff",
  foreground: "#1a1a1a",
  card: "#f5f5f5",
  border: "#e5e5e5",
  primary: "#ffc300",
  secondary: "#4834d4",
  accent: "#f97316",
  muted: "#e5e5e5",
  destructive: "#dc2626",
}

const DARK_COLORS = {
  background: "#1a1a1a",
  foreground: "#ffffff",
  card: "#2a2a2a",
  border: "#3a3a3a",
  primary: "#ffc300",
  secondary: "#4834d4",
  accent: "#f97316",
  muted: "#3a3a3a",
  destructive: "#dc2626",
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setThemeState] = useState<Theme>(() => {
    const stored = localStorage.getItem(STORAGE_KEY)
    return (stored as Theme) || "dark"
  })

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, theme)
    document.documentElement.setAttribute("data-theme", theme)
    document.documentElement.className = theme

    const colors = theme === "light" ? LIGHT_COLORS : DARK_COLORS
    Object.entries(colors).forEach(([key, value]) => {
      document.documentElement.style.setProperty(`--color-${key}`, value)
    })
    console.log("Theme changed to:", theme, "Colors:", colors)
  }, [theme])

  const value = useMemo<ThemeContextValue>(() => ({
    theme,
    setTheme: setThemeState,
  }), [theme])

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
}

export function useTheme() {
  const context = useContext(ThemeContext)
  if (!context) throw new Error("useTheme must be used inside ThemeProvider.")
  return context
}
