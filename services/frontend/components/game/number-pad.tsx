interface NumberPadProps {
  onNumberClick?: (num: number) => void
  onDelete?: () => void
}

export function NumberPad({ onNumberClick, onDelete }: NumberPadProps) {
  return (
    <div className="grid grid-cols-5 gap-2">
      {[1, 2, 3, 4, 5, 6, 7, 8, 9].map((num) => (
        <button
          key={num}
          onClick={() => onNumberClick?.(num)}
          className="bg-secondary text-primary font-sans text-2xl sm:text-3xl font-bold aspect-square flex items-center justify-center rounded-lg border-2 border-accent shadow-[3px_3px_0px_0px_var(--color-accent)] active:translate-y-1 active:translate-x-1 active:shadow-none transition-all hover:brightness-110"
        >
          {num}
        </button>
      ))}
      <button
        onClick={onDelete}
        className="bg-destructive text-white font-sans text-2xl sm:text-3xl font-bold aspect-square flex items-center justify-center rounded-lg border-2 border-secondary shadow-[3px_3px_0px_0px_var(--color-secondary)] active:translate-y-1 active:translate-x-1 active:shadow-none transition-all hover:brightness-110"
        aria-label="Delete"
      >
        <span className="material-symbols-outlined text-3xl">backspace</span>
      </button>
    </div>
  )
}
