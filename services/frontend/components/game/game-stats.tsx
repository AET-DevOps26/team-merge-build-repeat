interface GameStatsBarProps {
  score: number
  time: string
}

export function GameStatsBar({ score, time }: GameStatsBarProps) {
  return (
    <div className="flex justify-between items-center bg-muted p-3 rounded-lg border-2 border-accent shadow-[4px_4px_0px_0px_rgba(248,148,29,0.3)]">
      <div className="flex flex-col">
        <span className="font-mono text-xs text-primary uppercase tracking-widest">
          Score
        </span>
        <span className="font-sans text-2xl sm:text-3xl font-bold text-foreground">
          {score.toLocaleString()}
        </span>
      </div>
      <div className="flex flex-col items-end">
        <span className="font-mono text-xs text-primary uppercase tracking-widest">
          Time
        </span>
        <span className="font-sans text-2xl sm:text-3xl font-bold text-accent">
          {time}
        </span>
      </div>
    </div>
  )
}

interface DifficultyChipProps {
  difficulty: "easy" | "medium" | "hard" | "expert"
}

export function DifficultyChip({ difficulty }: DifficultyChipProps) {
  const labels = {
    easy: "EASY MODE",
    medium: "MEDIUM MODE",
    hard: "HARD MODE",
    expert: "EXPERT MODE",
  }

  return (
    <div className="flex justify-center">
      <span className="bg-destructive text-white font-mono text-xs px-4 py-1.5 rounded-full border-2 border-card shadow-[3px_3px_0px_0px_var(--color-secondary)]">
        {labels[difficulty]}
      </span>
    </div>
  )
}
