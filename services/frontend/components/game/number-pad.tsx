import { cn } from "@/lib/utils"

interface NumberPadProps {
  onNumberClick?: (num: number) => void
  onDelete?: () => void
  onUndo?: () => void
  onRedo?: () => void
  canUndo?: boolean
  canRedo?: boolean
  pencilMode?: boolean
  onTogglePencil?: () => void
  onCheck?: () => void
  onSolve?: () => void
}

export function NumberPad({
  onNumberClick,
  onDelete,
  onUndo,
  onRedo,
  canUndo,
  canRedo,
  pencilMode,
  onTogglePencil,
  onCheck,
  onSolve,
}: NumberPadProps) {
  return (
    <div className="flex flex-col gap-2">
      <button
        onClick={onTogglePencil}
        aria-label="Toggle pencil mode"
        aria-pressed={pencilMode}
        className={cn(
          "w-full h-14 md:h-20 flex items-center justify-center rounded-lg border-2 transition-all active:translate-y-1 active:translate-x-1 active:shadow-none hover:brightness-110",
          pencilMode
            ? "bg-accent text-white border-primary shadow-[2px_2px_0px_0px_var(--color-primary)]"
            : "bg-secondary text-primary border-accent shadow-[2px_2px_0px_0px_var(--color-accent)]"
        )}
      >
        <span className="material-symbols-outlined text-2xl md:text-3xl">edit</span>
      </button>
      <div className="grid grid-cols-3 gap-2">
        {[1, 2, 3, 4, 5, 6, 7, 8, 9].map((num) => (
          <button
            key={num}
            onClick={() => onNumberClick?.(num)}
            className="bg-secondary text-primary font-sans text-xl md:text-2xl font-bold w-14 h-14 md:w-20 md:h-20 flex items-center justify-center rounded-lg border-2 border-accent shadow-[2px_2px_0px_0px_var(--color-accent)] active:translate-y-1 active:translate-x-1 active:shadow-none transition-all hover:brightness-110"
          >
            {num}
          </button>
        ))}
      </div>
      <div className="grid grid-cols-3 gap-2">
        <button
          onClick={onUndo}
          disabled={!canUndo}
          aria-label="Undo"
          className="bg-secondary text-primary w-full h-14 md:h-20 flex items-center justify-center rounded-lg border-2 border-accent shadow-[2px_2px_0px_0px_var(--color-accent)] active:translate-y-1 active:translate-x-1 active:shadow-none transition-all hover:brightness-110 disabled:opacity-40 disabled:pointer-events-none"
        >
          <span className="material-symbols-outlined text-2xl md:text-3xl">undo</span>
        </button>
        <button
          onClick={onDelete}
          aria-label="Delete"
          className="bg-destructive text-white w-full h-14 md:h-20 flex items-center justify-center rounded-lg border-2 border-secondary shadow-[2px_2px_0px_0px_var(--color-secondary)] active:translate-y-1 active:translate-x-1 active:shadow-none transition-all hover:brightness-110"
        >
          <span className="material-symbols-outlined text-2xl md:text-3xl">backspace</span>
        </button>
        <button
          onClick={onRedo}
          disabled={!canRedo}
          aria-label="Redo"
          className="bg-secondary text-primary w-full h-14 md:h-20 flex items-center justify-center rounded-lg border-2 border-accent shadow-[2px_2px_0px_0px_var(--color-accent)] active:translate-y-1 active:translate-x-1 active:shadow-none transition-all hover:brightness-110 disabled:opacity-40 disabled:pointer-events-none"
        >
          <span className="material-symbols-outlined text-2xl md:text-3xl">redo</span>
        </button>
      </div>
      <div className="grid grid-cols-2 gap-2 w-full">
        <button
          onClick={onCheck}
          aria-label="Check"
          className="bg-accent text-primary w-full h-14 md:h-20 flex items-center justify-center rounded-lg border-2 border-primary shadow-[2px_2px_0px_0px_var(--color-primary)] active:translate-y-1 active:translate-x-1 active:shadow-none transition-all hover:brightness-110"
        >
          <span className="material-symbols-outlined text-2xl md:text-3xl">check</span>
        </button>
        <button
          onClick={onSolve}
          aria-label="Solve"
          className="bg-destructive text-white w-full h-14 md:h-20 flex items-center justify-center rounded-lg border-2 border-secondary shadow-[2px_2px_0px_0px_var(--color-secondary)] active:translate-y-1 active:translate-x-1 active:shadow-none transition-all hover:brightness-110"
        >
          <span className="material-symbols-outlined text-2xl md:text-3xl">lightbulb</span>
        </button>
      </div>
    </div>
  )
}
