import { useState } from "react"

export type Difficulty = "easy" | "medium" | "hard"

interface DifficultySelectorProps {
  onSelect: (difficulty: Difficulty) => void
  loading?: boolean
}

export function DifficultySelector({ onSelect, loading }: DifficultySelectorProps) {
  const difficulties: { value: Difficulty; label: string; emoji: string }[] = [
    { value: "easy", label: "Easy", emoji: "😊" },
    { value: "medium", label: "Medium", emoji: "🎯" },
    { value: "hard", label: "Hard", emoji: "🔥" },
  ]

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-card border-2 border-secondary rounded-xl p-8 max-w-md w-full mx-4 shadow-lg">
        <h2 className="text-2xl font-bold text-foreground mb-6 text-center">Select Difficulty</h2>
        
        <div className="space-y-3">
          {difficulties.map(({ value, label, emoji }) => (
            <button
              key={value}
              onClick={() => onSelect(value)}
              disabled={loading}
              className="w-full flex items-center justify-between bg-accent/20 hover:bg-accent/30 text-foreground font-bold py-4 px-6 rounded-lg border-2 border-accent/50 hover:border-accent transition-all disabled:opacity-50 disabled:cursor-not-allowed active:translate-y-1"
            >
              <span>{label}</span>
              <span className="text-2xl">{emoji}</span>
            </button>
          ))}
        </div>

        {loading && (
          <div className="mt-6 flex items-center justify-center">
            <span className="material-symbols-outlined text-accent text-3xl animate-spin">progress_activity</span>
          </div>
        )}
      </div>
    </div>
  )
}
